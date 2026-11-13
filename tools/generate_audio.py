#!/usr/bin/env python3
"""Build reusable ACARS MP3 announcements from templates.json + config.json."""

import argparse
import asyncio
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RATE_RE = re.compile(r"^[+-]\d{1,3}%$")
PITCH_RE = re.compile(r"^[+-]\d{1,3}Hz$")
FILENAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*\.mp3$", re.IGNORECASE)
UNRESOLVED_RE = re.compile(r"\{\{.*?\}\}|\[[^\]]+\]")


def fail(message):
    raise ValueError(message)


def load_json(filename):
    with (ROOT / filename).open(encoding="utf-8") as handle:
        return json.load(handle)


def resolve(config, template):
    roles = config["roles"]
    tts = config["tts_defaults"]
    audio = config["audio"]
    presets = audio["effect_presets"]
    seen_ids, seen_files = set(), set()
    plans = []
    if template.get("schema_version") != 1 or config.get("schema_version") != 1:
        fail("Unsupported schema_version (expected 1)")
    if not isinstance(template.get("announcements"), list) or not template["announcements"]:
        fail("templates.json must include a nonempty announcements list")
    if template.get("variables"):
        fail("All announcements must be static; top-level variables must be empty")
    for item in template["announcements"]:
        identifier = item.get("id")
        if not isinstance(identifier, str) or not re.fullmatch(r"[a-z0-9][a-z0-9_]*", identifier):
            fail(f"Invalid announcement id: {identifier!r}")
        if identifier in seen_ids:
            fail(f"Duplicate announcement id: {identifier}")
        seen_ids.add(identifier)
        filename = item.get("filename", identifier + ".mp3")
        if not isinstance(filename, str) or not FILENAME_RE.fullmatch(filename) or ".." in filename:
            fail(f"{identifier}: invalid filename {filename!r}; use an MP3 basename only")
        if filename.casefold() in seen_files:
            fail(f"Duplicate output filename: {filename}")
        seen_files.add(filename.casefold())
        text = item.get("text")
        if not isinstance(text, str) or not text.strip() or UNRESOLVED_RE.search(text):
            fail(f"{identifier}: text is empty or contains unresolved placeholders")
        if item.get("variables"):
            fail(f"{identifier}: this generator only supports static announcements")
        role = item.get("speaker")
        if role not in roles:
            fail(f"{identifier}: unknown speaker role {role!r}")
        voice = item.get("voice") or roles[role]["voice"]
        if not isinstance(voice, str) or not re.fullmatch(r"[A-Za-z0-9-]+", voice):
            fail(f"{identifier}: invalid Edge voice name")
        overrides = item.get("audio") or {}
        if not isinstance(overrides, dict):
            fail(f"{identifier}: audio overrides must be an object")
        if set(overrides) - {"rate", "pitch", "volume", "effect"}:
            fail(f"{identifier}: unknown audio override(s): {set(overrides) - {'rate', 'pitch', 'volume', 'effect'}}")
        settings = {k: overrides.get(k, tts[k]) for k in ("rate", "pitch", "volume")}
        for key, regex in (("rate", RATE_RE), ("pitch", PITCH_RE), ("volume", RATE_RE)):
            if not isinstance(settings[key], str) or not regex.fullmatch(settings[key]):
                fail(f"{identifier}: invalid {key} {settings[key]!r}; expected e.g. '+5%' or '+0Hz'")
        channel = item.get("channel", "passenger_pa")
        effect = overrides.get("effect", audio["channel_effects"].get(channel, audio["default_effect"]))
        if effect not in presets:
            fail(f"{identifier}: unknown effect {effect!r}; use {', '.join(presets)}")
        for key in ("highpass_hz", "lowpass_hz", "presence_hz", "presence_gain_db",
                    "compressor_threshold", "compressor_ratio", "compressor_attack_ms",
                    "compressor_release_ms", "compressor_makeup",
                    "crusher_bits", "crusher_mix", "noise_amplitude", "noise_mix"):
            if key not in presets[effect] or type(presets[effect][key]) not in (float, int):
                fail(f"config.json: {effect} preset missing numeric {key}")
        preset = presets[effect]
        if preset["highpass_hz"] < 0 or not 0 <= preset["lowpass_hz"] < audio["sample_rate_hz"] / 2:
            fail(f"{effect}: invalid cutoff frequencies")
        if preset["highpass_hz"] > 0 and preset["lowpass_hz"] > 0 and preset["highpass_hz"] >= preset["lowpass_hz"]:
            fail(f"{effect}: highpass must be lower than lowpass")
        if not 0 <= preset["presence_hz"] < audio["sample_rate_hz"] / 2 or not -12 <= preset["presence_gain_db"] <= 12:
            fail(f"{effect}: presence EQ out of range")
        if not 0 <= preset["compressor_threshold"] <= 1 or not 1 <= preset["compressor_ratio"] <= 20:
            fail(f"{effect}: invalid compression settings")
        if not 0.01 <= preset["compressor_attack_ms"] <= 2000 or not 0.01 <= preset["compressor_release_ms"] <= 9000:
            fail(f"{effect}: invalid compression timing")
        if not 1 <= preset["compressor_makeup"] <= 8:
            fail(f"{effect}: invalid compressor makeup gain")
        if not 0 <= preset["crusher_mix"] <= 1 or not 0 <= preset["noise_mix"] <= 1:
            fail(f"{effect}: mix levels must be between 0 and 1")
        if not 0 <= preset["noise_amplitude"] <= 0.1 or not 0 <= preset["crusher_bits"] <= 64:
            fail(f"{effect}: static or bit-crusher settings out of range")
        plans.append({
            "id": identifier, "filename": filename, "event": item.get("event", ""),
            "speaker": role, "channel": channel, "voice": voice, "text": text,
            "rate": settings["rate"], "pitch": settings["pitch"], "volume": settings["volume"],
            "effect": effect,
        })
    if not isinstance(audio.get("sample_rate_hz"), int) or audio["sample_rate_hz"] < 8000:
        fail("audio.sample_rate_hz must be an integer >= 8000")
    if not isinstance(audio.get("bitrate_kbps"), int) or audio["bitrate_kbps"] not in (64, 96, 128, 160, 192, 256, 320):
        fail("audio.bitrate_kbps must be a supported MP3 bitrate")
    return plans


def process_audio(raw, output, audio, preset):
    """Apply configurable radio/PA frequency, distortion, and static using FFmpeg."""
    rate = audio["sample_rate_hz"]
    args = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-y", "-i", str(raw)]
    filters = []
    if preset["highpass_hz"] > 0:
        filters.append(f"highpass=f={preset['highpass_hz']}")
    if preset["lowpass_hz"] > 0:
        filters.append(f"lowpass=f={preset['lowpass_hz']}")
    # PA microphones and ceiling speakers emphasize speech consonants around 2-3 kHz.
    if preset["presence_hz"] > 0 and preset["presence_gain_db"] != 0:
        filters.append(
            f"equalizer=f={preset['presence_hz']}:t=q:w=1:g={preset['presence_gain_db']}"
        )
    # A PA amplifier's leveled voice is more recognizable than constant added hiss.
    if preset["compressor_threshold"] > 0 and preset["compressor_ratio"] > 1:
        filters.append(
            "acompressor="
            f"threshold={preset['compressor_threshold']}:"
            f"ratio={preset['compressor_ratio']}:"
            f"attack={preset['compressor_attack_ms']}:"
            f"release={preset['compressor_release_ms']}:"
            f"makeup={preset['compressor_makeup']}"
        )
    if preset["crusher_mix"] > 0:
        filters.append(f"acrusher=bits={preset['crusher_bits']}:mix={preset['crusher_mix']}")
    if preset["noise_amplitude"] > 0 and preset["noise_mix"] > 0:
        args += ["-f", "lavfi", "-i", (
            f"anoisesrc=color=white:amplitude={preset['noise_amplitude']}:sample_rate={rate}"
        )]
        chain = ",".join(filters) if filters else "anull"
        graph = (
            f"[0:a]{chain}[speech];"
            f"[speech][1:a]amix=inputs=2:duration=first:"
            f"weights='1 {preset['noise_mix']}':normalize=0,"
            f"alimiter=limit=0.95[out]"
        )
        args += ["-filter_complex", graph, "-map", "[out]"]
    elif filters:
        args += ["-af", ",".join(filters) + ",alimiter=limit=0.95"]
    args += ["-ar", str(rate), "-c:a", "libmp3lame",
             "-b:a", f"{audio['bitrate_kbps']}k", str(output)]
    subprocess.run(args, check=True)
    subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(output)],
        check=True, stdout=subprocess.DEVNULL,
    )
    if not output.is_file() or output.stat().st_size < 512:
        fail(f"Audio output is empty or invalid: {output.name}")


def generation_settings(config):
    settings = config.get("generation")
    if not isinstance(settings, dict):
        fail("Missing generation settings in config.json")
    timeout = settings.get("timeout_seconds")
    attempts = settings.get("max_attempts")
    retry_delay = settings.get("retry_delay_seconds")
    if type(timeout) not in (int, float) or not 1 <= timeout <= 120:
        fail("generation.timeout_seconds must be a number from 1 to 120")
    if type(attempts) is not int or attempts not in (1, 2):
        fail("generation.max_attempts must be 1 or 2 (at most one retry)")
    if type(retry_delay) not in (int, float) or not 0 <= retry_delay <= 60:
        fail("generation.retry_delay_seconds must be a number from 0 to 60")
    return timeout, attempts, retry_delay


async def synthesize(plan, target, timeout_seconds, attempts, retry_delay_seconds):
    import edge_tts

    for attempt in range(1, attempts + 1):
        try:
            communicate = edge_tts.Communicate(
                text=plan["text"], voice=plan["voice"],
                rate=plan["rate"], pitch=plan["pitch"], volume=plan["volume"],
            )
            await asyncio.wait_for(
                communicate.save(str(target)), timeout=timeout_seconds
            )
            if not target.is_file() or target.stat().st_size < 512:
                raise RuntimeError("Edge returned an empty audio file")
            return
        except Exception as exc:
            target.unlink(missing_ok=True)
            detail = (
                f"timeout after {timeout_seconds}s"
                if isinstance(exc, TimeoutError) else str(exc)
            )
            print(
                f"{plan['id']} ({plan['voice']}): attempt "
                f"{attempt}/{attempts} failed: {detail}",
                file=sys.stderr, flush=True,
            )
            if attempt >= attempts:
                raise RuntimeError(
                    f"{plan['id']} ({plan['voice']}): failed after "
                    f"{attempts} attempt(s); aborting all audio generation"
                ) from exc
            print(
                f"Retrying {plan['id']} in {retry_delay_seconds}s...",
                file=sys.stderr, flush=True,
            )
            await asyncio.sleep(retry_delay_seconds)


def package(output_dir, plans):
    manifest = {
        "schema_version": 1, "format": "mp3", "count": len(plans),
        "announcements": [{k: value for k, value in p.items() if k != "text"} for p in plans],
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
    )
    archive = output_dir.parent / "ACARS-Announcements-audio.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.write(output_dir / "manifest.json", "manifest.json")
        for plan in sorted(plans, key=lambda x: x["filename"]):
            z.write(output_dir / plan["filename"], "audio/" + plan["filename"])
    print(f"Packaged {len(plans)} recordings -> {archive}")


async def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate", action="store_true", help="Check config without Edge or FFmpeg")
    parser.add_argument("--output", default="dist/audio", help="Directory for generated MP3s")
    args = parser.parse_args()
    config, template = load_json("config.json"), load_json("templates.json")
    plans = resolve(config, template)
    timeout_seconds, attempts, retry_delay_seconds = generation_settings(config)
    print(
        f"Validated {len(plans)} announcements "
        f"({len(set(p['voice'] for p in plans))} voices), "
        f"timeout={timeout_seconds}s, attempts={attempts}, retry_delay={retry_delay_seconds}s"
    )
    if args.validate:
        return
    out = Path(args.output).resolve()
    if out in (ROOT.resolve(), ROOT.parent.resolve(), Path("/")):
        fail("Unsafe output directory")
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    raw_dir = out.parent / ".tts-raw"
    shutil.rmtree(raw_dir, ignore_errors=True)
    raw_dir.mkdir(parents=True)
    try:
        for index, plan in enumerate(plans, 1):
            print(f"[{index}/{len(plans)}] {plan['id']} | {plan['voice']} | {plan['effect']}", flush=True)
            raw = raw_dir / (plan["id"] + ".mp3")
            await synthesize(
                plan, raw, timeout_seconds, attempts, retry_delay_seconds
            )
            process_audio(raw, out / plan["filename"], config["audio"],
                          config["audio"]["effect_presets"][plan["effect"]])
        package(out, plans)
    finally:
        shutil.rmtree(raw_dir, ignore_errors=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (ValueError, RuntimeError, OSError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

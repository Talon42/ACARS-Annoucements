#!/usr/bin/env python3
"""Build reusable ACARS MP3 announcements from templates.json + config.json."""

import argparse
import asyncio
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RATE_RE = re.compile(r"^[+-]\d{1,3}%$")
PITCH_RE = re.compile(r"^[+-]\d{1,3}Hz$")
FILENAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*\.mp3$", re.IGNORECASE)
UNRESOLVED_RE = re.compile(r"\{\{.*?\}\}|\[[^\]]+\]")
SPEECH_CACHE = ROOT / "speech-cache"
MP3_SAMPLE_RATES = {8000, 11025, 12000, 16000, 22050, 24000, 32000, 44100, 48000}


def fail(message):
    raise ValueError(message)


def load_json(filename):
    with (ROOT / filename).open(encoding="utf-8") as handle:
        return json.load(handle)


def resolve(config, template):
    engine = config.get("tts_engine", "edge")
    if engine not in ("edge", "kokoro"):
        fail("tts_engine must be 'edge' or 'kokoro'")
    roles = config["roles"]
    tts = config["tts_defaults"]
    audio = config["audio"]
    presets = audio["effect_presets"]
    if type(audio.get("sample_rate_hz")) is not int or audio["sample_rate_hz"] not in MP3_SAMPLE_RATES:
        fail("audio.sample_rate_hz must be a supported MP3 sample rate")
    if type(audio.get("bitrate_kbps")) is not int or audio["bitrate_kbps"] not in (64, 96, 128, 160, 192, 256, 320):
        fail("audio.bitrate_kbps must be a supported MP3 bitrate")
    if audio["sample_rate_hz"] < 32000 and audio["bitrate_kbps"] > 160:
        fail("MP3 sample rates below 32000 Hz support at most 160 kbps")
    known_voices = {v["short_name"] for v in load_json("voices.json")["voices"]
                    if v.get("engine", "edge") == engine}
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
        title = item.get("title")
        if not isinstance(title, str) or not title.strip():
            fail(f"{identifier}: title must be a nonempty string")
        text = item.get("text")
        if not isinstance(text, str) or not text.strip() or UNRESOLVED_RE.search(text):
            fail(f"{identifier}: text is empty or contains unresolved placeholders")
        if item.get("variables"):
            fail(f"{identifier}: this generator only supports static announcements")
        role = item.get("speaker")
        if role not in roles:
            fail(f"{identifier}: unknown speaker role {role!r}")
        voice = item.get("voice") or roles[role].get("voices", {}).get(engine, roles[role].get("voice"))
        if not isinstance(voice, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", voice):
            fail(f"{identifier}: invalid {engine} voice name")
        if voice not in known_voices:
            fail(f"{identifier}: unknown voice {voice!r}; refresh the voice catalog if needed")
        overrides = item.get("audio") or {}
        if not isinstance(overrides, dict):
            fail(f"{identifier}: audio overrides must be an object")
        if set(overrides) - {"rate", "pitch", "volume", "effect"}:
            fail(f"{identifier}: unknown audio override(s): {set(overrides) - {'rate', 'pitch', 'volume', 'effect'}}")
        settings = {k: overrides.get(k, tts[k]) for k in ("rate", "pitch", "volume")}
        for key, regex in (("rate", RATE_RE), ("pitch", PITCH_RE), ("volume", RATE_RE)):
            if not isinstance(settings[key], str) or not regex.fullmatch(settings[key]):
                fail(f"{identifier}: invalid {key} {settings[key]!r}; expected e.g. '+5%' or '+0Hz'")
        language = ""
        if engine == "kokoro":
            if voice[:2] not in ("af", "am", "bf", "bm"):
                fail(f"{identifier}: this generator currently supports English Kokoro voices only")
            language = "en-us" if voice.startswith("a") else "en-gb"
            if not -50 <= int(settings["rate"][:-1]) <= 100:
                fail(f"{identifier}: Kokoro rate must be between -50% and +100%")
            if int(settings["pitch"][:-2]) != 0:
                fail(f"{identifier}: Kokoro does not support pitch offsets; use +0Hz")
            if int(settings["volume"][:-1]) < -100:
                fail(f"{identifier}: Kokoro volume must be at least -100%")
        effect = overrides.get("effect", audio["default_effect"])
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
            "engine": engine, "language": language,
            "id": identifier, "filename": filename, "title": title,
            "speaker": role, "voice": voice, "text": text,
            "rate": settings["rate"], "pitch": settings["pitch"], "volume": settings["volume"],
            "effect": effect,
        })
        if engine == "kokoro":
            # Model/voice-pack and runtime changes must not reuse another model's speech.
            plans[-1]["model_fingerprint"] = fingerprint({
                "assets": config["kokoro"],
                "runtime": file_hash(ROOT / "requirements.txt"),
                "synthesizer": file_hash(ROOT / "tools/kokoro_tts.py"),
            })
    return plans


def fingerprint(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def speech_key(plan):
    # No effect, filename, role, or title: only inputs that change spoken audio.
    inputs = {k: plan[k] for k in ("text", "voice", "rate", "pitch", "volume")}
    if plan.get("engine", "edge") == "kokoro":
        inputs.update(engine="kokoro", language=plan["language"], model=plan["model_fingerprint"])
    return fingerprint({"version": 1, **inputs})


def processing_key(plan, config):
    audio = config["audio"]
    return fingerprint({
        "speech_key": speech_key(plan),
        "preset": audio["effect_presets"][plan["effect"]],
        "sample_rate_hz": audio["sample_rate_hz"], "bitrate_kbps": audio["bitrate_kbps"],
        # Code changes must not silently reuse outputs from an older processor.
        "generator_sha256": file_hash(Path(__file__)),
    })


def manifest_entry(plan, config, path):
    return {
        **{k: value for k, value in plan.items() if k != "text"},
        "speech_key": speech_key(plan), "processing_key": processing_key(plan, config),
        "sha256": file_hash(path),
    }


def speech_path(plan):
    return SPEECH_CACHE / (speech_key(plan) + (".wav" if plan["engine"] == "kokoro" else ".mp3"))


def cached_speech(plan):
    path = speech_path(plan)
    checksum = path.with_suffix(".sha256")
    return (path.is_file() and path.stat().st_size >= 512 and checksum.is_file()
            and checksum.read_text(encoding="utf-8").strip() == file_hash(path))


def previous_recordings():
    try:
        manifest = load_json("audio/manifest.json")
        return {entry["id"]: entry for entry in manifest["announcements"]}
    except (OSError, ValueError, KeyError, TypeError):
        return {}


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
    if config.get("tts_engine", "edge") == "kokoro":
        timeout = settings.get("kokoro_timeout_seconds")
        if type(timeout) not in (int, float) or not 1 <= timeout <= 600:
            fail("generation.kokoro_timeout_seconds must be a number from 1 to 600")
    return timeout, attempts, retry_delay


async def synthesize(plan, target, timeout_seconds, attempts, retry_delay_seconds, kokoro=None):
    for attempt in range(1, attempts + 1):
        try:
            if plan["engine"] == "kokoro":
                await asyncio.to_thread(kokoro.generate, plan, target, timeout_seconds)
            else:
                import edge_tts
                communicate = edge_tts.Communicate(
                    text=plan["text"], voice=plan["voice"],
                    rate=plan["rate"], pitch=plan["pitch"], volume=plan["volume"],
                )
                await asyncio.wait_for(
                    communicate.save(str(target)), timeout=timeout_seconds
                )
            if not target.is_file() or target.stat().st_size < 512:
                raise RuntimeError(f"{plan['engine']} returned an empty audio file")
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


def write_manifest(output_dir, plans, config):
    manifest = {
        "schema_version": 1, "format": "mp3", "count": len(plans),
        "announcements": [manifest_entry(p, config, output_dir / p["filename"]) for p in plans],
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
    )
    print(f"Wrote manifest for {len(plans)} recordings -> {output_dir}")


async def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate", action="store_true", help="Check config without TTS engines or FFmpeg")
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
    print(f"Active TTS engine: {config.get('tts_engine', 'edge')}", flush=True)
    for role in config["roles"]:
        assigned = sorted({p["voice"] for p in plans if p["speaker"] == role})
        if assigned:
            print(f"  {role}: {', '.join(assigned)}", flush=True)
        else:
            settings = config["roles"][role]
            voice = settings.get("voices", {}).get(config.get("tts_engine", "edge"), settings.get("voice"))
            print(f"  {role}: {voice} (no announcements assigned)", flush=True)
    if args.validate:
        return
    out = Path(args.output).resolve()
    if out in (ROOT.resolve(), ROOT.parent.resolve(), Path("/")):
        fail("Unsafe output directory")
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    SPEECH_CACHE.mkdir(parents=True, exist_ok=True)
    previous = previous_recordings()
    reused = processed = generated = 0
    kokoro = None
    if config.get("tts_engine", "edge") == "kokoro":
        from kokoro_tts import KokoroSynthesizer
        kokoro = KokoroSynthesizer(config["kokoro"])
    try:
        for index, plan in enumerate(plans, 1):
            print(f"[{index}/{len(plans)}] {plan['id']} | {plan['voice']} | {plan['effect']}", flush=True)
            raw = speech_path(plan)
            old = previous.get(plan["id"], {})
            # Resolve the old path only from a validated basename.
            old_name = old.get("filename", "")
            old_path = ROOT / "audio" / old_name
            if (FILENAME_RE.fullmatch(old_name) and ".." not in old_name
                    and old_path.is_file() and old_path.resolve() != (out / plan["filename"]).resolve()
                    and old.get("processing_key") == processing_key(plan, config)
                    and old.get("sha256") == file_hash(old_path) and cached_speech(plan)):
                shutil.copyfile(old_path, out / plan["filename"])
                reused += 1
                print("  Reused unchanged MP3", flush=True)
                continue
            if not cached_speech(plan):
                temporary = raw.with_name(raw.stem + ".tmp" + raw.suffix)
                try:
                    await synthesize(
                        plan, temporary, timeout_seconds, attempts, retry_delay_seconds, kokoro
                    )
                    temporary.replace(raw)
                    raw.with_suffix(".sha256").write_text(file_hash(raw) + "\n", encoding="utf-8")
                finally:
                    temporary.unlink(missing_ok=True)
                generated += 1
                print("  Generated clean speech", flush=True)
            else:
                print("  Reused clean speech; applying PA effect", flush=True)
            process_audio(raw, out / plan["filename"], config["audio"],
                          config["audio"]["effect_presets"][plan["effect"]])
            processed += 1
        write_manifest(out, plans, config)
        # Keep only active clean speech, after the entire pack succeeds.
        active = {speech_key(plan) for plan in plans}
        for path in SPEECH_CACHE.iterdir():
            if path.suffix in (".mp3", ".wav", ".sha256") and path.stem not in active:
                path.unlink()
        print(f"Complete: {reused} unchanged MP3s, {generated} new speech recordings, {processed} processed MP3s")
    finally:
        if kokoro is not None:
            kokoro.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (ValueError, RuntimeError, OSError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


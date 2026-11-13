#!/usr/bin/env python3
"""Refresh Edge's live voices and Kokoro's pinned upstream voice pack together."""

import asyncio
import json
from pathlib import Path

import edge_tts

from kokoro_tts import voice_names

ROOT = Path(__file__).resolve().parents[1]
LOCALES = {
    "a": ("en-US", "American English"), "b": ("en-GB", "British English"),
    "j": ("ja-JP", "Japanese"), "z": ("cmn-CN", "Mandarin Chinese"),
    "e": ("es-ES", "Spanish"), "f": ("fr-FR", "French"),
    "h": ("hi-IN", "Hindi"), "i": ("it-IT", "Italian"), "p": ("pt-BR", "Brazilian Portuguese"),
}


def kokoro_entries(names):
    voices = []
    for name in names:
        locale, language = LOCALES.get(name[0], ("unknown", "Unknown language"))
        voices.append({
            "engine": "kokoro", "short_name": name,
            "gender": "Female" if name[1] == "f" else "Male", "locale": locale,
            "friendly_name": name[3:].replace("_", " ").title() + f" ({language})",
            "content_categories": [], "voice_personalities": [],
            "supported": name[0] in ("a", "b"),
        })
    return voices


def write_catalog(voices):
    voices.sort(key=lambda v: (v["engine"], v["locale"], v["short_name"]))
    counts = {engine: sum(v["engine"] == engine for v in voices) for engine in ("edge", "kokoro")}
    output = {
        "schema_version": 1,
        "source": "Microsoft Edge via edge-tts; Kokoro via the configured upstream ONNX voice pack",
        "count": len(voices), "counts_by_engine": counts, "voices": voices,
    }
    lines = [
        "# Edge and Kokoro voice catalog", "",
        "Run **Actions > Refresh TTS Voices > Run workflow** to update both engines together.",
        "The weekly refresh runs on the default branch. Select kokoro for a manual branch refresh; both engines refresh weekly after merge.",
        "", f"**Available voices:** {len(voices)} ({counts['edge']} Edge, {counts['kokoro']} Kokoro)", "",
        "Set tts_engine in config.json to edge or kokoro. Role defaults are in `roles.<role>.voices.<engine>`.",
        "A templates.json voice override must belong to the selected engine.", "",
        "Kokoro entries come from the voice pack configured in config.json, so the list matches the installed model assets.",
        "This generator currently supports American and British English Kokoro voices; other voices are listed for reference.",
        "Kokoro model weights: Apache-2.0. See https://huggingface.co/hexgrad/Kokoro-82M.", "",
        "| Engine | Short name | Gender | Locale | Friendly name | Supported by generator |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for voice in voices:
        columns = (voice["engine"], voice["short_name"], voice["gender"], voice["locale"],
                   voice["friendly_name"], "Yes" if voice.get("supported", True) else "Catalog only")
        safe = [str(value).replace("|", "\\|").replace("\n", " ") for value in columns]
        lines.append("| " + " | ".join(safe) + " |")
    # Fetch and validate both sources before replacing either catalog.
    (ROOT / "voices.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "VOICES.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Refreshed {counts['edge']} Edge and {counts['kokoro']} Kokoro voices")


async def main():
    raw = await asyncio.wait_for(edge_tts.list_voices(), timeout=60)
    if not raw or len(raw) < 10:
        raise RuntimeError("Edge returned an unexpectedly small/empty voice list")
    voices = []
    for item in raw:
        tag = item.get("VoiceTag") or {}
        voices.append({
            "engine": "edge", "short_name": item["ShortName"],
            "gender": item.get("Gender", ""), "locale": item.get("Locale", ""),
            "friendly_name": item.get("FriendlyName", ""),
            "content_categories": tag.get("ContentCategories", []),
            "voice_personalities": tag.get("VoicePersonalities", []), "supported": True,
        })
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    voices.extend(kokoro_entries(voice_names(config["kokoro"])))
    write_catalog(voices)


if __name__ == "__main__":
    asyncio.run(main())

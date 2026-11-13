#!/usr/bin/env python3
"""Refresh the live Edge TTS voice catalog (JSON + browseable Markdown)."""

import asyncio
import json
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parents[1]


async def main():
    raw = await edge_tts.list_voices()
    if not raw or len(raw) < 10:
        raise RuntimeError("Edge returned an unexpectedly small/empty voice list")
    voices = []
    for item in raw:
        tag = item.get("VoiceTag") or {}
        voices.append({
            "short_name": item["ShortName"],
            "gender": item.get("Gender", ""),
            "locale": item.get("Locale", ""),
            "friendly_name": item.get("FriendlyName", ""),
            "content_categories": tag.get("ContentCategories", []),
            "voice_personalities": tag.get("VoicePersonalities", []),
        })
    voices.sort(key=lambda v: (v["locale"], v["short_name"]))
    output = {
        "schema_version": 1,
        "source": "Microsoft Edge online voices via edge-tts (unofficial service)",
        "count": len(voices),
        "voices": voices,
    }
    (ROOT / "voices.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Edge TTS voice catalog", "",
        "Generated from the live Edge voice service. Run **Actions > Refresh Edge Voices > Run workflow** to refresh.",
        "", f"**Available voices:** {len(voices)}", "",
        "Use a short_name in config.json (role defaults) or templates.json (individual announcement override).",
        "", "| Short name | Gender | Locale | Friendly name |",
        "| --- | --- | --- | --- |",
    ]
    for voice in voices:
        columns = (voice["short_name"], voice["gender"], voice["locale"], voice["friendly_name"])
        safe = [str(value).replace("|", "\\|").replace("\n", " ") for value in columns]
        lines.append("| " + " | ".join(safe) + " |")
    (ROOT / "VOICES.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Refreshed {len(voices)} voices in voices.json and VOICES.md")


if __name__ == "__main__":
    asyncio.run(main())

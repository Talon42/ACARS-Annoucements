#!/usr/bin/env python3
"""Package the MP3s already committed under /audio; never synthesize speech."""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

from generate_audio import load_json, manifest_entry, resolve

ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "audio"
SEMVER = re.compile(r"^v([0-9]+)\.([0-9]+)\.([0-9]+)$")


def fail(message):
    raise ValueError(message)


def next_version():
    result = subprocess.run(
        ["git", "tag", "--list"], cwd=ROOT, check=True, capture_output=True, text=True
    )
    numbers = []
    for tag in result.stdout.splitlines():
        match = SEMVER.fullmatch(tag.strip())
        if match:
            numbers.append(tuple(map(int, match.groups())))
    if not numbers:
        return "v1.0.0"
    major, minor, patch = max(numbers)
    return f"v{major}.{minor}.{patch + 1}"


def collect_mp3s():
    if not AUDIO.is_dir():
        fail("No /audio folder in this commit. Run Generate ACARS Audio first.")
    files = sorted(
        (path for path in AUDIO.iterdir() if path.is_file() and path.suffix.lower() == ".mp3"),
        key=lambda p: p.name.casefold(),
    )
    if not files:
        fail("No .mp3 files found in /audio. Generate and commit audio before releasing.")
    names = set()
    for path in files:
        if path.name.casefold() in names:
            fail(f"Case-insensitive filename collision in /audio: {path.name}")
        names.add(path.name.casefold())
        if path.is_symlink() or not path.stat().st_size >= 512:
            fail(f"Empty, too-small, or symlinked MP3: {path.name}")
        with path.open("rb") as handle:
            header = handle.read(3)
        if not (header.startswith(b"ID3") or (
            len(header) >= 2 and header[0] == 0xFF and header[1] & 0xE0 == 0xE0
        )):
            fail(f"{path.name} does not appear to be a valid MP3")
    manifest_path = AUDIO / "manifest.json"
    if not manifest_path.is_file():
        fail("Missing audio/manifest.json. Run Generate ACARS Audio before releasing.")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    config = load_json("config.json")
    plans = resolve(config, load_json("templates.json"))
    expected_names = {plan["filename"].casefold() for plan in plans}
    if expected_names != names or len(plans) != len(files):
        fail("MP3s do not match current templates. Run Generate ACARS Audio before releasing.")
    expected_entries = [manifest_entry(plan, config, AUDIO / plan["filename"]) for plan in plans]
    if (manifest.get("schema_version") != 1 or manifest.get("format") != "mp3"
            or manifest.get("count") != len(plans)
            or manifest.get("announcements") != expected_entries):
        fail("Audio is stale or modified: scripts, voices, PA settings, generator, or MP3 checksums differ. "
             "Run Generate ACARS Audio before releasing (unchanged speech is reused).")
    return files


def make_zip(path, files):
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED) as archive:
        for file in files:
            # Flat ZIP: MP3 audio only, no manifest, no directories.
            info = zipfile.ZipInfo(file.name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o100644 << 16
            with archive.open(info, "w") as destination, file.open("rb") as source:
                shutil.copyfileobj(source, destination)
    with zipfile.ZipFile(path) as check:
        if check.testzip() is not None or check.namelist() != [p.name for p in files]:
            fail("Final release ZIP failed content validation")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="dist/releases")
    args = parser.parse_args()
    files = collect_mp3s()
    tag = next_version()
    target = (ROOT / args.output_dir).resolve()
    if target == AUDIO.resolve() or AUDIO.resolve() in target.parents:
        fail("Cannot write the release archive inside /audio")
    filename = f"ACARS-Announcements-{tag}.zip"
    archive = target / filename
    make_zip(archive, files)
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as handle:
            handle.write(f"tag={tag}\n")
            handle.write(f"archive={archive}\n")
            handle.write(f"count={len(files)}\n")
    print(f"Prepared {archive} with {len(files)} MP3-only entries; next tag: {tag}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

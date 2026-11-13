# ACARS Announcements

This repository builds reusable Edge TTS cabin-crew and flight-deck audio for ACARS. All 16 supplied announcements are **fully generic and flight-independent**. ACARS already handles the playback triggers; this project handles generating and distributing the audio.

## Quick start

1. Edit [templates.json](templates.json) to modify wording, add an announcement, change the speaker, or change the exported MP3 filename.
2. Edit [config.json](config.json) to adjust default male/female voices, speech rate, pitch, volume, output format, or radio/PA effects.
3. Commit changes to main; the **Generate ACARS Audio** workflow runs automatically.
4. Open [Generate ACARS Audio](../../actions/workflows/generate-audio.yml) and download the **acars-announcements-audio** workflow artifact from a successful run. This contains the MP3 ZIP and its manifest.
5. To publish a persistent pack under [GitHub Releases](../../releases), choose **Run workflow** and enter a new release_tag (example: v1.0.0). Blank release_tag means artifact-only.

## Important files

| File | Purpose |
| --- | --- |
| [templates.json](templates.json) | Announcement text, stable IDs, filenames, role and per-announcement overrides |
| [config.json](config.json) | Role voice defaults, speaking rate, pitch/volume, MP3 settings, and effect presets |
| [VOICES.md](VOICES.md) | Browseable Edge voice names, gender and locale |
| [voices.json](voices.json) | Machine-readable voice catalog |
| [tools/generate_audio.py](tools/generate_audio.py) | Validates scripts, synthesizes MP3, applies FFmpeg effects, packages audio |
| [tools/update_voices.py](tools/update_voices.py) | Fetches the live Edge voice list |
| [Generate ACARS Audio workflow](.github/workflows/generate-audio.yml) | Auto-build and manual build / optional Release |
| [Refresh Edge Voices workflow](.github/workflows/refresh-voices.yml) | Refresh voice catalog automatically each Monday or on demand |

## Adding or editing announcements

Each entry in the **announcements** array of templates.json represents one MP3. A simplified example:

    {
      "id": "boarding_welcome_fa",
      "event": "boarding_complete",
      "title": "Boarding Complete / Welcome Aboard",
      "speaker": "flight_attendant",
      "channel": "passenger_pa",
      "text": "Ladies and gentlemen, welcome aboard. Thank you for flying with us.",
      "variables": [],
      "filename": "boarding_welcome_fa.mp3",
      "voice": null,
      "audio": {}
    }

To customize *only* this recording, you can edit its filename, voice, and audio settings:

    "filename": "welcome_message.mp3",
    "voice": "en-US-AriaNeural",
    "audio": {
      "rate": "+8%",
      "pitch": "+0Hz",
      "volume": "+0%",
      "effect": "medium"
    }

- **id** stays stable for ACARS trigger mapping even if you change the filename.
- **filename** must be a unique MP3 basename (no directories/slashes); you can name files as desired.
- **voice: null** inherits the voice for that speaker from config.json; otherwise specify any valid Edge voice name.
- **audio: {}** inherits rate/pitch/volume and the channel's default effect. Override any subset of them individually.
- **speaker** can be captain (male default), copilot (male default), or flight_attendant (female default); other roles can be defined in config.json.
- **channel** may be passenger_pa or crew_interphone; the latter is not intended for passenger playback.
- **variables** must remain an empty array. This is a static, generic sound library. Dynamic placeholders are rejected by the generator.

To add a new announcement, duplicate an existing object, give it a unique **id** and **filename**, and update the text and other fields. No extra Python code or workflow changes are needed.

## Default voice selections

| Speaker | Edge voice | Gender |
| --- | --- | --- |
| captain | en-US-GuyNeural | Male |
| copilot | en-US-ChristopherNeural | Male |
| flight_attendant | en-US-JennyNeural | Female |

These are defaults in config.json, not mandatory choices. Each announcement can override **voice** independently.

Open [VOICES.md](VOICES.md) to browse the available voices. Use [Refresh Edge Voices](../../actions/workflows/refresh-voices.yml) > **Run workflow** to fetch the latest available list; a weekly run also updates voices.json and VOICES.md when changes are detected.

## Speed and radio/PA effects

In config.json, adjust **tts_defaults.rate** (e.g. -10% slower or +10% faster), **pitch** (e.g. +0Hz), and **volume** (e.g. +0%). These can be overridden in an individual announcement's audio object.

The audio.channel_effects map selects a preset for passenger_pa or crew_interphone. Default presets are:

| Preset | Sound |
| --- | --- |
| off | Clean voice, no filters/static |
| low | Light PA/radio coloration |
| medium | Narrower bandwidth with audible radio grit/static |
| high | Strong radio distortion/static |

Each preset in **audio.effect_presets** defines highpass_hz, lowpass_hz, crusher_bits, crusher_mix, noise_amplitude, and noise_mix. All of these can be tuned to change the sound. To remove a component, set its mix to 0. Every announcement can also select **audio.effect** independently.

Output MP3 sample rate and bitrate are adjustable via **audio.sample_rate_hz** and **audio.bitrate_kbps**.

## Generated ZIP and manifest

Each successful build produces **dist/ACARS-Announcements-audio.zip** containing:

    manifest.json
    audio/
      boarding_welcome_fa.mp3
      boarding_welcome_captain.mp3
      ...
      deboarding_fa.mp3

The manifest maps **id** to **filename**, and records event, speaker, channel, voice, speech rate/pitch/volume, and effect. ACARS can resolve existing trigger IDs to the correct filenames without relying on filenames being fixed forever.

The build currently regenerates the entire pack; there is no incremental audio cache. Each successful GitHub Actions run uploads a download artifact retained for 30 days. A manual run with **release_tag** set to an x.y.z tag (prefixed by v) also publishes the ZIP as a GitHub Release asset.

## Local build

Requires Python 3.12+, FFmpeg with MP3 encoding support, internet access to Edge's online TTS service, and these commands:

    python -m pip install -r requirements.txt
    python tools/generate_audio.py --validate
    python tools/generate_audio.py

Validation detects duplicate IDs, duplicate filenames, invalid placeholders, missing speaker roles, unknown effects, invalid voice/audio settings, and unsafe filenames. Synthesis failures fail the action instead of uploading a partial pack.

## Limitations

This uses the unofficial [edge-tts](https://github.com/rany2/edge-tts) interface; availability and service behavior can change. Check licensing/redistribution terms before distributing recordings broadly. The scripts (including safety instructions) are intended for simulation, not actual aviation safety announcements. This repository generates sound packs but does not yet modify ACARS playback code.

# ACARS Announcements

This repository builds reusable Edge TTS cabin-crew and flight-deck audio for ACARS. All 16 supplied announcements are **fully generic and flight-independent**. ACARS already handles the playback triggers; this project handles generating and distributing the audio.

## Quick start

1. Edit [templates.json](templates.json) to change scripts, filenames, or individual voices; edit [config.json](config.json) for role defaults, speed, volume, and radio/PA effects.
2. Commit changes to main, or manually run [Generate ACARS Audio](../../actions/workflows/generate-audio.yml). It generates changed speech and reuses unchanged recordings and **commits the MP3 files plus manifest.json to [/audio](audio/)**. Generated audio is also available as a temporary Actions artifact.
3. Open [/audio](audio/), listen to the MP3 files, and adjust settings and regenerate as many times as desired. Each successful run replaces the current /audio contents. Previous versions remain in Git history.
4. When satisfied, open [Publish Final Audio Release](../../actions/workflows/publish-final-audio.yml), select **Run workflow** on **main**, and run it. This is the **only** workflow that publishes a release.
5. The release workflow packages the currently committed MP3 files from /audio **without regenerating** them. It chooses the next version automatically (first v1.0.0, then v1.0.1, v1.0.2, etc.), creates the Git tag, and publishes the MP3-only ZIP under [Releases](../../releases).

**Important:** Let Generate ACARS Audio finish successfully and commit its files before running Publish Final Audio Release. The two workflows share a concurrency group to prevent publishing during generation.

## Important files

| File | Purpose |
| --- | --- |
| [/audio](audio/) | Committed generated MP3s and manifest.json; review these before releasing |
| [/speech-cache](speech-cache/) | Clean speech keyed by text, voice, rate, pitch, and volume; reused across generations |
| [templates.json](templates.json) | Announcement text, stable IDs, filenames, role and per-announcement overrides |
| [config.json](config.json) | Role voice defaults, speaking rate, pitch/volume, MP3 settings, and unified PA effect presets |
| [VOICES.md](VOICES.md) | Browseable Edge voice names, gender and locale |
| [voices.json](voices.json) | Machine-readable voice catalog |
| [tools/generate_audio.py](tools/generate_audio.py) | Validates scripts, synthesizes MP3, applies FFmpeg effects, packages audio |
| [tools/update_voices.py](tools/update_voices.py) | Fetches the live Edge voice list |
| [Generate ACARS Audio workflow](.github/workflows/generate-audio.yml) | Automatic/manual regeneration, commit /audio, and preview artifact |
| [Refresh Edge Voices workflow](.github/workflows/refresh-voices.yml) | Refresh voice catalog automatically each Monday or on demand |
| [Publish Final Audio Release workflow](.github/workflows/publish-final-audio.yml) | Manual-only: create version/tag and MP3-only release ZIP |
| [tools/release_audio.py](tools/release_audio.py) | Validate and package the committed /audio recordings; never synthesizes audio |

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
- **audio: {}** inherits rate/pitch/volume and the unified default PA effect. Override any subset of them individually.
- **speaker** can be captain (male default), copilot (male default), or flight_attendant (female default); other roles can be defined in config.json.
- **channel** may be passenger_pa or crew_interphone; the latter is not intended for passenger playback.
- **variables** must remain an empty array. This is a static, generic sound library. Dynamic placeholders are rejected by the generator.

To add a new announcement, duplicate an existing object, give it a unique **id** and **filename**, and update the text and other fields. No extra Python code or workflow changes are needed.

## Default voice selections

| Speaker | Edge voice | Gender |
| --- | --- | --- |
| captain | en-US-AndrewNeural | Male |
| copilot | en-US-BrianNeural | Male |
| flight_attendant | en-US-EmmaNeural | Female |

These are defaults in config.json, not mandatory choices. Each announcement can override **voice** independently.

Open [VOICES.md](VOICES.md) to browse the available voices. Use [Refresh Edge Voices](../../actions/workflows/refresh-voices.yml) > **Run workflow** to fetch the latest available list; a weekly run also updates voices.json and VOICES.md when changes are detected.

## Speed and radio/PA effects

In config.json, adjust **tts_defaults.rate** (e.g. -10% slower or +10% faster), **pitch** (e.g. +0Hz), and **volume** (e.g. +0%). These can be overridden in an individual announcement's audio object.

The audio.default_effect setting selects one unified PA effect for both passenger_pa and crew_interphone. Channels remain metadata for ACARS routing; they do not select different processing. Available strength presets are:

| Preset | Sound |
| --- | --- |
| off | Clean voice, no filters/static |
| low | Light PA/radio coloration |
| medium | Narrower bandwidth with audible radio grit/static |
| high | Strong radio distortion/static |

Each preset in **audio.effect_presets** defines highpass_hz, lowpass_hz, crusher_bits, crusher_mix, noise_amplitude, and noise_mix. All of these can be tuned to change the sound. To remove a component, set its mix to 0. Every announcement can also select **audio.effect** independently.

Output MP3 sample rate and bitrate are adjustable via **audio.sample_rate_hz** and **audio.bitrate_kbps**.

## Selective generation and speech reuse

Clean speech is cached by announcement text, resolved voice, rate, pitch, and volume, with a checksum for corruption detection. Successful workflow runs commit this cache alongside /audio, so it persists between runners.

- An unchanged recording is copied byte-for-byte from committed /audio when its fingerprints and checksum match.
- Changing only the PA effect, its strength/settings, sample rate, or bitrate reprocesses cached clean speech without contacting Edge.
- Changing a role voice regenerates only announcements that resolve to that voice; explicit voice overrides are respected.
- Changing text regenerates only that announcement. Changing rate/pitch/volume regenerates only recordings whose resolved values changed.
- Renaming an output or changing event/channel metadata does not require new speech.
- Missing or damaged clean speech is regenerated with the existing timeout/retry policy. Unused cache entries are removed after a successful build.

The first run after upgrading must generate clean speech once: older processed MP3s cannot be used as clean originals and their manifests lack source fingerprints. A failed run never replaces committed /audio. Release validation does not require the clean cache or call Edge; it checks the finished pack against current inputs.

## Generated audio, preview artifacts, and finalized releases

Every successful generation on main commits the current recordings to **/audio** and reusable clean speech to **/speech-cache**:

    audio/
      boarding_welcome_fa.mp3
      boarding_welcome_captain.mp3
      ...
      deboarding_fa.mp3
      manifest.json

The manifest maps stable IDs to filenames, event, speaker, channel, voice, rate/pitch/volume, and effect. It also stores fingerprints of speech inputs and processing settings/code, plus a checksum of each final MP3. Release validation compares these with the current sources and files, rejecting stale or modified audio even when filenames match. The workflow fully replaces /audio each time (so removing or renaming templates also removes obsolete MP3s). As a safety measure, it will not force-push if main changed while audio was synthesizing.

Every generation also uploads an optional 30-day preview artifact named **acars-announcements-audio**, containing a ZIP with manifest.json and audio/MP3 files. **A generation run never publishes a GitHub Release.**

Only **Publish Final Audio Release** creates a release. It reads **exactly the MP3s already committed under /audio on main** and builds a ZIP with the MP3 files directly at its root. No manifest, directories, scripts, configuration, or other files are included. It validates the files against audio/manifest.json but does not include that manifest in the release ZIP.

The first release gets **v1.0.0** unless matching version tags already exist; subsequent releases increment the highest vMAJOR.MINOR.PATCH tag's **patch** number. For example, after v1.0.0, the next is v1.0.1. The release asset is named **ACARS-Announcements-v1.0.1.zip**. There is no version input required.

GitHub's Releases page also automatically shows built-in *Source code (zip/tar.gz)* links; those are provided by GitHub separately. The **ACARS-Announcements-vX.Y.Z.zip** asset is the MP3-only archive.

The release uses the specific committed main SHA reviewed at release time and will fail rather than package an uncommitted or changing set of recordings. Run it again after resolving any conflict. It does not generate new audio.

## Local build

Requires Python 3.12+, FFmpeg with MP3 encoding support, internet access to Edge's online TTS service, and these commands:

    python -m pip install -r requirements.txt
    python tools/generate_audio.py --validate
    python tools/generate_audio.py

Validation detects duplicate IDs, duplicate filenames, invalid placeholders, missing speaker roles, unknown effects, voices absent from voices.json, unsupported MP3 sample rates/bitrates, invalid voice/audio settings, and unsafe filenames. Voice checking uses the committed catalog without a network call; refresh the catalog if a newly available voice is missing. Synthesis failures fail the action instead of uploading a partial pack. When run locally, generated files remain under dist/; only the GitHub workflow copies them into /audio and commits them together with /speech-cache.

## Limitations

This uses the unofficial [edge-tts](https://github.com/rany2/edge-tts) interface; availability and service behavior can change. Check licensing/redistribution terms before distributing recordings broadly. The scripts (including safety instructions) are intended for simulation, not actual aviation safety announcements. This repository generates sound packs but does not yet modify ACARS playback code.

# ACARS Announcements

This repository builds reusable Edge TTS cabin-crew and flight-deck audio for ACARS. All 16 supplied announcements are **fully generic and flight-independent**. ACARS already handles the playback triggers; this project handles generating and distributing the audio.

## Quick start

1. Edit [templates.json](templates.json) to change scripts, filenames, or individual voices; edit [config.json](config.json) for role defaults, speed, volume, and the unified PA effect.
2. Commit changes to templates.json or config.json on **main**, or manually run [Generate ACARS Audio](https://github.com/Talon42/ACARS-Annoucements/actions/workflows/generate-audio.yml) with **main** selected. It reuses unchanged recordings, generates only missing or changed speech, and **commits the final MP3s and manifest.json to [/audio](audio/) together with clean speech in [/speech-cache](speech-cache/)**. A successful generation also uploads a preview ZIP as a 30-day Actions artifact.
3. Open [/audio](audio/), listen to the MP3 files, and adjust settings and regenerate as many times as desired. Each successful run replaces the current /audio contents. Previous versions remain in Git history.
4. When satisfied, open [Publish Final Audio Release](https://github.com/Talon42/ACARS-Annoucements/actions/workflows/publish-final-audio.yml), select **Run workflow** on **main**, and run it. This is the **only** workflow that publishes a release.
5. The release workflow packages the currently committed MP3 files from /audio **without regenerating** them. It chooses the next version automatically (first v1.0.0, then v1.0.1, v1.0.2, etc.), creates the Git tag, and publishes the MP3-only ZIP under [Releases](https://github.com/Talon42/ACARS-Annoucements/releases).

**Important:** Let Generate ACARS Audio finish successfully and commit its files before running Publish Final Audio Release. The generation and release workflows share a concurrency group, so they do not run at the same time. Release validation also rejects audio that no longer matches the current inputs.

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
| [Generate ACARS Audio workflow](.github/workflows/generate-audio.yml) | Selective generation, commit /audio and /speech-cache, and preview artifact |
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

All supplied announcements currently use role voices and global delivery settings (`"voice": null`, `"audio": {}`), including the global **+20%** rate. To customize *only* one recording, the generator also supports filename, voice, and audio overrides. For example:

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
- **voice: null** inherits the voice for that speaker from config.json; otherwise specify an Edge voice short name present in voices.json.
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

Open [VOICES.md](VOICES.md) to browse the available voices. Use [Refresh Edge Voices](https://github.com/Talon42/ACARS-Annoucements/actions/workflows/refresh-voices.yml) > **Run workflow** to fetch the latest available list; a weekly run also updates voices.json and VOICES.md when changes are detected.

## Current defaults and unified PA effect

The current config.json defaults are:

| Setting | Current value |
| --- | --- |
| Speaking rate (`tts_defaults.rate`) | `+20%` |
| Pitch (`tts_defaults.pitch`) | `+0Hz` |
| TTS volume (`tts_defaults.volume`) | `+0%` |
| Unified PA strength (`audio.default_effect`) | `medium` |
| MP3 sample rate (`audio.sample_rate_hz`) | `24000` Hz |
| MP3 bitrate (`audio.bitrate_kbps`) | `128` kbps |

Adjust rate, pitch, and volume in **tts_defaults** to change global speech delivery. Per-announcement audio overrides take precedence; the supplied templates currently have none.

The audio.default_effect setting selects one unified PA effect for both passenger_pa and crew_interphone. Channels remain metadata for ACARS routing; they do not select different processing. Available strength presets are:

| Preset | Sound |
| --- | --- |
| off | Clean voice, no filters/static |
| low | Subtle speech coloration, compression, and light distortion/static |
| medium | Default: narrower bandwidth, speech presence EQ, compression, and moderate distortion/static |
| high | Stronger bandwidth restriction, compression, and distortion/static |

Each preset in **audio.effect_presets** configures:

- **highpass_hz / lowpass_hz:** speech frequency range; set a cutoff to 0 to disable that filter.
- **presence_hz / presence_gain_db:** speech presence EQ; set the gain to 0 to disable it.
- **compressor_threshold / compressor_ratio / compressor_attack_ms / compressor_release_ms / compressor_makeup:** voice compression; set threshold to 0 or ratio to 1 to disable it.
- **crusher_bits / crusher_mix:** bit-crusher distortion; set crusher_mix to 0 to disable it.
- **noise_amplitude / noise_mix:** added white noise; set either to 0 to disable it.

The same preset system applies to every channel. An announcement can select a different strength through its **audio.effect** override; there are no separate PA and interphone profiles. A limiter follows enabled processing. The supplied **off** preset bypasses effects, but the output is still encoded to the configured MP3 format.

Output MP3 sample rate and bitrate are adjustable via **audio.sample_rate_hz** and **audio.bitrate_kbps**. Validation checks supported settings before synthesis.

## Selective generation and speech reuse

Clean speech is cached by announcement text, resolved voice, rate, pitch, and volume, with a checksum for corruption detection. Successful workflow runs commit this cache alongside /audio, so it persists between runners.

- An unchanged recording is copied byte-for-byte from committed /audio when its processing fingerprint and checksum match and its clean speech cache is intact.
- Changing only the PA effect, its strength/settings, sample rate, or bitrate reprocesses affected recordings from cached clean speech without contacting Edge. Recordings whose effective settings did not change retain their existing MP3s.
- Changing a role voice regenerates only announcements that resolve to that voice; explicit voice overrides are respected.
- Changing text regenerates only that announcement. Changing rate/pitch/volume regenerates only recordings whose resolved values changed.
- Renaming an output or changing event/channel metadata does not require new speech. If the ID stays the same and processing is unchanged, the committed MP3 is reused.
- Missing or damaged clean speech is regenerated with the timeout/retry policy below. Unused cache entries are removed after a successful build.
- Changes to tools/generate_audio.py invalidate final MP3 processing fingerprints, so cached clean speech is reprocessed. They do not automatically require new speech.

When clean speech is absent, it must be generated once; processed MP3s cannot serve as clean originals. Older manifests without fingerprints also require a generation run before release. Successful runs preserve the cache for subsequent builds. A failed run never replaces committed /audio. Release validation does not require the clean cache or call Edge; it checks the finished pack against current inputs.

## Timeouts and retries

These settings are under **generation** in config.json:

| Setting | Current value | Behavior |
| --- | --- | --- |
| timeout_seconds | 10 | Maximum wait for each individual TTS download attempt |
| max_attempts | 2 | One initial attempt and at most one retry |
| retry_delay_seconds | 10 | Wait before retrying a failed attempt |

Announcements are processed sequentially. If both attempts fail, generation aborts immediately without processing later announcements or uploading a partial preview. These limits apply to speech downloads, not FFmpeg processing or the whole workflow; cached speech needs no TTS attempt.

## Workflow triggers

- **Generate ACARS Audio:** runs for pushes to main or pull requests that change templates.json, config.json, voices.json, requirements.txt, tools/generate_audio.py, or its own workflow file. It can also be run manually on main. Pull-request runs upload previews but do not commit audio or the cache to the repository.
- **Refresh Edge Voices:** runs each Monday at **10:25 UTC**, on demand, or when its script/workflow changes on main. It updates voices.json and VOICES.md when the catalog changes.
- **Publish Final Audio Release:** manual-only, and requires main. It packages existing committed audio; it never synthesizes speech.
- A README-only edit does not trigger audio generation.

## Generated audio, preview artifacts, and finalized releases

After successful generation on main, the workflow updates **/audio** and **/speech-cache**, creating a commit only when their contents changed:

    audio/
      boarding_welcome_fa.mp3
      boarding_welcome_captain.mp3
      ...
      deboarding_fa.mp3
      manifest.json

The manifest maps stable IDs to filenames, event, speaker, channel, voice, rate/pitch/volume, and effect. It also stores fingerprints of speech inputs and processing settings/code, plus a checksum of each final MP3. Release validation compares these with the current sources and files, rejecting stale or modified audio even when filenames match. The workflow fully replaces /audio each time (so removing or renaming templates also removes obsolete MP3s). As a safety measure, it will not force-push if main changed while audio was synthesizing.

Every successful generation also uploads a required 30-day preview artifact named **acars-announcements-audio**, containing a ZIP with manifest.json and audio/MP3 files. **A generation run never publishes a GitHub Release.**

Only **Publish Final Audio Release** creates a release. It reads **exactly the MP3s already committed under /audio on main** and builds a ZIP with the MP3 files directly at its root. No manifest, directories, scripts, configuration, or other files are included. It requires audio/manifest.json and validates the MP3 checksums, speech inputs, effective processing settings, generator fingerprint, and announcement metadata against the current sources. The manifest is not included in the release ZIP.

The first release gets **v1.0.0** unless matching version tags already exist; subsequent releases increment the highest vMAJOR.MINOR.PATCH tag's **patch** number. For example, after v1.0.0, the next is v1.0.1. The release asset is named **ACARS-Announcements-v1.0.1.zip**. There is no version input required.

GitHub's Releases page also automatically shows built-in *Source code (zip/tar.gz)* links; those are provided by GitHub separately. The **ACARS-Announcements-vX.Y.Z.zip** asset is the MP3-only archive.

The release uses the specific committed main SHA reviewed at release time and will fail rather than package an uncommitted or changing set of recordings. Run it again after resolving any conflict. It does not generate new audio.

## Local build

Run these commands from the repository root. Use Python 3.12+ and FFmpeg/ffprobe with libmp3lame support. Internet access to Edge is needed only when speech must be synthesized:

    python -m pip install -r requirements.txt
    python tools/generate_audio.py --validate
    python tools/generate_audio.py

Validation detects duplicate IDs, duplicate filenames, invalid placeholders, missing speaker roles, unknown effects, voices absent from voices.json, unsupported MP3 sample rates/bitrates, invalid voice/audio settings, and unsafe filenames. Voice checking uses the committed catalog without a network call; refresh the catalog if a newly available voice is missing. Synthesis failures fail the action instead of uploading a partial pack. When run locally, final MP3s and the manifest are written to dist/audio/, the preview ZIP to dist/ACARS-Announcements-audio.zip, and clean speech to speech-cache/ at the repository root. Only the GitHub workflow copies finished recordings into /audio and commits them together with /speech-cache. Local runs also reuse the committed /audio recordings when they match.

## Limitations

This uses the unofficial [edge-tts](https://github.com/rany2/edge-tts) interface; availability and service behavior can change. Check licensing/redistribution terms before distributing recordings broadly. The scripts (including safety instructions) are intended for simulation, not actual aviation safety announcements. This repository generates sound packs but does not yet modify ACARS playback code.

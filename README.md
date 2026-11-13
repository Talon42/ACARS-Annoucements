# ACARS Announcements

This repository builds reusable Edge or Kokoro TTS cabin-crew and flight-deck audio for ACARS. All 16 supplied announcements are **fully generic and flight-independent**. ACARS already handles the playback triggers; this project handles generating and distributing the audio.

## Quick start

1. Edit [templates.json](templates.json) to change scripts, filenames, or individual voices; edit [config.json](config.json) for the TTS engine, role defaults, speed, volume, and the unified PA effect.
2. Commit changes to templates.json or config.json on **main** or **kokoro**, or manually run [Generate ACARS Audio](https://github.com/Talon42/ACARS-Annoucements/actions/workflows/generate-audio.yml) with the matching branch selected. It reuses unchanged recordings, generates only missing or changed speech, and **commits the final MP3s and manifest.json to [/audio](audio/) together with clean speech in [/speech-cache](speech-cache/)**. A successful generation also uploads a preview ZIP as a 30-day Actions artifact.
3. Open [/audio](audio/), listen to the MP3 files, and adjust settings and regenerate as many times as desired. Each successful run replaces the current /audio contents. Previous versions remain in Git history.
4. When satisfied, open [Publish Final Audio Release](https://github.com/Talon42/ACARS-Annoucements/actions/workflows/publish-final-audio.yml), select **Run workflow** on **main**, and run it. This is the **only** workflow that publishes a release.
5. The release workflow packages the currently committed MP3 files from /audio **without regenerating** them. It chooses the next version automatically (first v1.0.0, then v1.0.1, v1.0.2, etc.), creates the Git tag, and publishes the MP3-only ZIP under [Releases](https://github.com/Talon42/ACARS-Annoucements/releases).

**Important:** Let Generate ACARS Audio finish successfully and commit its files before running Publish Final Audio Release. Workflows serialize writes within each branch. Final releases remain main-only. Release validation also rejects audio that no longer matches the current inputs.

## Important files

| File | Purpose |
| --- | --- |
| [/audio](audio/) | Committed generated MP3s and manifest.json; review these before releasing |
| [/speech-cache](speech-cache/) | Clean speech keyed by text, voice, rate, pitch, and volume; reused across generations |
| [templates.json](templates.json) | Announcement text, stable IDs, filenames, role and per-announcement overrides |
| [config.json](config.json) | Engine selection, per-engine role voices, delivery, model assets, MP3 settings, and PA effect presets |
| [VOICES.md](VOICES.md) | Combined Edge/Kokoro voice names, gender, locale, and generator support |
| [voices.json](voices.json) | Machine-readable voice catalog |
| [tools/generate_audio.py](tools/generate_audio.py) | Validates scripts, synthesizes MP3, applies FFmpeg effects, packages audio |
| [tools/update_voices.py](tools/update_voices.py) | Updates the combined Edge and Kokoro catalog |
| [tools/kokoro_tts.py](tools/kokoro_tts.py) | Verifies/downloads pinned model assets and runs a reusable CPU synthesis worker |
| [Generate ACARS Audio workflow](.github/workflows/generate-audio.yml) | Selective generation, commit /audio and /speech-cache, and preview artifact |
| [Refresh TTS Voices workflow](.github/workflows/refresh-voices.yml) | Refresh both voice catalogs each Monday or on demand |
| [Publish Final Audio Release workflow](.github/workflows/publish-final-audio.yml) | Manual-only: create version/tag and MP3-only release ZIP |
| [tools/release_audio.py](tools/release_audio.py) | Validate and package the committed /audio recordings; never synthesizes audio |

## Adding or editing announcements

Each entry in the **announcements** array of templates.json represents one MP3. A simplified example:

    {
      "id": "boarding_welcome_fa",
      "title": "Boarding Complete / Welcome Aboard",
      "speaker": "flight_attendant",
      "text": "Ladies and gentlemen, welcome aboard. Thank you for flying with us.",
      "variables": [],
      "filename": "boarding_welcome_fa.mp3",
      "voice": null,
      "audio": {}
    }

All supplied announcements currently use role voices and global delivery settings (`"voice": null`, `"audio": {}`), including the global **+20%** rate. To customize *only* one recording, the generator also supports filename, voice, and audio overrides. For example:

    "filename": "welcome_message.mp3",
    "voice": "af_bella",
    "audio": {
      "rate": "+8%",
      "pitch": "+0Hz",
      "volume": "+0%",
      "effect": "medium"
    }

- **id** stays stable for ACARS trigger mapping even if you change the filename.
- **filename** must be a unique MP3 basename (no directories/slashes); you can name files as desired.
- **voice: null** inherits the voice for that speaker from config.json; otherwise specify a voice short name present in voices.json for the selected engine.
- **audio: {}** inherits rate/pitch/volume and the unified default PA effect. Override any subset of them individually.
- **speaker** can be captain (male default), copilot (male default), or flight_attendant (female default); other roles can be defined in config.json.
- **title** is a readable announcement name, included in the manifest. Stable IDs and filenames distinguish recordings even when titles match.
- **event** and **channel** are not needed by this generator and have been removed. Playback timing belongs to ACARS; PA processing is configured globally in config.json.
- **variables** must remain an empty array. This is a static, generic sound library. Dynamic placeholders are rejected by the generator.

To add a new announcement, duplicate an existing object, give it a unique **id** and **filename**, and update the text and other fields. No extra Python code or workflow changes are needed.

## Selecting the TTS engine

The **tts_engine** setting is at the top of config.json. Set it to **kokoro** or **edge**. This branch selects **kokoro** by default. Each role retains a voice for both engines, so switching that one setting selects the matching role defaults. With `"tts_engine": "kokoro"`, only the `roles.<role>.voices.kokoro` entries are active; the Edge entries are inactive alternatives. Validation and generation print the active engine and resolved voices before processing. The copilot voice is available for announcements assigned that role; the supplied scripts currently use captain and flight_attendant.

Kokoro runs locally on CPU through the pinned kokoro-onnx runtime. Model weights and voice assets are downloaded from the configured upstream release and verified against SHA-256 values in **kokoro**. They are cached in **.kokoro-models/**, excluded from Git, and cached between Actions runs. No API key or paid GPU is required. The GitHub Actions runner downloads assets only when missing; synthesis itself uses no remote speech endpoint.

The generator supports American and British English Kokoro voices. The combined catalog lists all voices in the pinned pack, with other languages marked as catalog-only. Edge retains its existing multilingual voice support.

For Kokoro, the global **+20%** rate maps to model speed **1.2**; supported rates are -50% through +100%. Pitch must remain **+0Hz** because this backend does not support Edge-style pitch offsets. Volume is applied to the clean waveform; settings below -100% are rejected. Edge keeps its own rate/pitch/volume controls. The PA effect is applied after either engine.

## Preview voices before generation

| Engine | Voice playground | What to try |
| --- | --- | --- |
| Edge | [Edge TTS web demo](https://huggingface.co/spaces/innoai/Edge-TTS-Text-to-Speech) (community hosted) | Paste a short announcement and select the exact Edge voice name from VOICES.md. |
| Kokoro | [Official Kokoro voice demo](https://huggingface.co/spaces/hexgrad/Kokoro-TTS) | Try Heart (`af_heart`), Michael (`am_michael`), Fenrir (`am_fenrir`), or another voice in the catalog. |

To compare with this config, use **+20% rate** for Edge or **1.2 speed** for Kokoro when the demo exposes that control. These sites preview clean speech; this repository adds its PA effect afterward. Demo voice availability and model/runtime versions can differ from the pinned generator, so choose a voice listed for the correct engine in [VOICES.md](VOICES.md). Hosted demos may have queues or usage limits.

## Default voice selections

| Speaker | Kokoro voice (selected) | Edge voice (retained) | Gender |
| --- | --- | --- | --- |
| captain | am_michael | en-US-AndrewNeural | Male |
| copilot | am_fenrir | en-US-BrianNeural | Male |
| flight_attendant | af_heart | en-US-EmmaNeural | Female |

These are defaults in `roles.<role>.voices.<engine>` in config.json, not mandatory choices. Each announcement can override **voice** independently; overrides must belong to the selected engine.

Open [VOICES.md](VOICES.md) to browse the available voices. Use [Refresh TTS Voices](https://github.com/Talon42/ACARS-Annoucements/actions/workflows/refresh-voices.yml) > **Run workflow** to update both sources; the weekly refresh runs on the default branch (both engines once these changes are merged). Select kokoro for a manual branch refresh. The catalog labels each voice by engine, gender, locale, and generator support. Kokoro names are read from the configured upstream voice pack; newly published model packs require updating the pinned asset settings before their voices appear.

## Current defaults and unified PA effect

The current config.json defaults are:

| Setting | Current value |
| --- | --- |
| TTS engine (`tts_engine`) | `kokoro` |
| Speaking rate (`tts_defaults.rate`) | `+20%` |
| Pitch (`tts_defaults.pitch`) | `+0Hz` |
| TTS volume (`tts_defaults.volume`) | `+0%` |
| Unified PA strength (`audio.default_effect`) | `medium` |
| MP3 sample rate (`audio.sample_rate_hz`) | `24000` Hz |
| MP3 bitrate (`audio.bitrate_kbps`) | `128` kbps |

Adjust rate, pitch, and volume in **tts_defaults** to change global speech delivery. Per-announcement audio overrides take precedence; the supplied templates currently have none.

The audio.default_effect setting selects one unified PA effect for all announcements. No channel setting is required. Available strength presets are:

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

The same preset system applies to every announcement. An announcement can select a different strength through its **audio.effect** override; there are no separate PA and interphone profiles. A limiter follows enabled processing. The supplied **off** preset bypasses effects, but the output is still encoded to the configured MP3 format.

Output MP3 sample rate and bitrate are adjustable via **audio.sample_rate_hz** and **audio.bitrate_kbps**. Validation checks supported settings before synthesis.

## Selective generation and speech reuse

Clean speech is cached by announcement text, resolved voice, rate, pitch, and volume, with a checksum for corruption detection. Kokoro keys additionally include the engine, voice language, pinned model/voice assets, dependency file, and synthesis helper fingerprint. Clean Edge speech is MP3; clean Kokoro speech is PCM WAV. Successful workflow runs commit this cache alongside /audio, so it persists between runners.

- An unchanged recording is copied byte-for-byte from committed /audio when its processing fingerprint and checksum match and its clean speech cache is intact.
- Changing only the PA effect, its strength/settings, sample rate, or bitrate reprocesses affected recordings from cached clean speech without calling a TTS engine. Recordings whose effective settings did not change retain their existing MP3s.
- Changing a role voice regenerates only announcements that resolve to that voice; explicit voice overrides are respected.
- Changing text regenerates only that announcement. Changing rate/pitch/volume regenerates only recordings whose resolved values changed.
- Renaming an output or editing its title does not require new speech. If the ID stays the same and processing is unchanged, the committed MP3 is reused.
- Missing or damaged clean speech is regenerated with the timeout/retry policy below. Unused cache entries are removed after a successful build.
- Changes to tools/generate_audio.py invalidate final MP3 processing fingerprints, so cached clean speech is reprocessed. They do not automatically require new speech. Changing Kokoro model assets, requirements.txt, or tools/kokoro_tts.py invalidates Kokoro clean speech too.

When clean speech is absent, it must be generated once; processed MP3s cannot serve as clean originals. Older manifests without fingerprints also require a generation run before release. Successful runs preserve the cache for subsequent builds. A failed run never replaces committed /audio. Release validation does not require the clean cache or call a TTS engine; it checks the finished pack against current inputs.

## Timeouts and retries

These settings are under **generation** in config.json:

| Setting | Current value | Behavior |
| --- | --- | --- |
| timeout_seconds | 10 | Maximum wait for each individual Edge TTS download attempt |
| kokoro_timeout_seconds | 300 | Maximum CPU synthesis wait per Kokoro announcement attempt, including first worker model load |
| max_attempts | 2 | One initial attempt and at most one retry |
| retry_delay_seconds | 10 | Wait before retrying a failed attempt |

Announcements are processed sequentially. If both attempts fail, generation aborts immediately without processing later announcements or uploading a partial preview. The Edge limit applies to downloads; the Kokoro limit applies to CPU synthesis. Kokoro asset downloads use a separate 60-second network socket timeout and checksum validation. A timed-out Kokoro worker is terminated before retrying, so synthesis attempts cannot overlap. Cached speech needs no TTS attempt. These are not whole-workflow time limits.

## Workflow triggers

- **Generate ACARS Audio:** runs for pushes to main/kokoro or pull requests that change templates.json, config.json, voices.json, requirements.txt, tools/generate_audio.py, tools/kokoro_tts.py, or its own workflow file. It can also be run manually on main or kokoro. Successful non-PR runs commit only to the branch that ran the workflow. Pull-request runs upload previews but do not commit audio or the cache to the repository.
- **Refresh TTS Voices:** runs each Monday at **10:25 UTC**, on demand, or when its script/workflow changes on main. It updates the combined Edge/Kokoro voices.json and VOICES.md when the catalog changes. Scheduled runs use main; manual runs update the selected branch.
- **Publish Final Audio Release:** manual-only, and requires main. It packages existing committed audio; it never synthesizes speech.
- A README-only edit does not trigger audio generation.

## Generated audio, preview artifacts, and finalized releases

After successful generation on main or kokoro, the workflow updates **/audio** and **/speech-cache**, creating a commit only when their contents changed:

    audio/
      boarding_welcome_fa.mp3
      boarding_welcome_captain.mp3
      ...
      deboarding_fa.mp3
      manifest.json

The manifest maps stable IDs to filenames, title, speaker, engine, resolved voice, rate/pitch/volume, and effect. It also stores fingerprints of speech inputs and processing settings/code, plus a checksum of each final MP3. Release validation compares these with the current sources and files, rejecting stale or modified audio even when filenames match. The workflow fully replaces /audio each time (so removing or renaming templates also removes obsolete MP3s). As a safety measure, it will not force-push if the target branch changed while audio was synthesizing.

Every successful generation also uploads a required 30-day preview artifact named **acars-announcements-audio**, containing a ZIP with manifest.json and audio/MP3 files. **A generation run never publishes a GitHub Release.**

Only **Publish Final Audio Release** creates a release. It reads **exactly the MP3s already committed under /audio on main** and builds a ZIP with the MP3 files directly at its root. No manifest, directories, scripts, configuration, or other files are included. It requires audio/manifest.json and validates the MP3 checksums, speech inputs, effective processing settings, generator fingerprint, and announcement metadata against the current sources, including engine/model inputs. The manifest is not included in the release ZIP.

The first release gets **v1.0.0** unless matching version tags already exist; subsequent releases increment the highest vMAJOR.MINOR.PATCH tag's **patch** number. For example, after v1.0.0, the next is v1.0.1. The release asset is named **ACARS-Announcements-v1.0.1.zip**. There is no version input required.

GitHub's Releases page also automatically shows built-in *Source code (zip/tar.gz)* links; those are provided by GitHub separately. The **ACARS-Announcements-vX.Y.Z.zip** asset is the MP3-only archive.

The release uses the specific committed main SHA reviewed at release time and will fail rather than package an uncommitted or changing set of recordings. Run it again after resolving any conflict. It does not generate new audio.

## Local build

Run these commands from the repository root. Use Python 3.12+ and FFmpeg/ffprobe with libmp3lame support. Linux installations should provide espeak-ng and libsndfile1 (the Actions workflow installs these). Internet is needed for dependency/model downloads, catalog refreshes, and uncached Edge speech; Kokoro synthesis is local:

    python -m pip install -r requirements.txt
    python tools/generate_audio.py --validate
    python tools/generate_audio.py

Validation detects duplicate IDs, duplicate filenames, invalid placeholders, missing speaker roles, unknown effects, voices absent from the selected engine catalog, unsupported Kokoro language/rate/pitch settings, unsupported MP3 sample rates/bitrates, invalid voice/audio settings, and unsafe filenames. Voice checking uses the committed catalog without a network call; refresh the catalog if a newly available voice is missing. Synthesis failures fail the action instead of uploading a partial pack. When run locally, final MP3s and the manifest are written to dist/audio/, the preview ZIP to dist/ACARS-Announcements-audio.zip, and clean speech to speech-cache/ at the repository root. Only the GitHub workflow copies finished recordings into /audio and commits them together with /speech-cache. Local runs also reuse the committed /audio recordings when they match.

## Limitations

The Edge option uses the unofficial [edge-tts](https://github.com/rany2/edge-tts) interface; availability and service behavior can change. Check licensing/redistribution terms before distributing recordings broadly. The scripts (including safety instructions) are intended for simulation, not actual aviation safety announcements. Kokoro model weights are Apache-2.0 licensed and kokoro-onnx is MIT licensed; retain the relevant notices when redistributing model/software assets. Voice quality varies, especially for very short phrases and long passages; audition the resulting recordings. This repository generates sound packs but does not yet modify ACARS playback code.


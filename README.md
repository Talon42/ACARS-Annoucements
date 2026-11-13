# ACARS Announcements

Generate 16 reusable cabin-crew and flight-deck MP3 announcements with **Kokoro** or **Edge TTS**. Scripts are static and flight-independent; ACARS controls when recordings play.

## Generate and review audio

1. Edit [templates.json](templates.json) for announcements and [config.json](config.json) for voices, speed, and PA effects.
2. Commit changes on **kokoro** or **main**, or run [Generate ACARS Audio](https://github.com/Talon42/ACARS-Annoucements/actions/workflows/generate-audio.yml) with the correct branch selected.
3. After the action succeeds, listen to the MP3s in [audio/](audio/). It also commits the manifest and [clean speech cache](speech-cache/) to that branch. The final audio folder is replaced, including removal of obsolete filenames.
4. Repeat as needed. Unchanged speech is reused automatically.

Each successful run uploads a 30-day preview artifact named **acars-announcements-audio**. Pull-request runs provide previews without committing generated files. README-only edits do not trigger generation.

## Announcement fields: templates.json

Each object in `announcements` produces one MP3:

```json
{
  "id": "boarding_welcome_fa",
  "title": "Boarding Complete / Welcome Aboard",
  "speaker": "flight_attendant",
  "text": "Ladies and gentlemen, welcome aboard.",
  "variables": [],
  "filename": "boarding_welcome_fa.mp3",
  "voice": null,
  "audio": {}
}
```

| Field | Meaning / accepted values |
| --- | --- |
| `id` | Unique, stable recording identifier. Use lowercase letters, digits, and underscores. Keep it unchanged when editing a script or filename. |
| `title` | Required readable name. Appears in the manifest; it is not spoken. Different recordings may share a title. |
| `speaker` | Role used to select the default voice: `captain`, `copilot`, or `flight_attendant`. Additional roles can be defined in config. |
| `text` | Required words to speak. Write the complete script; dynamic placeholders are unsupported. |
| `variables` | Leave as `[]`. These recordings do not substitute flight-specific values. |
| `filename` | Unique MP3 filename, compared without regard to case. Use letters, digits, dots, underscores, or hyphens; start with a letter/digit. No directories or `..`. If omitted, defaults to `<id>.mp3`. |
| `voice` | `null` inherits the speaker's voice for the active engine. A voice name overrides only this announcement and must belong to that engine in [VOICES.md](VOICES.md). |
| `audio` | `{}` inherits global settings. Optional overrides: `rate`, `pitch`, `volume`, and `effect`. |
| `note` | Optional editing/reference note. It is not spoken and does not affect audio. |

To add an announcement, copy an object and give it a unique `id` and `filename`. At the file's top level, keep `schema_version: 1` and `variables: {}`; `description` is informational and `announcements` contains the recordings. All supplied announcements currently inherit their voice and audio settings.

## Engine, voices, and global settings: config.json

**`tts_engine` at the top selects the active engine.** With `"tts_engine": "kokoro"`, only each role's `voices.kokoro` entry is active. Set it to `"edge"` to use `voices.edge`. Both sets remain available for switching; generation logs print the active engine and resolved voices.

| Role | Kokoro voice (active) | Edge alternative |
| --- | --- | --- |
| `captain` | `am_michael` | `en-US-AndrewNeural` |
| `copilot` | `am_fenrir` | `en-US-BrianNeural` |
| `flight_attendant` | `af_heart` | `en-US-EmmaNeural` |

Edit voices under `roles.<role>.voices.<engine>`. Role `gender` is informational; the selected voice determines the sound. The supplied scripts use captain and flight_attendant; copilot is available for new assignments.

| Config setting | Current value | Meaning |
| --- | --- | --- |
| `tts_engine` | `kokoro` | Active synthesis engine: `kokoro` or `edge`. |
| `tts_defaults.rate` | `+20%` | Global speaking speed. Kokoro maps this to speed 1.2 and accepts -50% through +100%. |
| `tts_defaults.pitch` | `+0Hz` | Pitch offset. Kokoro requires zero; Edge supports pitch offsets. |
| `tts_defaults.volume` | `+0%` | Voice volume adjustment. Kokoro rejects values below -100%. |
| `audio.default_effect` | `medium` | Global PA strength: `off`, `low`, `medium`, or `high`. |
| `audio.sample_rate_hz` | `24000` | Final MP3 sample rate in Hz. |
| `audio.bitrate_kbps` | `128` | Final MP3 bitrate in kbps. |
| `generation.timeout_seconds` | `10` | Edge download timeout per attempt, in seconds. |
| `generation.kokoro_timeout_seconds` | `300` | Kokoro CPU synthesis timeout per attempt, including first worker model load. |
| `generation.max_attempts` | `2` | Initial attempt plus one retry; allowed values are 1 or 2. |
| `generation.retry_delay_seconds` | `10` | Delay before retrying, in seconds. |

Rate and volume use signed percentages such as `+20%` or `-10%`; pitch uses signed Hz such as `+0Hz`. Announcement overrides take precedence over these global delivery/effect settings.

Announcements run sequentially. After the final failed attempt, generation stops immediately and leaves committed audio intact. A timed-out Kokoro worker is terminated before retrying.

Kokoro runs locally on CPU and supports American/British English in this generator. The `kokoro` config block pins the upstream release, model/voice filenames, and SHA-256 checksums; change these together when upgrading assets. Downloads use a separate 60-second socket timeout. Models are cached in `.kokoro-models/` and are not committed. Edge uses an online service and requires internet for uncached speech.

## Preview voices before generation

| Engine | Voice preview |
| --- | --- |
| Edge | [Community Edge TTS demo](https://huggingface.co/spaces/innoai/Edge-TTS-Text-to-Speech) |
| Kokoro | [Official Kokoro demo](https://huggingface.co/spaces/hexgrad/Kokoro-TTS) |

Use **+20% rate** for Edge or **1.2 speed** for Kokoro when available. Demos play clean speech without this project's PA effect and may differ in model version or available voices. Choose names from [VOICES.md](VOICES.md), which lists both engines and marks supported voices.

[Refresh TTS Voices](https://github.com/Talon42/ACARS-Annoucements/actions/workflows/refresh-voices.yml) updates **VOICES.md** and **voices.json** together. Select **kokoro** for a manual branch refresh. Scheduled refreshes run Mondays at **10:25 UTC** on the default branch; the combined updater applies there after merge. Kokoro's list follows the pinned voice pack, so a newer pack requires updated asset settings.

## PA effect controls

The same PA processing applies to every announcement. `off` bypasses effects; `low` is subtle, `medium` is the default, and `high` is stronger. To change one recording's strength, set its `audio.effect`.

Tune presets under `audio.effect_presets.<preset>`:

| Parameters | Control / disable |
| --- | --- |
| `highpass_hz`, `lowpass_hz` | Lower/upper frequency cutoffs in Hz. Set a cutoff to 0 to disable that filter. |
| `presence_hz`, `presence_gain_db` | Speech presence EQ frequency and gain. Set gain to 0 to disable it. |
| `compressor_threshold`, `compressor_ratio` | Compression trigger level and strength. Threshold is a linear level from 0 to 1. Set threshold to 0 or ratio to 1 to disable compression. |
| `compressor_attack_ms`, `compressor_release_ms`, `compressor_makeup` | Compression response times and output gain multiplier. |
| `crusher_bits`, `crusher_mix` | Bit depth and distortion blend. Lower bit depth gives stronger grit; mix 0 disables it. |
| `noise_amplitude`, `noise_mix` | Added white-noise level and blend. Set either to 0 to disable noise. |

Mix values run from 0 to 1. A limiter follows enabled processing; all outputs, including `off`, are encoded to the configured MP3 format.

## What gets regenerated?

| Change | Result |
| --- | --- |
| Nothing affecting audio | Reuse the finished MP3 when its checksum and clean cache are valid. |
| Text or resolved voice/rate/pitch/volume | Generate speech only for affected recordings. |
| PA settings, sample rate, or bitrate | Reprocess affected cached speech; no new TTS call. |
| Title or filename | No new speech. |
| Missing/damaged clean speech | Regenerate that speech. |
| Generator code | Reprocess cached speech. Kokoro model/runtime/helper changes may also require new speech. |

Clean speech lives in [speech-cache/](speech-cache/); final recordings and their source fingerprints/checksums live in [audio/](audio/). Removing announcements also removes obsolete outputs and unused clean cache entries after a successful build.

## Publish a release

After the desired changes are on **main** and generation has succeeded there, run [Publish Final Audio Release](https://github.com/Talon42/ACARS-Annoucements/actions/workflows/publish-final-audio.yml) on **main**.

It validates the committed recordings against the current inputs and manifest, then publishes **ACARS-Announcements-vX.Y.Z.zip** containing MP3s only, directly at the ZIP root. It never regenerates speech. Versioning starts at v1.0.0 and otherwise increments the highest version tag's patch number. Stale or modified audio must be rebuilt before release.

## Local generation

Requires Python 3.12+, FFmpeg/ffprobe with libmp3lame, and Linux libraries `espeak-ng` and `libsndfile1` (installed automatically in Actions). Run from the repository root:

```sh
python -m pip install -r requirements.txt
python tools/generate_audio.py --validate
python tools/generate_audio.py
```

Local outputs: MP3s/manifest in `dist/audio/`, preview ZIP at `dist/ACARS-Announcements-audio.zip`, and clean speech in `speech-cache/`. The workflow copies final outputs into committed `audio/`. Validation checks inputs without downloading models or generating speech.

For simulation use. Edge uses the unofficial edge-tts interface; service availability can change. Kokoro model weights are Apache-2.0 licensed and kokoro-onnx is MIT licensed.

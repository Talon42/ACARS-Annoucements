# ACARS Announcements

Reusable, flight-independent cabin-crew and flight-deck announcements for ACARS. The canonical source is [`templates.json`](./templates.json), converted from the original supplied text and updated to use only **generic, pre-recordable speech**.

## What is included

There are 16 uniquely identified announcements across nine event groups. Each one is fully written: **no variable substitution, airline names, destinations, flight numbers, time-of-day selections, or aircraft-specific values are required**.

Each `announcements[]` entry has:

- `id`: stable identifier for the recording and eventual filename.
- `event`: logical trigger group.
- `title`: original script section for organization; not spoken.
- `speaker`: `flight_attendant` or `captain`.
- `channel`: `passenger_pa` for cabin announcements or `crew_interphone` for internal calls.
- `text`: the complete sentence(s) to synthesize into audio.
- `variables`: an empty array for every recording; retained for JSON format compatibility.
- `note` (optional): sequencing or audience guidance; not spoken.

The top-level `variables` object is empty by design. `schema_version` remains `1` because the same general data structure is retained.

## Edge TTS voices

`voice_roles` defines the intended Edge TTS voice for each speaker (currently `en-US-JennyNeural` for a flight attendant and `en-US-GuyNeural` for a captain), plus rate and pitch. These settings can be changed separately from the announcement scripts.

## Passenger PA vs. crew interphone

Three announcements have `channel: "crew_interphone"`. They are **not** passenger PA announcements. Your ACARS implementation should respect the channel when mapping these recordings to existing triggers.

`note` fields provide sequencing context (for example, an acknowledgement after a crosscheck), but they are not to be synthesized.

## Safety briefing

The generic safety briefing avoids specifying an emergency-exit count, exit arrangement, or life-vest placement. Instead it directs passengers to the aircraft-specific safety card and crew instructions. This is intended for flight-simulator immersion; it is **not** a certified safety briefing for real-world aviation operations.

## Planned audio build pipeline

A future GitHub Actions workflow can read `templates.json` and generate exactly one recording per ID, using the appropriate speaker voice. Since every script is static, it can generate all recordings once, regenerate only changed recordings, and distribute a reusable audio ZIP for ACARS to play locally.

**This repository currently contains the source templates only. No audio-generation workflow, produced MP3 recordings, or published audio pack is included yet.**

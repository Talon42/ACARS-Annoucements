# ACARS Announcements

Source library for spoken cabin-crew and flight-deck announcements. The canonical source is [`templates.json`](./templates.json), converted from the supplied `scripts.txt` on November 13, 2026.

## Format

- `schema_version`: version number for consumers of this JSON structure.
- `voice_roles`: default Edge TTS voice and delivery options for the `flight_attendant` and `captain` roles. These are editable defaults, not guaranteed voice availability.
- `variables`: descriptions of dynamic speech values required by templates.
- `announcements`: one entry per recording with a stable `id`, a logical `event`, the original section `title`, a `speaker`, `channel`, `text`, and a list of `variables`.
- `note` (optional): sequencing or presentation guidance, **not** text to synthesize.

### Example

```json
{
  "id": "boarding_welcome_fa",
  "event": "boarding_complete",
  "title": "Boarding Complete / Welcome Aboard",
  "speaker": "flight_attendant",
  "channel": "passenger_pa",
  "text": "Good {{time_of_day}} ladies and gentlemen...",
  "variables": ["time_of_day", "airline_name", "flight_number", "destination", "captain_name"]
}
```

The JSON identifiers are **proposed stable announcement IDs**, not verified mappings to triggers in the existing ACARS app. The app's trigger IDs can be mapped separately without changing the spoken text.

## Passenger vs. crew playback

`channel: passenger_pa` indicates an announcement heard in the cabin. `channel: crew_interphone` indicates a crew-only/internal call. Three entries are crew-interphone messages. Their `note` fields indicate when they should play.

Do not synthesize `title`, `note`, or `variables`; only the resolved `text` is spoken.

## Dynamic fields

Tokens follow the `{{snake_case}}` convention. Examples include:

- `{{airline_name}}` and `{{flight_number}}`
- `{{destination}}`, `{{arrival_time}}`, and `{{gate_number}}`
- `{{emergency_exit_count}}`, `{{emergency_exit_locations}}`, and `{{life_vest_location}}`

**Do not send unresolved placeholders to a text-to-speech service.** The generation pipeline should validate that every token in a selected announcement has a spoken value, or skip that announcement with a clear message.

A flight-independent announcement (no entries in `variables`) can be generated once and reused. Flight-specific announcements must be rendered with a supplied value set (for example, a destination and flight number), or generated later as the user selects a flight. Because each flight can differ, a pre-rendered sound pack cannot cover unlimited dynamic values.

Aircraft-specific safety information must be checked against the aircraft before producing a briefing. The source text has not been verified for regulatory accuracy or rewritten beyond structural cleanup and removal of one stray text artifact.

## Planned generation workflow

The next layer will read `templates.json`, resolve variables, select the voice for each speaker, synthesize audio via Edge TTS, and publish files using their stable announcement IDs. A GitHub Actions workflow can do this on a manual run or after a script change.

No audio generation workflow is included yet, and this repository does not currently publish MP3 files.

# Anki Deck Spec

## Deck Metadata
- deck_name: [replace]
- source_mode: domain
- card_type: term
- output_file: [replace].apkg

## Card Policy
- style_profile: concise
- strict_precise_mode: true
- generation_notes: [replace]

## Field Schema
| field | required | description |
| --- | --- | --- |
| id | yes | Stable card id |
| note_type | yes | term/language/qa |
| front | yes | Front side text |
| back | yes | Back side text |
| context | no | Topic cue shown with front |
| example | no | Example sentence or use case |
| extra | no | Additional explanation |
| tags | no | Comma-separated tags |

## Cards
| id | note_type | front | back | context | example | extra | tags |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | term | [replace] | [replace] | [replace or blank] | [replace or blank] | [replace or blank] | [comma,separated,tags] |

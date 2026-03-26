# Anki Deck Spec

## Deck Metadata
- deck_name: Biology Basics
- source_mode: domain
- card_type: term
- output_file: biology-basics.apkg

## Card Policy
- style_profile: concise
- strict_precise_mode: true
- generation_notes: Focus on foundational biology concepts.

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
| 1 | term | What organelle produces ATP in eukaryotic cells? | Mitochondria. | Biology: Cells |  | Main site of aerobic respiration. | biology,cell |
| 2 | term | Which structure contains most genetic material in eukaryotic cells? | Nucleus. | Biology: Cells |  | Houses most nuclear DNA. | biology,cell |

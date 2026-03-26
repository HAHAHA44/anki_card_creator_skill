# Anki Deck Spec

## Deck Metadata
- deck_name: Planetary Motion QA
- source_mode: extract
- card_type: qa
- output_file: planetary-motion-qa.apkg

## Card Policy
- style_profile: concise
- strict_precise_mode: true
- generation_notes: Focus on precise astronomy recall.

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
| 1 | qa | What force keeps planets in orbit around the Sun? | Gravity. | Astronomy: Orbital Mechanics |  | Specifically the Sun's gravitational attraction. | astronomy,orbit |
| 2 | qa | Why do planets move faster when they are closer to the Sun? | Because conserving angular momentum leads to higher orbital speed near perihelion. | Astronomy: Orbital Mechanics | This pattern appears in elliptical orbits. | Related to Kepler's second law. | astronomy,kepler |
| 3 | qa | What is the name of the closest point of a planet's orbit to the Sun? | Perihelion. | Astronomy: Orbital Mechanics |  | The farthest point is aphelion. | astronomy,orbit |

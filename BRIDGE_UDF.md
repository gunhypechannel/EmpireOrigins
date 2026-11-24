# Empire Origins → Ultra Deep Field bridge

Empire Origins (EO) is **the last Eclipse**; Ultra Deep Field (UDF) is **the next one**. EO follows every rule in the UDF story handoff: Wardens not invaders, the Unmade never seen, the Advisor as the heart, the Hive as the only villain, and shared, remembered results.

## How the canon maps into Empire Origins
| UDF canon | In Empire Origins |
|---|---|
| Architects' prison, pyramid stations | The Ancient Pyramid is a piece of it. The "alien" sites and the Ancient Guardians are the Architects'. |
| The Pentarch (5 seals) | Seal of Flame (Great Lighthouse, Ignaroth), Light (Great Library, Auricor), Roots (Hanging Gardens, Viridrax), Storms (Bronze Colossus, Voltaris), Void (Great Sphinx, Gravemorn). Each has a strength from 0 to 100%. |
| Wardens | Every non-beast boss. Killing one weakens the nearest seal (by 3, or 6 for the weekly boss) and drops **Warden Hearts** (the top hitter gets 2; anyone with at least 10% of the damage gets 1). |
| Titan Cores | Warden Hearts (`mat_warden`) forge the Warden-forged set: Wardenheart Blade, Aegis of the Outer Wall, Architect's Circlet, Ring of the Five Seals, Echo Stone Amulet. |
| The Hive / Vael'Khor | The Brood (Brood Matriarch, pods). Rival camps within 14 tiles of a wonder are Hive cultists. Beating either strengthens the nearest seal (+8 for the Brood, +5 for a camp). |
| The Advisor | **Echo Stones**: the 9 obelisk landmarks hold her recordings (Kokoro bf_emma with a stone-echo effect). She calls the player "Founder". The 10th recording, "Take Me With You", waits in the pyramid's heart until the Space Age. The hero (still the only guide) answers each recording. Hearing all 10 gives the title "Keeper of the Echo" and 1 Warden Heart. During the Dark Hour and on ledger results, she speaks live "from the pyramid". |
| The Ten Seals | **The First Eclipse**: the same 10 chapters. Each one runs the week **before** its UDF echo, starting Monday 18 Jan 2027 (00:00 UTC), the week before UDF's first Ten Seals finale, and repeating every 28 days; the year repeats after 10 chapters. The chapter's Warden becomes the Weekly Boss. If it falls that week the seal **holds** (+20); otherwise it **cracks** (−25). |
| The Eclipse | **The Dark Hour**: each chapter's Saturday, 18:00–20:00 UTC. The map goes dark. |
| Concord descends from the survivors | The Space Age record "Beyond the Stars" links to UDF. |

EO chapter Wardens: 1 Ancient Guardians · 2 OMEGA‑0, the First Cube · 3 the Elemental Sovereigns / Convergence · 4 Brood Matriarch · 5 Buried Colossus · 6 Event Horizon Wyrm · 7 Shard Colossus · 8 Morvath, the Hollow King · 9 Eryndor, the Gate Sovereign · 10 Solkaris, the Sun Devourer.

## The cross-game hook (UDF side still to build)
The "Continue in Ultra Deep Field" button opens:

`https://gunhypechannel.github.io/Ultradeepfield/?eo=EO1-HC-H-------a8aaa`

- `EO1-`: the format version.
- 10 characters, one per chapter of the current cycle: `H` held, `C` cracked, `-` not played yet.
- `-`, then 5 base-36 digits: the seal strengths ÷ 10 (0 to `a`), in the order flame, light, root, storm, void.

UDF can read `?eo=`, store it, and let the Advisor open with "In the age of empires, the Seal of Flame held…". She recognises the Founder she spoke to through the stones.

Code: `deep.js` (all of the above), plus hooks in `p70.py` (`bossDefeated`, `trackReport`), `bossdeploy.js` (chapter Warden as the weekly boss), `tapfix.js` (tapping Echo Stones) and `quickfinder.js` (an Echo Stones category). World state is kept in engine meta `deep`; player echo progress is the `eo.echo` key in the cloud save.

## Echo calendar (v140)

EO now runs on UDF's v737 clock (`echo.js`, computed, so no live sync is needed):
- Wed 18:00 → Fri 18:00 UTC: **Sky Omen**, the echo of that week's UDF rotation (Falling Star, Elemental Gathering, Ruin Wind, Stuttering Sun, Trial at the Gate, Stone Gaze). None in UDF's prologue.
- Fri 18:00 → Sun 18:00: **Battle for the Monolith**.
- Sun 18:00 → Mon 18:00: EO's own festival.
- Mon 18:00 → Wed 18:00: **Echo Hunt** of the next UDF boss (Overlord→Guardians of the Black Pyramid, Devourer→Marsh Devourer, Leviathan→Great Sea Serpent, Colossus→Crystal Colossus, …). Beating the Omen boss counts triple.
- **Echo Seasons** mirror UDF seasons: points from every event, 4 chests (10/25/45/70), op `echoSea`.
- Dec 7, 2026 is UDF's prologue (Season of the Countdown). Season of the Cube starts Feb 1, 2027; Season of the Mimic Apr 26, 2027.
- **Still needed on the UDF side:** reading `?eo=EO1-…` codes.

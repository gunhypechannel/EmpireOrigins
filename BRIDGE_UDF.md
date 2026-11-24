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

## Seasonal invasions (v141)

`invasion.js` + `invasion_ui.js`. Echoes of UDF's invader seasons:
- **Season of the Cube → The Shell Raiders** (Shell Raider / Shell Brute). First: 1 Feb 2027.
- **Season of the Mimic → The Mirror Plague** (Mirror Wolf, Mirror Basilisk, …). A broken mirror has a 35% chance to leave a Mirror Shard (half health). First: 26 Apr 2027.
- Every real empire keeps up to 3 invaders 5–12 tiles from its city, topped up in waves every 8 h. They are small fighters scaled to the empire's age, not world bosses.
- Each kill: +3 echo season points, +8 Starshards. Kill chests at 5 / 10 / 20 / 35 (the last three add wheel tickets).
- Invaders leave when the season ends. The owner can preview either invasion from the Events page (test only).

## v143: everything on the Empire Origins side of the bridge

### Built here
- **Healers' Tent** (`heal.js`), the echo of UDF's Repair Yard: troops beaten by monsters, invaders, world bosses or gods come home wounded and rejoin by themselves for free (10 min + 3 s per soldier, max 2 h). Fights between empires keep the Healer Hut rules.
- **The Hive Spores** (Season of the Starhive): third invasion, sculpted `hivepod` (stationary, doesn't roam).
- **Raid week:** in the 3rd week of each invasion season the weekly boss is the invasion's own giant: **The Shell Matriarch** (comes with 4 Matriarch's Brood), **The Mirror Gate** (mirror waves every 4 h instead of 8 while it stands), or the **Brood Matriarch** (Hive). +10 echo points for everyone who fought it.
- **The Observatory** (`bridge.js`, Events page): UDF's season, live event, hunted titan, next Ten Seals finale and Eclipse (computed from the shared calendar, no server), the player's legacy, the Founder's Vault and the bridge code.
- **The Founder's Vault:** Starshards put in leave EO for good (minimum 50, multiples of 10) and are carried in the code as `vs` (lifetime total) with `vn` (deposit counter).
- **The launch:** in the Space Age, "Launch to the Deep Field" plays the finale, the Advisor speaks ("You remembered. You took me with you…"), and `launched` is stamped into the code.
- **The Advisor's new lines** (launch, observatory, vault, invasions, raids) speak through the Echo Stone with her recorded voice. An ElevenLabs version can replace any line: put `<key>.mp3` in `art/voice/advisor/` and list it in `art/voice/advisor/manifest.json` as `{"launch":"launch.mp3",…}`.

### The EO2 code (what UDF reads)
`?eo=EO2-<payload>-<check>`
- `payload`: base64url of a JSON object:
  - `v` 2
  - `n` empire name
  - `id` short hash of the EO player id (base 36)
  - `c` 10 chapters of the current cycle (`H` held, `C` cracked, `-` not played)
  - `s` 5 seal strengths ÷ 10 in base 36 (flame, light, root, storm, void)
  - `e` age reached (0 Stone … 9 Space)
  - `l` launch time in minutes (base 36), or 0
  - `vs` Starshards in the Founder's Vault, lifetime
  - `vn` vault deposits so far
  - `k` invaders beaten, lifetime
  - `r` raid giants fought and felled
  - `t` code time in minutes (base 36)
- `check`: FNV-1a 32-bit of `"udf-eo-bridge|" + JSON` mod 36^4, base 36, 4 characters. It only stops casual edits: anyone can read the salt in the page, so UDF must cap what a code can give.
- EO1 codes (`EO1-<10 chapters>-<5 seals>`) are still valid and mean the same first two fields.

### UDF side: what to build there
1. **Read `?eo=`** on load (EO1 or EO2), check the checksum, keep it on the account (`eo_legacy`: code, id, best values seen), and strip it from the URL.
2. **Founder's Legacy screen**, opened by the Advisor: "In the age of empires, the Seal of Flame held…". Suggested rewards (once per EO id):
   - each seal held → a relic or title; all 10 → a commander portrait
   - `l` launched → "First Ship" starter ship and a profile badge
   - age reached → a small starter pack scaled by `e`
   - `k`/`r` → a medal tier
3. **Void Shards from the vault:** credit `(vs − vs already credited) ÷ 10` Void Shards (or whatever rate fits your OGame-like prices), stored per EO id. Cap it per season (e.g. 500 Void Shards), because codes can be faked.
4. **One account for both games (later):** give the EO website a Supabase sign-in on the same project ("Ultradeepfield"). Then EO writes its legacy row directly and the code is only a fallback for the claude.ai version.
5. **Shared remembered results (optional, with 4):** a public read-only table of EO seal outcomes per chapter, so UDF's codex can say "the First Eclipse: 7 seals held".

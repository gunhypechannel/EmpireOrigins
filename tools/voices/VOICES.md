# Hero voices (ElevenLabs)

Hypatia was remastered in v144. Each hero gets their own UDF-style wording and an ElevenLabs voice. The game swaps the words through `window.EOHEROLINES[hero]` (old shared line → that hero's line) and plays `art/voice/<hero>.mp3` / `.json` (clips indexed by the FNV key of the whole new line).

| Hero | Voice | Model | Status |
|---|---|---|---|
| Hypatia | Tamsin (`dAlhI9qAHVIjXuVppzhW`) | eleven_v4 | done (464 lines) |
| Imhotep, Tiberius, Oren, Ysolde, Brenna | pick one each | eleven_v4 | to do |

## Doing the next hero
1. Write `<hero>_lines.py` the way `hyp_lines.py` is written (regex of the shared line → the hero's line, `{n}` carries a building name). Check that every line in `vlines5.json` matches a rule, and keep the total near 30,000 characters.
2. Group the lines about 1,700 characters at a time, joined with ` [pause] `. Generate each group with the ElevenLabs connection (`creative_generate_speech`, eleven_v4, one take). `[pause]` is the cheapest separator that leaves a clear gap.
3. Join every group into one audio asset in the ElevenLabs sandbox (`ffmpeg -f concat -c copy`), with the duration of each part. Fetch the asset's preview URL in the Claude browser pane on elevenlabsusercontent.com and save it to Downloads, then stage it here.
4. Run `hyp_split.py` (cuts by the known durations, then the gaps) and `hyp_dp.py` (re-cuts each group by matching gaps against the expected length of each line). Check the reported outliers.
5. Pack the clips into `art/voice/<hero>.mp3` / `.json`, add the hero's map to `herolines.js`, bump `VV` in `advisers.js`, and deploy.

Credits: ElevenLabs flows charge about 1 credit per character for every model. The Creator plan gives 131,000 a month.

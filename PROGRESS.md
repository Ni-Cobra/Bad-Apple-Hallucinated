# PROGRESS.md — Production status tracker

**Update this file after every completed unit of work.** A fresh session reads this
first (see PROJECT.md §12) to know exactly where to resume. Trust the frames on
disk over this file: if a scene is marked done, verify its frame range exists
before building on it; if work exists that isn't logged here, log it.

## Phase 1 — Shared asset library

- [ ] Parametric figure toolkit (`assets/shapes.py`)
- [ ] Recurring characters (Reimu ×2 designs, Marisa, Yukari)
- [ ] All boundary handoff shapes (enumerated from SCENES.md transitions)
- [ ] Shared props (apple, broom, parasol/scythe)
- [ ] Contact-sheet helper (`tests/contact_sheet.py`, see PROJECT.md §12)
- [ ] Visual preview verified (`frames/_assets_preview/`)

## Phase 2 — Scenes (chronological order; done = passes the recognizability QC of
PROJECT.md §9 step 4 within its iteration cap; use Notes to flag cosmetic leftovers
for the optional end-of-project polish pass)

| # | Scene | Frames | Status | Notes |
|---|---|---|---|---|
| 1 | scene_01_loop_reveal | 0–120 | todo | |
| 2 | scene_02_reimu_apple | 120–450 | todo | |
| 3 | scene_03_marisa_flight | 450–855 | todo | |
| 4 | scene_04_patchouli | 855–1080 | todo | |
| 5 | scene_05_remilia | 1080–1275 | todo | |
| 6 | scene_06_sakuya | 1275–1500 | todo | |
| 7 | scene_07_flandre | 1500–1710 | todo | |
| 8 | scene_08_youmu | 1710–1920 | todo | |
| 9 | scene_09_yuyuko | 1920–2130 | todo | |
| 10 | scene_10_komachi | 2130–2370 | todo | |
| 11 | scene_11_eiki_split | 2370–2526 | todo | |
| 12 | scene_12_mokou | 2526–2790 | todo | |
| 13 | scene_13_keine_spin | 2790–2970 | todo | |
| 14 | scene_14_eirin_moon | 2970–3150 | todo | |
| 15 | scene_15_kaguya_whiteout | 3150–3363 | todo | |
| 16 | scene_16_prismriver | 3363–3570 | todo | |
| 17 | scene_17_chen_ran_tewi | 3570–3660 | todo | |
| 18 | scene_18_reisen | 3660–3750 | todo | |
| 19 | scene_19_momiji_leaves | 3750–3810 | todo | |
| 20 | scene_20_sanae | 3810–3930 | todo | |
| 21 | scene_21_hina | 3930–3990 | todo | |
| 22 | scene_22_kanako_suwako | 3990–4230 | todo | |
| 23 | scene_23_yukari | 4230–4410 | todo | |
| 24 | scene_24_tenshi | 4410–4650 | todo | |
| 25 | scene_25_aya | 4650–4830 | todo | |
| 26 | scene_26_suika | 4830–5040 | todo | |
| 27 | scene_27_alice | 5040–5220 | todo | |
| 28 | scene_28_nitori_splash | 5220–5430 | todo | |
| 29 | scene_29_yuka_petals | 5430–5610 | todo | |
| 30 | scene_30_elly | 5610–5850 | todo | |
| 31 | scene_31_crown_splash | 5850–5970 | todo | |
| 32 | scene_32_pc98_reimu | 5970–6090 | todo | |
| 33 | scene_33_reach | 6090–6270 | todo | |
| 34 | scene_34_yinyang | 6270–6420 | todo | |
| 35 | scene_35_finale | 6420–6570 | todo | |

## Phase 3 — Integration & final encode

- [ ] Frame census (0–6569, no gaps/dupes)
- [ ] Boundary continuity audit (34 boundaries)
- [ ] Polarity audit
- [ ] Spot-check vs `_ref_frames/`
- [ ] Encode + ffprobe verification (6570 frames, 219.0 s, no audio)
- [ ] Loop check (first frame == last frame == solid black)
- [ ] Final watch-through

## Session log

| Date | What was done | Where it stopped / next step |
|---|---|---|
| 2026-06-13 | Preparation complete (TOOLING.md, SCENES.md, PROJECT.md, toolchain verified) | Next: Phase 1 asset library |

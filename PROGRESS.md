# PROGRESS.md — Production status tracker

**Update this file after every completed unit of work.** A fresh session reads this
first (see PROJECT.md §12) to know exactly where to resume. Trust the frames on
disk over this file: if a scene is marked done, verify its frame range exists
before building on it; if work exists that isn't logged here, log it.

## Phase 1 — Shared asset library  ✅ DONE (2026-06-13)

- [x] Parametric figure toolkit (`assets/shapes.py`) — geometry helpers
      (circle/ellipse_poly, ribbon, mirror, transform/draw_polys), figure parts
      (head, dress_body, limb, reimu_bow, detached_sleeve, witch_hat, mob_cap,
      long_hair, ponytail)
- [x] Recurring characters: `reimu_back`, `reimu_front` (neutral/apple/wind),
      `reimu_hairdown`, `marisa_broom`, `marisa_hat`, `yukari`
- [x] Boundary handoff shapes — the major morph-chain shapes are in the library:
      apple, apple_core, broom, sakura_petal, moon, leaf_maple/ginkgo, fan_open,
      parasol, scythe, teacup, knife, rod_of_remorse, pen, gourd, drop, doll,
      gap_sukima, sdm_skyline, crown_splash, draw_stars, draw_yinyang.
      NOTE: a few scene-pair-specific micro-handoffs (raised finger 4→5,
      knife-tip→wing-prong 6→7, water-column 31→32) are deferred — add them to
      `shapes.py` when authoring those scene pairs so both sides share one shape
      (the library is intentionally extensible; §6 rule 2 still honoured).
- [x] Shared props (apple, broom, parasol, scythe) — included above
- [x] Contact-sheet helper (`tests/contact_sheet.py`, see PROJECT.md §12) +
      scratch preview `assets/_preview.py`
- [x] Visual preview verified (`frames/_assets_preview/assets_contact.png`) —
      all 29 silhouettes read clearly; 1 fix pass (ginkgo + petal notch)

## Phase 2 — Scenes (chronological order; done = passes the recognizability QC of
PROJECT.md §9 step 4 within its iteration cap; use Notes to flag cosmetic leftovers
for the optional end-of-project polish pass)

| # | Scene | Frames | Status | Notes |
|---|---|---|---|---|
| 1 | scene_01_loop_reveal | 0–120 | **done** | 120 frames; solid-black→back-view Reimu reveal; f0/f15 black verified; B-on-W; encoded+ffprobed OK. No fix passes needed. Loop-apple-in-hand detail intentionally omitted (back view; LOW-CONF per §10) |
| 2 | scene_02_reimu_apple | 120–450 | **done** | 330 frames; back-view→turn→front dance, apple in hand, near-bite ~f241, wind-up spin ~f330, toss; apple alone airborne at (540,140) by f436. B-on-W. No fix passes. Turn-around is a horizontal squash (recognizable, not literal 3D). |
| 3 | scene_03_marisa_flight | 450–855 | **done** | 405 frames; W-on-B starfield; Marisa catches apple, flies R→L, SDM skyline rises lower-left (~f721, matches ref), eats apple, drops core which falls+bounces alone (~f811); core handed off at (480,430). No fix passes. |
| 4 | scene_04_patchouli | 855–1080 | **done** | 225 frames; apple_core→Patchouli grow-morph (flip to B-on-W), dance w/ extended arm ~f961, raised wagging-finger close-up to end (~f1051). Patchouli built inline from toolkit (mob cap+long hair+robe). No fix passes. Front view (not profile) at the finger close-up — LOW-CONF cosmetic per §10. |
| 5 | scene_05_remilia | 1080–1275 | **done** | 195 frames; finger close-up (Scene 4 handoff)→Remilia, scalloped bat wings spread ~f1111, turn-to-profile (h-squash idiom) holding teacup out ~f1214, drops it; cup still falling on-screen at f1274 (~(240,580)) for the 5→6 shatter-flip. B-on-W. 1 fix pass. Added `raised_finger`/`bat_wing` to shapes.py. |
| 6 | scene_06_sakuya | 1275–1500 | **done** | 225 frames; W-on-B (flip at the teacup shatter). Cup hits→white shards scatter ~f1291, one→top-down twirl w/ arms+apron-ribbon ~f1336 ("not Rumia"), lands as frontal maid (frilly headdress+braids) ~f1381, 3/4-turn knife throw ~f1441; hero knife ends isolated upper-right, tip at (660,180) for 6→7 prong morph. 1 fix pass. Shards stay lower-left (cosmetic). |
| 7 | scene_07_flandre | 1500–1710 | **done** | 210 frames; knife (tip 660,180)→`crystal_wing` prongs emerge ~f1516, Flandre unfolds w/ crystal wings + side ponytail, arms spread + open hands ~f1591; hard inversion flash at local f120 (W-on-B→B-on-W); white blade-slash sweeps across chest ~f1666 and holds to end. No fix passes. Added `crystal_wing` to shapes.py. Grin (face-internal) omitted — not silhouette-visible (LOW-CONF cosmetic). 7→8 handoff: blade across chest, B-on-W (Youmu's sword; Scene 8 flips back to W-on-B). |
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
- [ ] Encode + ffprobe verification (6570 frames, 219.0 s, + original PV audio muxed via `encode.py`; `assets/badapple_audio.mp3`, AAC 192k, `-shortest`)
- [ ] Loop check (first frame == last frame == solid black)
- [ ] Final watch-through

## Session log

| Date | What was done | Where it stopped / next step |
|---|---|---|
| 2026-06-13 | Preparation complete (TOOLING.md, SCENES.md, PROJECT.md, toolchain verified) | Next: Phase 1 asset library |
| 2026-06-13 | Phase 1 complete: `assets/shapes.py` (toolkit + 6 recurring chars + ~20 handoff/prop shapes), `tests/contact_sheet.py`, preview verified (1 fix pass) | Next: Phase 2 scenes from #1 in chronological batches |
| 2026-06-13 | Scene 1 authored, QC'd, and encoded as a partial preview (`output/badapple.mp4`, 120 frames / 4.0 s, ffprobe-verified, no audio). Gapless prefix 0–119. | **Resume at Scene 2** (`scene_02_reimu_apple.py`, f120–449): Reimu dances B-on-W, near-bite ~f241, wind-up ~f361, tosses apple skyward (apple alone airborne by ~f436); the 2→3 polarity flip happens on the catch (Scene 3 starts already inverted). Use `reimu_front(pose='apple'/'wind')` + `apple()` from shapes.py. START A FRESH SESSION (§12). |
| 2026-06-13 | Scenes 2, 3, 4 authored + QC'd (one contact sheet vs refs, all beats recognizable, no fix passes). Frame census 0–1079 gapless. Re-encoded partial preview `output/badapple.mp4` (1080 frames / 36.0 s, ffprobe-verified, no audio). Handoffs verified: apple→(540,140) for 2→3 catch-flip; apple_core→(480,430) for 3→4 morph-flip. | **Resume at Scene 5** (`scene_05_remilia.py`, f1080–1274): finger→Remilia (mob cap w/ ribbon, short hair, scalloped bat wings ~f1111), holds teacup out (~f1201) and lets it drop; teacup `shatter` = the 5→6 polarity inversion (Scene 6 Sakuya starts W-on-B). Shared handoffs: author the finger 4→5 micro-shape in shapes.py; use `teacup()` (5→6). Build Remilia inline from the toolkit (`mob_cap`, scalloped wings). START A FRESH SESSION (§12). |
| 2026-06-13 | Scenes 5, 6, 7 authored + QC'd (contact sheets vs refs; 1 fix pass each on 5 & 6, none on 7). Added shared shapes to `assets/shapes.py`: `raised_finger` (4→5), `bat_wing` (Remilia), `crystal_wing` (6→7) — self-check OK (29 builders). Boundary chain verified: finger→Remilia; teacup-shatter FLIP→Sakuya (W-on-B); knife tip (660,180)→Flandre prongs (no flip); Flandre mid-scene FLIP at local f120 (W-on-B→B-on-W). Frame census 0–1709 gapless, no dupes. Re-encoded partial preview `output/badapple.mp4` = 1710 frames / 57.000 s, ffprobe-verified (960×720, 30/1, no audio). | **Resume at Scene 8** (`scene_08_youmu.py`, f1710–1919): 7→8 FLIPS BACK to W-on-B — Scene 7 ended B-on-W with the white blade-slash across Flandre's chest; that blade is Youmu's sword, so Scene 8 opens W-on-B continuing the cut. Youmu (two katana, the Roukanken/Hakurouken crossed at her back) does a chiburi + sheathes; half-bloomed Saigyou Ayakashi cherry tree (one side bare branches / one side dense bloom) dominates; Yuyuko small in left bg from ~f1801. 8→9 handoff: viewpoint rotates Youmu→Yuyuko beside the tree. Use `sakura_petal` (drifting petals) from shapes.py; build the cherry tree inline (or add a shared `cherry_tree`/`bare_branches` shape — Scene 9 also has the tree/petals). START A FRESH SESSION (§12). |
| 2026-06-13 | Added original PV audio. Fetched `assets/badapple_audio.mp3` (Internet Archive item `bad-apple-pv_202605`; 320 kbps stereo, 219.19 s — matches the 219 s target). Extended `src/encode.py` to mux it as AAC 192k with `-shortest` (default-on when the file exists; `--no-audio` / `--audio FILE` to control). Re-encoded `output/badapple.mp4` (still the 1710-frame preview): video 57.0 s + audio 56.98 s, in sync, volumedetect mean −9.1 dB (real signal). Frames stay silent; audio is added only at encode. | No change to scene resume point — **still resume at Scene 8** (see row above). Audio now rides along on every `encode.py` run automatically. |

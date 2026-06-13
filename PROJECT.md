# PROJECT.md — Bad Apple!! Fan Recreation: Master Orchestration Document

**Status: preparation complete — production has NOT started. This file tells you everything
you need to begin the real work.**

Last updated: 2026-06-13.

---

## 1. What this project is

A **fan recreation of the "Bad Apple!!" shadow-art PV** — the famous Touhou Project
silhouette animation (original by Anira, Nico Nico Douga sm8628149, 2009). We are
re-drawing the entire video ourselves, programmatically, scene by scene.

Hard constraints:

- **No audio. Visuals only.** The musical structure of the song is used purely as a
  timing reference; the output MP4 has no audio track.
- **Match the original's timing exactly.** Every scene's start/end is locked to a
  researched timestamp (see `SCENES.md`). Total runtime **3:39 = 219 s = 6,570 frames
  at 30 fps** (global frames 0–6569).
- **Drawn on our own, not traced.** This is a fan homage: study the reference stills,
  then author every silhouette by hand as code (polygons/beziers). Do not extract,
  copy, or programmatically trace pixel data from the original frames.
- **As accurate as feasible**: correct characters, actions, props, camera moves,
  morph transitions, and black/white polarity per scene. Stylistic simplification of
  silhouette detail is expected and fine; wrong content or wrong timing is not.
- **Quality bar: RECOGNIZABLE, not perfect.** A viewer who knows the original should
  recognize each scene and what's happening in it. That is the finish line — do not
  polish beyond it (see §9 step 4 iteration cap and §10).

## 2. Required reading (in this order)

1. **This file** — context, contracts, and the execution plan.
2. **`TOOLING.md`** — the toolchain, project standards, and the full `renderlib` API.
   Read it before writing any scene code.
3. **`SCENES.md`** — the single source of truth for WHAT happens WHEN. 35 contiguous
   scenes covering 0:00–3:39 with characters, actions, props, polarity, morph
   transitions, and confidence flags.

## 3. Current state of the repository

| Path | What it is |
|---|---|
| `TOOLING.md` | Stack rationale, standards, renderlib API reference, render/encode commands |
| `SCENES.md` | Complete scene-by-scene breakdown with timestamps, frame ranges, polarity |
| `src/renderlib.py` | Core rendering library (Canvas, easing, beziers, `morph_polys`, `FrameWriter`, `render_scene`) |
| `src/encode.py` | `frames/*.png` → `output/badapple.mp4` (auto-locates ffmpeg) |
| `src/scenes/` | EMPTY — scene scripts go here (one per scene, see §5) |
| `frames/` | Global output frame sequence `frame_NNNNNN.png` (currently empty except `_smoke/`) |
| `output/` | Encoded videos; final deliverable is `output/badapple.mp4` |
| `assets/` | EMPTY — shared shape/character libraries go here (see Phase 1) |
| `_ref_frames/` | 97 verified stills from the original (`t<sec>_f<frame>.jpg`) for visual QC |
| `tests/smoke_test.py` | End-to-end toolchain verification (PASSED 2026-06-13) |
| `frames/_smoke/`, `output/_smoke_test.mp4` | Smoke-test artifacts, safe to delete |

Toolchain is verified working (WSL2 / Ubuntu): Python 3.12 in a project venv
(`.venv`, activate it then run `python`), Pillow + numpy from `requirements.txt`,
ffmpeg 7.0. Measured render speed ~33 fps ⇒ the full 6,570-frame video renders in
~3 minutes, so iterate freely.

## 4. Fixed standards (summary — details in TOOLING.md)

- **960×720, 30 fps, 8-bit grayscale PNG**, frame naming `frame_NNNNNN.png` with the
  **global** frame index (all scenes write into the one shared `frames/` sequence).
- **Polarity:** default is black silhouettes on white (`Canvas()`); inverted passages
  use `canvas.invert()` or `bg=BLACK`. Never hand-pick gray for silhouettes. Gray is
  reserved for the few documented soft elements: Mokou's flames, the moon's glow, the
  Prismriver floor shadows, splash/smoke texture.
- Anti-aliasing is built into `Canvas` (2x supersample); soft edges are expected and
  match the original's look.

## 5. The timeline contract (frame ownership)

Scene boundaries are **half-open ranges `[start, end)`** in global frames. Scene N
writes exactly the frames `start ≤ f < end` and nothing else. Ranges are disjoint and
contiguous — together they cover 0–6569 with no gaps or overlaps. Where SCENES.md's
musical-section map and its scene list differ by a few frames, **the scene list (this
table) governs.**

| # | Script (`src/scenes/`) | Frames `[start, end)` | Count | Duration (s) | Subject |
|---|---|---|---|---|---|
| 1 | `scene_01_loop_reveal.py` | 0 – 120 | 120 | 4.0 | Black screen zooms out to Reimu |
| 2 | `scene_02_reimu_apple.py` | 120 – 450 | 330 | 11.0 | Reimu dances, tosses apple |
| 3 | `scene_03_marisa_flight.py` | 450 – 855 | 405 | 13.5 | Marisa catches apple, starfield flight, drops core |
| 4 | `scene_04_patchouli.py` | 855 – 1080 | 225 | 7.5 | Core → Patchouli dance, wagging finger |
| 5 | `scene_05_remilia.py` | 1080 – 1275 | 195 | 6.5 | Finger → Remilia, bat wings, drops teacup |
| 6 | `scene_06_sakuya.py` | 1275 – 1500 | 225 | 7.5 | Shards, twirl, knife throw |
| 7 | `scene_07_flandre.py` | 1500 – 1710 | 210 | 7.0 | Crystal wings, mid-scene inversion, blade flash |
| 8 | `scene_08_youmu.py` | 1710 – 1920 | 210 | 7.0 | Sword flourish under half-bloomed tree, Yuyuko bg |
| 9 | `scene_09_yuyuko.py` | 1920 – 2130 | 210 | 7.0 | Fan wave, camera follows single petal |
| 10 | `scene_10_komachi.py` | 2130 – 2370 | 240 | 8.0 | Petal → ferry, scythe wipe halves the screen |
| 11 | `scene_11_eiki_split.py` | 2370 – 2526 | 156 | 5.2 | Dual-polarity Eiki at the black/white seam |
| 12 | `scene_12_mokou.py` | 2526 – 2790 | 264 | 8.8 | Rod → Mokou, twin palm flames clapped together |
| 13 | `scene_13_keine_spin.py` | 2790 – 2970 | 180 | 6.0 | Two Keine forms clasp hands in fire, spiral → moon |
| 14 | `scene_14_eirin_moon.py` | 2970 – 3150 | 180 | 6.0 | Eirin reaches for the moon (top-left) |
| 15 | `scene_15_kaguya_whiteout.py` | 3150 – 3363 | 213 | 7.1 | Kaguya reaches for moon (top-right), whiteout |
| 16 | `scene_16_prismriver.py` | 3363 – 3570 | 207 | 6.9 | Prismriver trio concert, floor shadows |
| 17 | `scene_17_chen_ran_tewi.py` | 3570 – 3660 | 90 | 3.0 | One-beat portrait chain (flip on Tewi) |
| 18 | `scene_18_reisen.py` | 3660 – 3750 | 90 | 3.0 | Finger-gun beam splits screen horizontally |
| 19 | `scene_19_momiji_leaves.py` | 3750 – 3810 | 60 | 2.0 | Vertical slash, quadrants become falling leaves |
| 20 | `scene_20_sanae.py` | 3810 – 3930 | 120 | 4.0 | Sweeps giant leaves, catches one on palm |
| 21 | `scene_21_hina.py` | 3930 – 3990 | 60 | 2.0 | Pirouette wipe |
| 22 | `scene_22_kanako_suwako.py` | 3990 – 4230 | 240 | 8.0 | Suwako pops up hat-first, back-to-back, "TV-off" exit |
| 23 | `scene_23_yukari.py` | 4230 – 4410 | 180 | 6.0 | Emerges from gap with parasol, fan open/shut |
| 24 | `scene_24_tenshi.py` | 4410 – 4650 | 240 | 8.0 | Spotlit swagger, profile face-off with Yukari |
| 25 | `scene_25_aya.py` | 4650 – 4830 | 180 | 6.0 | Negative space → wing; writes article, tosses pen |
| 26 | `scene_26_suika.py` | 4830 – 5040 | 210 | 7.0 | Pen → horn; drains gourd, last drop |
| 27 | `scene_27_alice.py` | 5040 – 5220 | 180 | 6.0 | Overhead Alice, holds doll up, lets it fall |
| 28 | `scene_28_nitori_splash.py` | 5220 – 5430 | 210 | 7.0 | Doll → Nitori; run, reach, dive, white splash |
| 29 | `scene_29_yuka_petals.py` | 5430 – 5610 | 180 | 6.0 | Splash → petal storm; Yuka closes parasol |
| 30 | `scene_30_elly.py` | 5610 – 5850 | 240 | 8.0 | Parasol → scythe; Elly takes it and poses |
| 31 | `scene_31_crown_splash.py` | 5850 – 5970 | 120 | 4.0 | Drop from blade tip, milk-crown splash (no characters) |
| 32 | `scene_32_pc98_reimu.py` | 5970 – 6090 | 120 | 4.0 | Water column → PC-98 Reimu rises, looks up |
| 33 | `scene_33_reach.py` | 6090 – 6270 | 180 | 6.0 | Upside-down Marisa, opposite-polarity halves, hands reach |
| 34 | `scene_34_yinyang.py` | 6270 – 6420 | 150 | 5.0 | Full-frame spinning yin-yang orb |
| 35 | `scene_35_finale.py` | 6420 – 6570 | 150 | 5.0 | Marisa flies up / Reimu + apple; zoom to black (loop) |

Total: 6,570 frames. Each scene script sets `SCENE_START_FRAME` and
`SCENE_END_FRAME` from this table and derives `SCENE_DURATION = (end - start) / 30`
— **always compute duration from frame boundaries, never type seconds by hand**, so
rounding can never create gaps or overlaps. Re-running one scene script only
overwrites its own frame range, so scenes can be (re)rendered independently and in
parallel.

## 6. Handoff contracts (scene-to-scene continuity)

Bad Apple's signature is that one silhouette **morphs** into the next across scene
boundaries. SCENES.md documents every transition in its "Transition out / in" lines.
Rules:

1. **The outgoing scene owns the morph.** By its final frame it must have animated
   its subject into the *handoff state* (e.g. scene 3's last frame shows the bounced
   apple core; scene 9's last frame is the petal filling the frame). The incoming
   scene's first frame continues from that state.
2. **Shared handoff shapes.** Every shape that crosses a boundary (apple core, raised
   finger, teacup shard, knife tip, petal, Rod of Remorse, pen, sake drop, doll,
   splash, parasol/scythe, water column, yin-yang dots…) must be defined ONCE in the
   shared assets module (Phase 1) and imported by BOTH adjacent scenes. That makes
   the boundary pixel-consistent by construction.
3. **Polarity must agree at every boundary** — both sides per SCENES.md. Where the
   flip happens *at* the boundary (e.g. 2→3 at the catch, 5→6 at the shatter,
   22→23 at the gap reveal), the incoming scene starts already flipped; a hard cut
   there is correct and expected by the continuity check (§9).
4. Some boundaries are explicit hard cuts or full-frame states (scene 15 ends in
   pure white; scene 35 ends in pure black = scene 1's first frame, closing the
   loop). Match exactly.

## 7. Style consistency (what makes 35 scenes read as ONE video)

- **One figure style.** Build a parametric silhouette-figure toolkit in the shared
  assets module (Phase 1): consistent head/body proportions, a dress/skirt builder,
  arm/hand poses — then differentiate characters by their *identifying features*
  (SCENES.md lists them per scene: Reimu's bow + sleeves, Marisa's hat + braid,
  Remilia's scalloped wings, Suwako's flat hat, rabbit ears, etc.). Silhouettes must
  be identifiable from outline alone — the feature IS the character.
- **Smooth motion, eased.** Use `ease()` for everything; the original's movement is
  fluid and dance-like, never linear or jerky.
- **Camera language.** Zooms/pans are done by animating `transform()` scale/translate
  on the whole composition. SCENES.md flags every camera move.
- **Gray discipline** as in §4 — silhouettes are pure ink, gray only for the
  documented glow/fire/shadow elements.

## 8. Using the reference frames

`_ref_frames/t<sec>_f<frame>.jpg` are 97 stills from the original at 480×360.
**Frame numbers in their filenames are 1-indexed** (from the bleov/bad-apple-frames
GitHub repo); our global index is that number minus 1. More stills can be fetched
from `https://raw.githubusercontent.com/bleov/bad-apple-frames/` if a scene needs
extra reference (the repo has all 6,572 frames at exactly 30 fps; our timeline uses
the first 6,570).

Use them to: study a pose/composition before authoring it, and visually compare your
rendered frame against the corresponding ref frame (the Read tool displays both
PNGs and JPGs). Do NOT trace or programmatically extract contours from them (§1).

## 9. Execution plan (for the orchestrating agent)

### Phase 1 — Shared asset library (sequential, do this FIRST)

One agent builds `assets/shapes.py` (or `src/assets_shapes.py`) containing:

- The **parametric figure toolkit** (§7).
- **Recurring characters** appearing in multiple scenes, each as posed silhouette
  shape sets: Reimu (modern: scenes 1–2; hair-down design: 32, 33, 35), Marisa
  (scenes 3, 33, 35), Yukari (23, 24).
- **All handoff shapes** crossing scene boundaries (§6, rule 2) — enumerate them from
  SCENES.md's transition lines.
- Shared props used widely: the apple (scenes 1, 2, 3, 35), broom (3, 35),
  parasol/scythe (29, 30, 31).

The asset agent must visually verify its shapes: render samples to a scratch dir
(e.g. `frames/_assets_preview/`), view the PNGs, iterate until silhouettes read
clearly, and document every exported shape/function at the top of the module.

### Phase 2 — Scene production (parallel fan-out)

One agent per scene (or small batches of adjacent scenes — adjacent batching makes
handoffs easier). Frame ranges are disjoint, so parallel rendering into `frames/` is
safe. Brief each scene agent with:

1. Read `TOOLING.md` (API + standards), this file's §5–§8, and your scene's full
   entry in `SCENES.md` — including its "Transition in/out" lines and the entries of
   BOTH neighboring scenes.
2. View the `_ref_frames/` stills inside your frame range (fetch more if needed).
3. Write `src/scenes/scene_NN_<slug>.py` per the template in TOOLING.md §4, with
   `SCENE_START_FRAME` / `SCENE_END_FRAME` from §5's table. Import shared shapes
   from the assets module — especially the handoff shapes at your two boundaries.
4. Render (`python src/scenes/scene_NN_<slug>.py`), then **view your own output**: first
   frame, last frame, and 3–5 mid-action frames (or one contact sheet), compared
   against the refs. **Hard cap: 2 fix passes after the initial render** (3
   render-and-view rounds total). Judge only against the recognizability bar (§1):
   character identifiable from the silhouette, action readable, polarity correct
   (including any mid-scene flip at the documented window), boundary frames matching
   the handoff contract, frame count exact. Fix ONLY failures of that list — never
   refine proportions, smoothness, or detail that already reads fine. The cap may be
   exceeded only for hard correctness failures (wrong frame count, wrong polarity,
   broken handoff, script crash). If something cosmetic still bothers you at the
   cap, write it in PROGRESS.md's Notes column and move on.
5. Report: frames written (must equal the table's count), deviations from SCENES.md
   (if any), and confirmation of both boundary states.

Respect the decisions in §10 — do not re-litigate them.

### Phase 3 — Integration, QC, final encode (sequential, after all scenes)

1. **Frame census:** every `frame_000000.png` … `frame_006569.png` exists exactly
   once in `frames/` (write a small checker script; ignore `_smoke/` and preview
   subdirs).
2. **Boundary continuity audit:** for each of the 34 boundaries, view/diff the last
   frame of scene N and the first of N+1. Expect visual continuity except where §6
   rule 3 documents a flip/hard cut at that boundary.
3. **Polarity audit:** sample 2–3 frames per scene, check the dominant polarity
   column of SCENES.md's summary table.
4. **Spot-check vs originals:** compare ~20 rendered frames against their
   `_ref_frames/` counterparts across the whole timeline.
5. **Encode:** `python src/encode.py` → `output/badapple.mp4`. Probe with ffprobe:
   expect `width=960 height=720 r_frame_rate=30/1 nb_frames=6570
   duration=219.000000`, and no audio stream.
6. **Loop check:** first and last frames are both solid black (scene 35 → scene 1).
7. Fix-and-rerender loop: failures go back to the owning scene's script; only that
   frame range needs re-rendering; then re-encode.

**Acceptance =** all seven checks pass.

## 10. Decisions already made (do not re-litigate)

- **Aki sisters cameo (~2:07): SKIP.** Single-source, contradicts the canonical
  36-appearance count (flagged LOW CONFIDENCE in SCENES.md). The leaf quadrants in
  scene 19 are just leaves.
- **Final Reimu/Marisa design (scene 35):** Reimu with hair down and no sleeve
  ruffles, per SCENES.md's reconciliation of conflicting sources.
- **Exact flip frames:** SCENES.md brackets each polarity flip to a 30–45-frame
  window. Scene authors place the flip at the morph/accent moment *within* that
  window — this is an authoring choice, not an error.
- **Resolution/fps/polarity conventions** are FIXED as in §4 / TOOLING.md.
- **No audio track** in the final MP4, ever.
- **Quality bar = recognizability (user decision, 2026-06-13).** "We don't need
  things to be perfect, we just want to recognize what's going on." The §9 step 4
  iteration cap enforces this — do not exceed it for cosmetic reasons, and do not
  schedule polish work unless the user asks. An optional polish pass on
  PROGRESS.md-flagged scenes happens only after the full video is assembled, with
  leftover budget, at the user's request.

## 11. Known pitfalls

- Activate the venv (`source .venv/bin/activate`) before running scripts so
  `python` resolves to the project interpreter with Pillow/numpy installed.
- `ffmpeg` may not be on PATH in a fresh shell; `src/encode.py` handles the fallback
  (PATH, then `~/.local/bin`) — prefer it over raw ffmpeg commands.
- `frames/_smoke/` and `output/_smoke_test.mp4` are disposable test artifacts. Keep
  scratch renders in underscore-prefixed subdirs so they never pollute the global
  sequence.
- `render_scene` computes frame count as `round(duration * fps)` — which is why §5
  mandates deriving duration from integer frame boundaries.
- SCENES.md's musical-section table and scene list disagree by ≤3 frames in places;
  the **scene list / §5 table governs** frame ownership.
- The ref-frame repo has 6,572 frames; our timeline is 6,570. Refs are 1-indexed.
  Both facts matter when mapping `t<sec>_f<frame>.jpg` names to our indices (§8).

## 12. Session & budget management (IMPORTANT — limited token budget)

This project runs on a capped subscription (rolling 5-hour windows + weekly limit).
Production must survive interruption at any moment and spend tokens deliberately.

**Resume protocol (start of EVERY session):** read `PROGRESS.md` first. Verify the
last scene marked done actually has its frames on disk (count files in its range)
before continuing. Disk is ground truth; PROGRESS.md is the map. Update PROGRESS.md
(status + session log) after every completed scene — never batch the bookkeeping to
"the end of the session," because the session may not end gracefully.

**Work in small chronological batches.** Do scenes in timeline order, ~3–6 per
session, one agent at a time. Reasons: (a) adjacent scenes share handoff shapes, so
the morph contracts are fresh in context; (b) a contiguous completed prefix
(frames 0..N) can be encoded at any time for a partial preview —
`python src/encode.py` works on any gapless sequence starting at 0; (c) a batch fits
comfortably inside one usage window, so interruptions land between scenes, not
inside them.

**Do NOT use large parallel fan-outs** (many simultaneous scene agents / Workflow
swarms). Parallelism doesn't reduce total tokens — it concentrates the same spend
into one window and slams into the rate cap mid-flight, which is the worst possible
interruption point. Sequential batches give the same total progress with graceful
stopping points.

**Token economy rules for scene agents:**
- Images are the dominant cost. View frames purposefully: first frame, last frame,
  3–5 mid-action frames per iteration — not every frame.
- Prefer **contact sheets**: Phase 1 should add a tiny helper
  (`tests/contact_sheet.py`) that tiles N frames into one grid PNG with PIL — one
  image view instead of nine. Use it for iteration passes; view single full-size
  frames only for final QC of a pose.
- Respect the **iteration cap** (§9 step 4, max 2 fix passes per scene). Polishing
  past the recognizability bar is the second-biggest budget killer after
  undisciplined image viewing.
- Start scene work in a **fresh session** per batch (context startup via CLAUDE.md
  is cheap; dragging a long conversation re-reads everything each turn and is the
  silent budget killer).
- Capable-but-economical models (Sonnet-class) are fine for scene production —
  the specs in SCENES.md are detailed enough that the work is mostly faithful
  translation, not invention. Save the strongest model for Phase 1 (asset design)
  and Phase 3 (integration judgment).

**Interruption recovery:** a scene script is only "spent" tokens if it was lost
before being written to disk. If a session dies mid-scene, the next session re-runs
or finishes that one scene — frame writes are idempotent (same range overwritten).
Nothing else needs redoing. There is no penalty for pausing the project days or
weeks; all state is in files, the toolchain is installed, and reference stills are
local.

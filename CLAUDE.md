# Bad Apple!! Fan Recreation

Silent (no audio) programmatic recreation of the Bad Apple!! shadow-art PV.
960×720 @ 30 fps, 219 s, 6,570 frames, monochrome silhouettes.

**Before doing ANY work, read in this order:**

0. `PROGRESS.md` — what is already done and where to resume (update it as you work).
1. `PROJECT.md` — master orchestration document: context, frame-ownership table,
   handoff contracts, execution plan, decisions already made — including §12,
   the session/token-budget rules (small chronological batches, no big fan-outs).
2. `TOOLING.md` — standards and the `src/renderlib.py` API.
3. `SCENES.md` — the single source of truth for what to draw when.

Quick rules: activate the venv (`source .venv/bin/activate`) then run `python`;
scene scripts live in `src/scenes/` and write global frames `frame_NNNNNN.png`
into `frames/`; encode with `python src/encode.py`; reference stills in
`_ref_frames/` are for visual comparison only — never trace them. Quality bar is
RECOGNIZABLE, not perfect: max 2 fix passes per scene (PROJECT.md §9 step 4),
then move on.

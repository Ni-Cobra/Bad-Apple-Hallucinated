# Bad Apple!! Hallucinated

Fully programmatic recreation of the *Bad Apple!!* shadow-art PV
Entirely made by Claude.

## Requirements

- **Python 3.12+**
- **ffmpeg** (for encoding the frames into an MP4)

## Setup

```bash
# 1. ffmpeg
sudo apt install ffmpeg

# 2. Python deps (in a virtualenv)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
source .venv/bin/activate              # once per shell

python src/scenes/scene_01_loop_reveal.py   # render one scene into frames/
python src/encode.py                         # frames/ -> output/badapple.mp4
python tests/smoke_test.py                   # quick end-to-end toolchain check
```

## Project layout

| Path | What it is |
|---|---|
| `src/renderlib.py` | Core rendering library (Canvas, easing, beziers, morphs) |
| `src/encode.py` | PNG frames → H.264 MP4 (ffmpeg wrapper) |
| `src/scenes/` | One script per scene |
| `frames/` | Rendered frame sequence (generated, git-ignored) |
| `output/` | Encoded videos (generated, git-ignored) |
| `_ref_frames/` | Reference stills from the original, for visual QC only |

See `PROJECT.md`, `TOOLING.md`, and `SCENES.md` for the full design and the
scene-by-scene breakdown.

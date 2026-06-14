# Bad Apple!! Hallucinated

Fully programmatic recreation of the *Bad Apple!!* shadow-art PV
Entirely made by Claude.

I initially wanted to do this as a way to challenge Claude Fable 5 on a practically impossible task, to see how it would figure it out on its own.

The result is... yeah it's shit... and honestly pretty funny lmao but I thought this was a bit interesting in a weird way and why not showing it there.

In one prompt I let Fable do all the online research about the Bad Apple video, setup, technical decisions and orchestration setup for future sessions. I did not intervene and told it it could use any tool it wants to reach that goal, I wanted to see if it was able to guess the challenges and subtilities of it and how to organize the project around it. It decided to build a custom rendering engine in Python

That was right before Fable got banned, so I had to continue with Opus 4.8 for the actual animation programming of the frames, just letting it follow the method Fable decided. Too bad I couldn't let Fable to the animation too.

There are very likely tons of better stacks but again I wanted to let hands-down. I also purposefully asked to set some rules to avoid wasting too much tokens or iterating endlessly on working on a scene, as I only have the Pro Plan for Claude Code, and don't really want to either waste 100 bucks or waiting weeks for creating just one shitpost.

Check out branch `first-attempt`.

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

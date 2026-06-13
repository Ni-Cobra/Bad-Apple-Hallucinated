# TOOLING.md — Bad Apple!! Fan Recreation: Technical Foundation

Last updated: 2026-06-13. This is the authoritative reference for every agent
authoring scenes. Read this before writing any scene code.

---

## 1. Chosen stack and why

**Python 3.12 + Pillow + numpy for frame generation, ffmpeg (libx264) for encoding.**

| Component | Version | Role |
|---|---|---|
| Python 3 | 3.12+ | scene scripts + render library |
| Pillow | 10.4+ | rasterization (ImageDraw), PNG output |
| numpy | 2.0+ | array ops (morph alignment, frame-as-array access) |
| ffmpeg / ffprobe | 6.1+ | PNG sequence -> H.264 MP4, probing |
| pip + venv | — | package management (`requirements.txt`) |

Why this stack:

- **LLM-agent fit.** Scenes are plain Python functions: silhouette shapes as
  point lists, motion as easing-driven parameter changes, morphs as polygon
  interpolation. Fully deterministic — same code, same frames, every run.
- **Lightweight install.** Pillow + numpy via `pip install -r requirements.txt`
  in a venv; ffmpeg via `sudo apt install ffmpeg`. Minimal new surface area.
- **Fast enough.** Measured ~35 frames/s at 960x720 with 2x supersampling
  (single core). The full 6,570-frame video renders in ~3 minutes. Headroom
  is large; scene complexity can grow 5–10x and still render in under an hour.
- **Alternatives rejected:**
  - *HTML canvas + headless browser capture*: adds browser automation
    flakiness (timing, GPU variance), and frame-exact determinism is harder
    to guarantee.
  - *SVG + rasterizer (cairosvg/resvg)*: adds an XML indirection layer for no
    benefit — Pillow polygons already express silhouettes directly.
  - *Processing/p5*: requires a Java/Node runtime; weaker for headless
    deterministic batch rendering.
  - *opencv-python*: not needed — monochrome silhouettes need no CV; skipped
    to keep installs light. Add later only if raster post-effects are wanted.

**Note on ffmpeg PATH:** `src/encode.py` resolves ffmpeg from PATH first, then
falls back to `~/.local/bin` (handy if you drop a static ffmpeg build there
instead of installing system-wide).

---

## 2. Project standards (FIXED — all scenes must conform)

| Standard | Value | Rationale |
|---|---|---|
| Resolution | **960 x 720** | 4:3 like the original; 2x the classic 480x360 so silhouette edges stay clean on modern screens; cheap to render |
| Frame rate | **30 fps** | the rate the original is commonly reproduced at |
| Total duration | **219 s (3:39) = 6,570 frames** | matches the original |
| Color mode | 8-bit grayscale PNG (`L`) | monochrome shadow art; AA edges produce grays — expected |
| Audio | none | visuals-only project |
| Frame naming | `frame_NNNNNN.png` (6 digits, global index from 0) | one continuous sequence across all scenes |
| Anti-aliasing | 2x supersample + Lanczos downsample (built into `Canvas`) | Pillow has no native AA |

### Polarity convention (IMPORTANT)

- **DEFAULT polarity: BLACK silhouettes on a WHITE background** — the iconic
  Bad Apple look. `Canvas()` gives you this: background pre-filled white,
  default ink black.
- **Inverted passages (white-on-black):** either build the frame normally and
  call `canvas.invert()` at the end of your draw function (best for hard
  flash cuts mid-scene), or construct `Canvas` via
  `render_scene(..., bg=BLACK)` for a scene that is inverted throughout
  (default ink is then automatically white).
- Never hand-pick gray fills for silhouettes; use the default ink so polarity
  flips stay correct. Explicit `color=` is reserved for rare deliberate
  gray accents.

---

## 3. Folder structure

```
BadApple/
├── TOOLING.md            <- this file
├── requirements.txt      <- Python dependencies (pillow, numpy)
├── src/
│   ├── renderlib.py      <- core rendering library (the API below)
│   ├── encode.py         <- frames -> mp4 encoder (ffmpeg wrapper)
│   └── scenes/           <- one script per scene (scene authors work here)
├── frames/               <- rendered global frame sequence (frame_000000.png ...)
│   └── _smoke/           <- smoke-test frames (test artifact, safe to delete)
├── output/               <- encoded videos (badapple.mp4 final deliverable)
│   └── _smoke_test.mp4   <- smoke-test video (test artifact, safe to delete)
├── assets/               <- optional shared shape libraries / reference data
└── tests/
    └── smoke_test.py     <- end-to-end toolchain verification
```

Scene scripts in `src/scenes/` import renderlib with:

```python
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from renderlib import *
```

---

## 4. renderlib API (`src/renderlib.py`)

Constants: `WIDTH=960`, `HEIGHT=720`, `FPS=30`, `SUPERSAMPLE=2`,
`BLACK=0`, `WHITE=255`. All coordinates are logical 960x720 pixels,
origin top-left, y down. `Point = (x, y)` tuple.

### Easing / interpolation

| Function | Signature | Purpose |
|---|---|---|
| `clamp01` | `clamp01(t) -> float` | clamp to [0,1] |
| `lerp` | `lerp(a, b, t) -> float` | scalar linear interpolation |
| `lerp_pt` | `lerp_pt(p, q, t) -> Point` | 2D point interpolation |
| `ease` | `ease(t, kind="in_out") -> float` | kinds: `linear`, `in`, `out`, `in_out` (smoothstep — general default), `in_out_cubic`, `smoother` |

```python
x = lerp(100, 860, ease(u, "in_out"))   # eased sweep over the scene
```

### Bezier paths

| Function | Signature | Purpose |
|---|---|---|
| `bezier_point` | `bezier_point(ctrl, t) -> Point` | any-degree Bezier eval (De Casteljau) |
| `bezier_points` | `bezier_points(ctrl, n=48) -> list[Point]` | sampled polyline; use as a motion path or as a curved outline segment for `polygon()` |

```python
path = bezier_points([(60, 600), (300, 300), (660, 700), (900, 380)], 90)
cx, cy = path[int(u * (len(path) - 1))]      # move along the curve
```

### Polygon utilities

| Function | Signature | Purpose |
|---|---|---|
| `transform` | `transform(points, translate=(0,0), rotate=0.0, scale=1.0, origin=(0,0)) -> list[Point]` | scale -> rotate (radians, about `origin`) -> translate |
| `resample_polygon` | `resample_polygon(points, n=128) -> list[Point]` | n evenly spaced perimeter points on a closed outline |
| `morph_polys` | `morph_polys(poly_a, poly_b, t, n=128, align=True) -> list[Point]` | shape interpolation; `align` auto-rotates B's start vertex to avoid twisting. Define both shapes with the same winding. |

```python
body = morph_polys(GIRL_STANDING, GIRL_ARMS_UP, ease(u, "smoother"))
c.polygon(transform(body, rotate=0.1 * math.sin(u * 2 * math.pi), origin=(480, 360)))
```

### class `Canvas`

`Canvas(width=960, height=720, bg=WHITE, supersample=2)` — one frame.
`bg=WHITE` -> ink black (default polarity); `bg=BLACK` -> ink white.
Every drawing method accepts optional `color=` (0–255) overriding the ink.

| Method | Signature | Purpose |
|---|---|---|
| `fill` | `fill(color)` | flood whole canvas |
| `polygon` | `polygon(points, color=None)` | filled closed polygon — the workhorse silhouette primitive |
| `ellipse` | `ellipse(cx, cy, rx, ry, color=None)` | filled axis-aligned ellipse |
| `circle` | `circle(cx, cy, r, color=None)` | filled circle |
| `rectangle` | `rectangle(x0, y0, x1, y1, color=None)` | filled rectangle |
| `line` | `line(points, width=3.0, color=None)` | stroked polyline, round joints |
| `bezier` | `bezier(ctrl, width=3.0, color=None, samples=48)` | stroked Bezier curve |
| `invert` | `invert()` | polarity flip of the whole frame (call after drawing) |
| `image` | `image() -> PIL.Image` | finished frame at 960x720 (downsampled) |
| `to_array` | `to_array() -> np.ndarray` | finished frame as (720, 960) uint8 array |

### class `FrameWriter`

`FrameWriter(out_dir, start_frame=0, prefix="frame_", digits=6)` — creates
`out_dir`, writes `frame_NNNNNN.png` starting at `start_frame` (pass your
scene's global frame offset so all scenes form one sequence).
`write(canvas_or_pil_image) -> str` saves the next frame and returns its path.
`frame_index` is the next index to be written.

### `render_scene`

```python
render_scene(writer, duration, draw,
             fps=30, width=960, height=720, bg=WHITE,
             supersample=2, verbose=True) -> int   # frames written
```

Calls `draw(canvas, u, i, t)` once per frame with a fresh canvas:
`u` = progress in [0,1), `i` = local frame index, `t` = local seconds.
Frame count is `round(duration * fps)` — use exact multiples of 1/30 s so
scenes chain without drift.

### Complete minimal scene (`src/scenes/example.py` pattern)

```python
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from renderlib import *

SCENE_START_FRAME = 0          # global offset of this scene in the 6,570-frame timeline
SCENE_DURATION = 4.0           # seconds

# frames/ at the project root, resolved relative to this file (cwd-independent)
FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")
writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)

APPLE = [(480, 250), (560, 290), (590, 380), (540, 470), (420, 470),
         (370, 380), (400, 290)]

def draw(c: Canvas, u: float, i: int, t: float) -> None:
    sway = 30 * math.sin(u * 2 * math.pi)
    c.polygon(transform(APPLE, translate=(sway, 0)))
    if t >= 2.0:               # white-on-black for the second half
        c.invert()

render_scene(writer, SCENE_DURATION, draw)
```

---

## 5. How to render and encode (from the project root, venv activated)

Activate the virtualenv once per shell (`source .venv/bin/activate`), then
render a scene (each scene script writes its frames into `frames/`):

```bash
python src/scenes/example.py
```

Encode the full frame sequence to the deliverable:

```bash
python src/encode.py            # frames/*.png -> output/badapple.mp4 @ 30 fps, CRF 18, yuv420p, faststart
```

Options: `--frames <dir> --out <file> --fps 30 --crf 18 --prefix frame_ --digits 6`.
The script auto-detects the starting frame number and locates ffmpeg (PATH,
then `~/.local/bin`).

Equivalent raw one-liner (ffmpeg on PATH):

```bash
ffmpeg -y -framerate 30 -i frames/frame_%06d.png -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -movflags +faststart output/badapple.mp4
```

Probe the result:

```bash
ffprobe -v error -select_streams v:0 -show_entries "stream=width,height,r_frame_rate,nb_frames,duration" -of default=noprint_wrappers=1 output/badapple.mp4
```

---

## 6. Smoke test (verified 2026-06-13)

`tests/smoke_test.py` renders 2 s / 60 frames exercising: eased circle sweep,
square->triangle `morph_polys`, a stroked Bezier ribbon, and a polarity
inversion at t = 1.0 s. Then encoded with `src/encode.py`.

```bash
python tests/smoke_test.py
python src/encode.py --frames frames/_smoke --out output/_smoke_test.mp4
```

Results (verified on WSL2 / Ubuntu, Python 3.12, ffmpeg 7.0):

- **Render:** 60 frames in ~1.8 s = **~33 frames/s** -> full video
  (6,570 frames) extrapolates to **~3.3 minutes** of render time. Realistic.
- **Encode:** `output/_smoke_test.mp4`, ~50 KB, encoded faster than realtime.
- **ffprobe:** `width=960 height=720 r_frame_rate=30/1 duration=2.000000 nb_frames=60` — all correct.
- **Visual check:** frames inspected before and after the inversion point;
  black-on-white and white-on-black both correct, edges anti-aliased.

Test artifacts are kept in clearly marked locations — `frames/_smoke/` and
`output/_smoke_test.mp4` — and may be deleted or regenerated at any time.

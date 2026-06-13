"""renderlib -- core rendering library for the Bad Apple!! fan recreation.

PROJECT STANDARDS (do not change without updating TOOLING.md):
    Resolution : 960 x 720 (4:3, matches the original aspect ratio)
    Frame rate : 30 fps
    Color mode : 8-bit grayscale ("L"), strictly monochrome in spirit
                 (anti-aliased edges produce gray pixels; that is expected)
    Polarity   : DEFAULT scene polarity is BLACK SILHOUETTES ON WHITE
                 BACKGROUND (the iconic Bad Apple look). "Inverted" scenes
                 (white silhouettes on black) are produced either by
                 constructing Canvas(bg=BLACK) or by calling canvas.invert().

All drawing helpers take coordinates in LOGICAL pixels (960x720 space).
Internally the canvas is rendered at SUPERSAMPLE x resolution and
downsampled with a Lanczos filter when the frame is emitted, which gives
smooth anti-aliased silhouette edges (Pillow's ImageDraw has no native AA).

Typical scene script:

    from renderlib import *

    writer = FrameWriter("frames")   # path relative to the project root

    def draw(c: Canvas, u: float, i: int, t: float) -> None:
        # u: normalized progress 0..1 over the scene, i: local frame index,
        # t: local time in seconds
        x = lerp(100, 860, ease(u, "in_out"))
        c.circle(x, 360, 80)          # black silhouette on white bg

    render_scene(writer, duration=2.0, draw=draw)

Then encode with src/encode.py (see TOOLING.md).
"""

from __future__ import annotations

import math
import os
from typing import Callable, Iterable, List, Sequence, Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageOps

# ---------------------------------------------------------------------------
# Project-wide constants
# ---------------------------------------------------------------------------

WIDTH: int = 960          # logical canvas width  (project standard)
HEIGHT: int = 720         # logical canvas height (project standard)
FPS: int = 30             # project standard frame rate
SUPERSAMPLE: int = 2      # internal oversampling factor for anti-aliasing

BLACK: int = 0
WHITE: int = 255

Point = Tuple[float, float]


# ---------------------------------------------------------------------------
# Interpolation / easing
# ---------------------------------------------------------------------------

def clamp01(t: float) -> float:
    """Clamp *t* into the closed interval [0, 1]."""
    return 0.0 if t < 0.0 else (1.0 if t > 1.0 else t)


def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between scalars *a* and *b* at parameter *t*."""
    return a + (b - a) * t


def lerp_pt(p: Point, q: Point, t: float) -> Point:
    """Linear interpolation between 2D points *p* and *q* at parameter *t*."""
    return (lerp(p[0], q[0], t), lerp(p[1], q[1], t))


def ease(t: float, kind: str = "in_out") -> float:
    """Easing function. *t* in [0,1] -> eased value in [0,1].

    kind: "linear", "in" (quadratic accelerate), "out" (quadratic
    decelerate), "in_out" (smoothstep, the default -- good general-purpose
    motion), "in_out_cubic" (stronger ends), "smoother" (Perlin smootherstep,
    zero 1st+2nd derivative at the ends -- best for seamless morph loops).
    """
    t = clamp01(t)
    if kind == "linear":
        return t
    if kind == "in":
        return t * t
    if kind == "out":
        return 1.0 - (1.0 - t) * (1.0 - t)
    if kind == "in_out":
        return t * t * (3.0 - 2.0 * t)
    if kind == "in_out_cubic":
        return 4 * t ** 3 if t < 0.5 else 1 - ((-2 * t + 2) ** 3) / 2
    if kind == "smoother":
        return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)
    raise ValueError(f"unknown easing kind: {kind!r}")


# ---------------------------------------------------------------------------
# Bezier paths
# ---------------------------------------------------------------------------

def bezier_point(ctrl: Sequence[Point], t: float) -> Point:
    """Evaluate a Bezier curve of arbitrary degree (De Casteljau) at *t*."""
    pts = [tuple(p) for p in ctrl]
    while len(pts) > 1:
        pts = [lerp_pt(pts[i], pts[i + 1], t) for i in range(len(pts) - 1)]
    return pts[0]


def bezier_points(ctrl: Sequence[Point], n: int = 48) -> List[Point]:
    """Sample *n* points along a Bezier curve defined by control points.

    Use the result as a motion path, or feed it to Canvas.polygon()/line()
    to draw smooth curved silhouette outlines.
    """
    if n < 2:
        raise ValueError("n must be >= 2")
    return [bezier_point(ctrl, i / (n - 1)) for i in range(n)]


# ---------------------------------------------------------------------------
# Polygon utilities (transform, resample, morph)
# ---------------------------------------------------------------------------

def transform(points: Sequence[Point],
              translate: Point = (0.0, 0.0),
              rotate: float = 0.0,
              scale: float | Point = 1.0,
              origin: Point = (0.0, 0.0)) -> List[Point]:
    """Scale, then rotate (radians, about *origin*), then translate points.

    *scale* may be a scalar or an (sx, sy) pair. Returns a new point list.

    Example -- spin a triangle around its center:
        tri = transform(TRI, rotate=u * 2 * math.pi, origin=(480, 360))
    """
    sx, sy = (scale, scale) if isinstance(scale, (int, float)) else scale
    cos_a, sin_a = math.cos(rotate), math.sin(rotate)
    ox, oy = origin
    tx, ty = translate
    out: List[Point] = []
    for x, y in points:
        x, y = (x - ox) * sx, (y - oy) * sy
        x, y = x * cos_a - y * sin_a, x * sin_a + y * cos_a
        out.append((x + ox + tx, y + oy + ty))
    return out


def resample_polygon(points: Sequence[Point], n: int = 128) -> List[Point]:
    """Resample a closed polygon outline to *n* evenly spaced perimeter points.

    Required preprocessing for morph_polys(); also useful to smooth coarse
    outlines. Vertex 0 of the output coincides with vertex 0 of the input.
    """
    pts = list(points)
    if len(pts) < 3:
        raise ValueError("polygon needs >= 3 points")
    # Cumulative perimeter lengths over the closed loop.
    segs = [(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts))]
    lengths = [math.dist(a, b) for a, b in segs]
    total = sum(lengths)
    if total == 0:
        return [pts[0]] * n
    out: List[Point] = []
    target = 0.0
    step = total / n
    seg_i, seg_start = 0, 0.0
    for _ in range(n):
        while seg_i < len(segs) - 1 and seg_start + lengths[seg_i] < target:
            seg_start += lengths[seg_i]
            seg_i += 1
        a, b = segs[seg_i]
        local = 0.0 if lengths[seg_i] == 0 else (target - seg_start) / lengths[seg_i]
        out.append(lerp_pt(a, b, local))
        target += step
    return out


def morph_polys(poly_a: Sequence[Point], poly_b: Sequence[Point],
                t: float, n: int = 128, align: bool = True) -> List[Point]:
    """Interpolated polygon between two closed shapes at parameter *t* in [0,1].

    Both polygons are resampled to *n* perimeter points; with *align* True
    (default) the start vertex of B is cyclically rotated to minimize total
    travel distance, which avoids "twisting" morphs. Define both shapes with
    the SAME winding direction (e.g. clockwise) for best results.

    Example -- square melting into a triangle over a scene:
        shape = morph_polys(SQUARE, TRIANGLE, ease(u, "in_out"))
        c.polygon(shape)
    """
    a = resample_polygon(poly_a, n)
    b = resample_polygon(poly_b, n)
    if align:
        an = np.asarray(a)
        bn = np.asarray(b)
        best_off, best_cost = 0, float("inf")
        for off in range(n):
            cost = float(np.sum((np.roll(bn, -off, axis=0) - an) ** 2))
            if cost < best_cost:
                best_cost, best_off = cost, off
        b = list(map(tuple, np.roll(bn, -best_off, axis=0)))
    t = clamp01(t)
    return [lerp_pt(a[i], b[i], t) for i in range(n)]


# ---------------------------------------------------------------------------
# Canvas
# ---------------------------------------------------------------------------

class Canvas:
    """A monochrome drawing surface for one frame.

    Created fresh for every frame (render_scene does this for you).
    Coordinates are in LOGICAL pixels (default 960x720); internally drawn at
    SUPERSAMPLE x size and downsampled on emit for anti-aliased edges.

    bg  -- background gray level: WHITE (default polarity) or BLACK.
    ink -- default drawing color: automatically the opposite of bg, so
           Canvas() draws black silhouettes on white, Canvas(bg=BLACK)
           draws white silhouettes on black. Any helper accepts an explicit
           color= override (0..255) for the rare gray accent.
    """

    def __init__(self, width: int = WIDTH, height: int = HEIGHT,
                 bg: int = WHITE, supersample: int = SUPERSAMPLE):
        self.width, self.height = width, height
        self.ss = max(1, int(supersample))
        self.bg = bg
        self.ink = BLACK if bg >= 128 else WHITE
        self._img = Image.new("L", (width * self.ss, height * self.ss), bg)
        self._draw = ImageDraw.Draw(self._img)
        self._inverted = False

    # -- internal ----------------------------------------------------------
    def _s(self, points: Iterable[Point]) -> List[Tuple[float, float]]:
        return [(x * self.ss, y * self.ss) for x, y in points]

    def _c(self, color: int | None) -> int:
        return self.ink if color is None else int(color)

    # -- drawing primitives -------------------------------------------------
    def fill(self, color: int) -> None:
        """Flood the whole canvas with *color*."""
        self._draw.rectangle([0, 0, self._img.width, self._img.height],
                             fill=int(color))

    def polygon(self, points: Sequence[Point], color: int | None = None) -> None:
        """Fill a closed polygon (the workhorse silhouette primitive)."""
        self._draw.polygon(self._s(points), fill=self._c(color))

    def ellipse(self, cx: float, cy: float, rx: float, ry: float,
                color: int | None = None) -> None:
        """Fill an axis-aligned ellipse centered at (cx, cy)."""
        s = self.ss
        self._draw.ellipse([(cx - rx) * s, (cy - ry) * s,
                            (cx + rx) * s, (cy + ry) * s],
                           fill=self._c(color))

    def circle(self, cx: float, cy: float, r: float,
               color: int | None = None) -> None:
        """Fill a circle of radius *r* centered at (cx, cy)."""
        self.ellipse(cx, cy, r, r, color)

    def rectangle(self, x0: float, y0: float, x1: float, y1: float,
                  color: int | None = None) -> None:
        """Fill an axis-aligned rectangle."""
        s = self.ss
        self._draw.rectangle([x0 * s, y0 * s, x1 * s, y1 * s],
                             fill=self._c(color))

    def line(self, points: Sequence[Point], width: float = 3.0,
             color: int | None = None) -> None:
        """Stroke a polyline with round joints (for thin strokes/ribbons)."""
        s = self.ss
        self._draw.line(self._s(points), fill=self._c(color),
                        width=max(1, round(width * s)), joint="curve")

    def bezier(self, ctrl: Sequence[Point], width: float = 3.0,
               color: int | None = None, samples: int = 48) -> None:
        """Stroke a Bezier curve given its control points."""
        self.line(bezier_points(ctrl, samples), width=width, color=color)

    # -- polarity ------------------------------------------------------------
    def invert(self) -> None:
        """Swap black and white over the entire canvas (polarity flip).

        Call AFTER drawing to flip a finished frame, e.g. for the signature
        Bad Apple white-on-black passages or hard flash cuts.
        """
        self._img = ImageOps.invert(self._img)
        self._draw = ImageDraw.Draw(self._img)
        self.bg, self.ink = 255 - self.bg, 255 - self.ink
        self._inverted = not self._inverted

    # -- output ---------------------------------------------------------------
    def image(self) -> Image.Image:
        """Return the finished frame at logical resolution (downsampled)."""
        if self.ss == 1:
            return self._img.copy()
        return self._img.resize((self.width, self.height), Image.LANCZOS)

    def to_array(self) -> np.ndarray:
        """Return the finished frame as a (H, W) uint8 numpy array."""
        return np.asarray(self.image(), dtype=np.uint8)


# ---------------------------------------------------------------------------
# Frame output
# ---------------------------------------------------------------------------

class FrameWriter:
    """Writes numbered PNG frames: frame_000000.png, frame_000001.png, ...

    out_dir     -- destination folder (created if missing).
    start_frame -- global index of the first frame this writer emits. Scene
                   scripts rendering a mid-video scene pass their global
                   offset here so all frames form one continuous sequence.

    Example:
        w = FrameWriter("frames", start_frame=900)   # scene starts at 0:30
    """

    def __init__(self, out_dir: str, start_frame: int = 0,
                 prefix: str = "frame_", digits: int = 6):
        self.out_dir = out_dir
        self.prefix = prefix
        self.digits = digits
        self.frame_index = start_frame
        os.makedirs(out_dir, exist_ok=True)

    def write(self, frame: "Canvas | Image.Image") -> str:
        """Save the next frame (Canvas or PIL Image); returns the file path."""
        img = frame.image() if isinstance(frame, Canvas) else frame
        path = os.path.join(
            self.out_dir, f"{self.prefix}{self.frame_index:0{self.digits}d}.png")
        img.save(path, optimize=False, compress_level=1)
        self.frame_index += 1
        return path


# ---------------------------------------------------------------------------
# Scene driver
# ---------------------------------------------------------------------------

def render_scene(writer: FrameWriter, duration: float,
                 draw: Callable[[Canvas, float, int, float], None],
                 fps: int = FPS, width: int = WIDTH, height: int = HEIGHT,
                 bg: int = WHITE, supersample: int = SUPERSAMPLE,
                 verbose: bool = True) -> int:
    """Render *duration* seconds of animation by calling *draw* per frame.

    draw(canvas, u, i, t) receives:
        canvas -- a fresh Canvas (background pre-filled with *bg*)
        u      -- normalized scene progress in [0, 1) == i / frame_count
        i      -- local frame index, 0 .. frame_count-1
        t      -- local time in seconds == i / fps

    Returns the number of frames written. Frame count is round(duration*fps),
    so chain scenes by passing exact multiples of 1/30 s as durations.
    """
    frame_count = round(duration * fps)
    for i in range(frame_count):
        canvas = Canvas(width, height, bg=bg, supersample=supersample)
        draw(canvas, i / frame_count, i, i / fps)
        writer.write(canvas)
        if verbose and (i + 1) % (fps * 5) == 0:
            print(f"  rendered {i + 1}/{frame_count} frames")
    return frame_count

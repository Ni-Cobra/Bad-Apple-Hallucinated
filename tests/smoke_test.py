"""Smoke test: verifies the full toolchain end to end.

Renders 2 seconds (60 frames @ 30fps, 960x720) of a circle silhouette
sweeping across the canvas with an eased motion, a square-to-triangle morph,
a bezier stroke, and a black/white polarity inversion at the 1-second mark.

Run from the project root:
    python tests/smoke_test.py
Then encode + probe:
    python src/encode.py --frames frames/_smoke --out output/_smoke_test.mp4

Test artifacts live in clearly marked locations:
    frames/_smoke/            rendered test frames
    output/_smoke_test.mp4    encoded test video
"""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from renderlib import (Canvas, FrameWriter, WIDTH, HEIGHT, ease, lerp,
                       morph_polys, render_scene)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAMES_DIR = os.path.join(PROJECT_ROOT, "frames", "_smoke")

SQUARE = [(380, 460), (580, 460), (580, 660), (380, 660)]
TRIANGLE = [(480, 440), (620, 660), (340, 660)]


def draw(c: Canvas, u: float, i: int, t: float) -> None:
    # Circle silhouette sweeping left -> right with ease in/out.
    x = lerp(120, WIDTH - 120, ease(u, "in_out"))
    c.circle(x, 220, 90)

    # Square morphing into a triangle across the scene.
    c.polygon(morph_polys(SQUARE, TRIANGLE, ease(u, "in_out")))

    # A bezier ribbon to exercise curve stroking.
    c.bezier([(60, 600), (300, 300), (660, 700), (900, 380)], width=8)

    # Polarity inversion for the second half (white-on-black passage).
    if t >= 1.0:
        c.invert()


def main() -> None:
    writer = FrameWriter(FRAMES_DIR, start_frame=0)
    t0 = time.perf_counter()
    n = render_scene(writer, duration=2.0, draw=draw, verbose=False)
    dt = time.perf_counter() - t0
    fps_render = n / dt
    full = 6570 / fps_render
    print(f"rendered {n} frames in {dt:.2f}s "
          f"({fps_render:.1f} frames/s; full 6570-frame video ~{full / 60:.1f} min)")


if __name__ == "__main__":
    main()

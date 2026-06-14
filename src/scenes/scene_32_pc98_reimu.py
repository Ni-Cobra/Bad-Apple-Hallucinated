"""Scene 32 -- PC-98 Reimu rises (f5970-6090, 120 fr).  W-on-B.

31->32: opens on Scene 31's exact end state -- the rising water COLUMN (a tapering
white column + blob head out of a bottom pool, the milk-crown subsiding).  The
column morphs into old-works Reimu seen from BEHIND, rising with the water (ref
f6031 ~ local f61): hair down, broad kimono-style sleeves, no sleeve ruffles
(shared `reimu_hairdown`).  She lifts her face to the sky.

32->33: ends on the risen white Reimu standing centre on black -- Scene 33 opens
on that same figure, then a black Marisa hangs upside-down above her and the
frame splits into opposite-polarity halves.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: E402,F403
from shapes import (  # noqa: E402
    reimu_hairdown, ellipse_poly, crown_splash, draw_polys, transform_polys,
)

SCENE_START_FRAME = 5970
SCENE_END_FRAME = 6090
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / 30.0   # 4.0 s

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

# --- Scene-31 hand-off end state (reproduced so f0 continues f5969) ----------
POOL = (480.0, 620.0)         # bottom pool ellipse centre (shared with Scene 31)
COL_TOP = 236.0               # top of the rising column at the hand-off
SPLASH = (480.0, 540.0)       # subsiding milk-crown centre

A1 = 28      # pure water-column phase (continues Scene 31)
A2 = 82      # column fully morphed into the risen Reimu (ref f6031 ~ local f61)

# Risen-Reimu standing position (shared with Scene 33's frame 0)
REIMU_DY = 44.0              # translate down so she "rises with the water", low


def reimu_rising(dy, scale=1.0):
    return transform_polys(reimu_hairdown(480), translate=(0.0, dy),
                           scale=scale, origin=(480, 360))


def draw(c, u, i, t):
    c.fill(BLACK)

    # ---- Phase A: the water column from Scene 31 keeps rising ----------------
    if i < A1:
        draw_polys(c, ellipse_poly(POOL[0], POOL[1], 218, 96), color=WHITE)
        c.polygon([(430, 614), (456, COL_TOP), (504, COL_TOP), (530, 614)], color=WHITE)
        c.circle(480, COL_TOP, 22, color=WHITE)
        cs = 0.45 * (1.0 - i / float(A1))            # crown subsides away
        if cs > 0.02:
            draw_polys(c, crown_splash(SPLASH[0], SPLASH[1], r=164, spikes=11, t=cs),
                       color=WHITE)
        return

    # ---- Phase B: the column becomes Reimu rising out of the pool ------------
    if i < A2:
        mb = ease((i - A1) / float(A2 - A1), "in_out")
        col_top = lerp(COL_TOP, POOL[1] - 44, mb)    # column recedes into the pool
        draw_polys(c, ellipse_poly(POOL[0], POOL[1], lerp(218, 116, mb),
                                   lerp(96, 26, mb)), color=WHITE)
        if col_top < POOL[1] - 48:
            c.polygon([(430, 614), (456, col_top), (504, col_top), (530, 614)],
                      color=WHITE)
        draw_polys(c, reimu_rising(lerp(540, REIMU_DY, mb), lerp(0.72, 1.0, mb)),
                   color=WHITE)
        return

    # ---- Phase C: risen Reimu, a gentle upward "looks to the sky" bob --------
    p = (i - A2) / float(SCENE_END_FRAME - SCENE_START_FRAME - A2)
    dy = REIMU_DY - 18.0 * math.sin(math.pi * p)     # bob up and settle back
    draw_polys(c, reimu_rising(dy, 1.0), color=WHITE)


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw, bg=BLACK)   # W-on-B
    print(f"Scene 32: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

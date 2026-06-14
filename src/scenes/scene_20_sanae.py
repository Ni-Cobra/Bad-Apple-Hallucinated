"""Scene 20 -- Sanae sweeps the giant leaves; catches one on her palm
(f3810-3930, 120 fr). B-on-W. VERSE 3 begins.

Continues Scene 19's falling B-on-W leaves. Tiny Sanae at the bottom of the
frame sweeps the huge drifting leaves with a broom (ref f3826/f3856), then a
push-in close-up: she holds the broom upright and catches one small maple leaf
on her open palm (ref f3931 -- the iconic gentle beat).

19->20: leaves rain down (B-on-W) -- opens with big leaves still falling.
20->21: as she watches the caught leaf, Hina bursts in (Scene 21 pirouette
wipe, stays B-on-W) -- ends on the caught-leaf close-up. Sanae built inline
(frog hair clip kept minimal at silhouette scale); leaves are the shared shapes.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: E402,F403
from shapes import (  # noqa: E402
    leaf_maple, leaf_ginkgo, ellipse_poly, circle_poly, head, dress_body,
    ribbon, broom, draw_polys, transform_polys,
)

SCENE_START_FRAME = 3810
SCENE_END_FRAME = 3930
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / 30.0   # 4.0 s

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

CUT = 54            # local frame: wide sweep -> close-up catch

# Big background leaves drifting down (continue Scene 19's rain).
# (builder, x0, y0, fall, drift, spin, radius)
LEAVES = [
    (leaf_maple,  214, 150, 360, 34, -0.30, 138),
    (leaf_ginkgo, 742, 120, 360, 30,  0.42, 132),
    (leaf_ginkgo, 150, 470, 300, 26, -0.50, 120),
    (leaf_maple,  792, 500, 300, 30,  0.36, 134),
    (leaf_maple,  470, 70,  420, 40,  0.20, 96),
]


def sanae_small(cx, foot_y, swing, scale=1.0):
    """Tiny full-figure Sanae sweeping a broom (wide shot)."""
    polys = []
    hy = foot_y - 150
    # hair + head
    polys += ellipse_poly(cx, hy - 6, 30, 34)              # hair mass
    polys += [[(cx - 30, hy + 4), (cx - 14, hy + 2), (cx - 22, hy + 58)]]   # hair tail L
    polys += [[(cx + 30, hy + 4), (cx + 14, hy + 2), (cx + 22, hy + 58)]]   # hair tail R
    polys += head(cx, hy, 24)
    # body + skirt
    polys += dress_body(cx, hy + 26, hy + 78, foot_y, 28, 38, 60)
    # broom held out, angled, sweeping (swing rocks it)
    bx, by = cx - 16, hy + 40
    ang = math.radians(-46 + swing)
    polys += transform_polys(broom(bx, by, length=150, angle=ang,
                                   bristle=64, thick=6, fan_dir=-1),
                             rotate=0.0)
    # near arm to the broom grip
    gx = bx - 60 * math.cos(ang)
    gy = by - 60 * math.sin(ang)
    polys += ribbon([(cx - 22, hy + 40), (gx, gy)], [9, 6])
    if scale != 1.0:
        polys = transform_polys(polys, scale=scale, origin=(cx, foot_y))
    return polys


def sanae_closeup(leaf_in_hand):
    """Close-up profile (facing LEFT): broom held upright, near hand open,
    reaching up toward the descending leaf. ref f3931."""
    polys = []
    hx, hy = 600, 232
    R = 78
    # long hair flowing down the back (to the right / behind)
    polys += [[
        (hx + 30, hy - R * 0.5), (hx + 78, hy - R * 0.2), (hx + 96, hy + 150),
        (hx + 70, hy + 360), (hx + 18, hy + 372), (hx + 6, hy + 150),
        (hx - 6, hy + R),
    ]]
    # head (profile-ish: shifted nose-left silhouette)
    polys += ellipse_poly(hx, hy, R * 0.92, R)
    polys += [[(hx - R * 0.92, hy - 18), (hx - R * 1.16, hy + 6),
               (hx - R * 0.92, hy + 30)]]                  # nose/face bump (faces left)
    # front bang
    polys += [[(hx - R * 0.6, hy - R * 0.9), (hx + 10, hy - R * 1.02),
               (hx + 30, hy - R * 0.2), (hx - R * 0.2, hy - R * 0.3)]]
    # shoulders / upper body
    polys += [[(hx - 70, hy + R + 30), (hx + 90, hy + R + 10),
               (hx + 140, 720), (hx - 150, 720)]]
    # broom held upright (vertical handle through the figure)
    polys += ribbon([(430, 96), (440, 470)], [12, 12])
    polys += [[(404, 470), (476, 470), (496, 600), (384, 600)]]   # bristle fan
    # near (left) arm reaching up-left to the open hand/palm
    palm_x, palm_y = 326, 224
    polys += ribbon([(hx - 56, hy + R + 22), (430, 300), (palm_x + 18, palm_y + 18)],
                    [16, 12, 8])
    # open hand (palm up): little cup of fingers
    polys += ellipse_poly(palm_x, palm_y, 26, 18)
    for fx in (-18, -6, 6, 18):
        polys += ribbon([(palm_x + fx, palm_y - 6), (palm_x + fx, palm_y - 26)], 4)
    return polys


def draw_leaves(c, prog, fade=1.0):
    for fn, x0, y0, fall, drift, spin, r in LEAVES:
        y = y0 + fall * ease(prog, "in")
        x = x0 + drift * math.sin(prog * 2.4 + x0)
        if -200 < y < 920:
            draw_polys(c, fn(x, y, int(r * fade), spin * (0.4 + prog * 1.6)))


def draw(c, u, i, t):
    if i < CUT:
        # WIDE: giant leaves drift down, tiny Sanae sweeps at the bottom.
        prog = i / float(CUT)
        draw_leaves(c, prog)
        swing = 20 * math.sin(i * 0.5)
        draw_polys(c, sanae_small(468, 690, swing))
    else:
        # CLOSE-UP: Sanae catches a single small maple leaf on her open palm.
        p = (i - CUT) / float(SCENE_END_FRAME - SCENE_START_FRAME - 1 - CUT)
        draw_polys(c, sanae_closeup(p))
        # the lone maple leaf descends to rest just above her open palm
        ly = lerp(70, 196, ease(clamp01(p / 0.82), "out"))
        lx = lerp(250, 318, ease(clamp01(p / 0.82), "out")) + 8 * math.sin(p * 6)
        draw_polys(c, leaf_maple(lx, ly, 34, 0.5 + 0.6 * math.sin(p * 4)))


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw)
    print(f"Scene 20: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

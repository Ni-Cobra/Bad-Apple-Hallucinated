"""Scene 17 -- Rapid-fire portrait chain: Chen -> Ran -> Tewi (f3570-3660, 90 fr).

Three one-beat close-up "portraits", ~30 frames each, with hard cuts between them
(the rapid second-half cameo barrage begins here):

  * Chen  (local 0-29, B-on-W): cat ears + a little star ornament poking through a
           mob cap, one paw raised near her face -- the 16->17 cut target (ref f3571).
  * Ran   (local 30-59, B-on-W): big-hatted profile head facing left, fox ears,
           hanging tails (ref f3616).
  * Tewi  (local 60-89, W-on-B): a hard POLARITY FLIP into Tewi's white
           rabbit-eared face (ref f3646 is the mid-flip frame).

16->17: continuous B-on-W -- cut from Lyrica's wave to Chen.
17->18: Tewi's face (W-on-B) hands off to Reisen full-body (Scene 18 stays W-on-B).
Built inline; quick hard cuts between the three portraits are correct here.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: E402,F403
from shapes import (  # noqa: E402
    ellipse_poly, ribbon, head, mob_cap, dress_body, draw_polys, transform_polys,
)

SCENE_START_FRAME = 3570
SCENE_END_FRAME = 3660
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / 30.0   # 3.0 s

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")


# ---------------------------------------------------------------------------
# Small portrait-specific features
# ---------------------------------------------------------------------------

def cat_ear(cx, base_y, w=18, h=42, lean=0.0):
    return [[(cx - w, base_y), (cx + w, base_y), (cx + lean, base_y - h)]]


def star(cx, cy, r=12):
    pts = []
    for k in range(10):
        rr = r if k % 2 == 0 else r * 0.42
        a = -math.pi / 2 + math.pi * k / 5
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return [pts]


def rabbit_ear(bx, by, dx, up, w=20):
    return ribbon([(bx, by), (bx + dx * 0.4, by - up * 0.5), (bx + dx, by - up)],
                  [w, w * 0.92, w * 0.5])


# ---------------------------------------------------------------------------
# The three portraits (black ink; Tewi is inverted to white in draw())
# ---------------------------------------------------------------------------

def chen():
    cx = 548
    polys = []
    # twin braided tails behind (she faces left, tails sweep back to the right)
    polys += ribbon([(cx + 30, 232), (cx + 70, 320), (cx + 58, 420)], [16, 12, 6])
    polys += ribbon([(cx + 48, 252), (cx + 100, 304), (cx + 114, 384)], [14, 10, 5])
    # shoulders / upper body, cut off at the frame bottom
    polys += dress_body(cx, 300, 430, 642, 62, 94, 150)
    # head + mob cap
    polys += head(cx, 228, 42)
    polys += mob_cap(cx, 208, 56, 32)
    # tall cat ears clearly poking above the cap, star ornament between them
    polys += cat_ear(cx - 30, 186, 23, 70, -10)
    polys += cat_ear(cx + 26, 186, 23, 70, 10)
    polys += star(cx - 2, 108, 13)
    # raised paw near the face (screen-left)
    polys += ribbon([(cx - 44, 322), (cx - 80, 272), (cx - 88, 232)], [16, 12, 9])
    polys += ellipse_poly(cx - 92, 224, 19, 17)
    return polys


def ran():
    cx = 470
    polys = []
    # hanging tails / tassels down the back (right side)
    polys += ribbon([(cx + 74, 250), (cx + 96, 350), (cx + 86, 470)], [22, 15, 7])
    polys += ribbon([(cx + 104, 276), (cx + 136, 366), (cx + 150, 462)], [16, 10, 5])
    # big rounded hat / hair mass
    polys += ellipse_poly(cx + 4, 180, 100, 82)
    # fox ears poking up from the hat
    polys += [[(cx - 34, 128), (cx - 2, 118), (cx - 22, 58)]]
    polys += [[(cx + 36, 128), (cx + 66, 120), (cx + 48, 64)]]
    # tassel hanging from the hat front
    polys += ribbon([(cx - 58, 150), (cx - 66, 210)], [5, 3])
    polys += ellipse_poly(cx - 66, 218, 9, 12)
    # profile head facing LEFT
    polys += ellipse_poly(cx - 18, 256, 64, 74)
    polys += [[(cx - 78, 248), (cx - 104, 262), (cx - 78, 276)]]   # nose
    polys += [[(cx - 74, 292), (cx - 90, 310), (cx - 58, 304)]]    # chin
    polys += [[(cx - 70, 200), (cx - 92, 250), (cx - 66, 252), (cx - 44, 210)]]  # bangs
    # shoulders
    polys += dress_body(cx + 6, 332, 452, 642, 58, 98, 162)
    return polys


def tewi():
    cx = 480
    polys = []
    # two tall rabbit ears
    polys += rabbit_ear(cx - 34, 200, -12, 150, 22)
    polys += rabbit_ear(cx + 34, 200, 12, 150, 22)
    # hair mass behind, then the close-up face on top
    polys += ellipse_poly(cx, 256, 92, 86)
    polys += head(cx, 262, 78)
    # short bob fringe poking past the cheeks
    polys += [[(cx - 78, 250), (cx - 92, 320), (cx - 64, 314)]]
    polys += [[(cx + 78, 250), (cx + 92, 320), (cx + 64, 314)]]
    # shoulders below
    polys += dress_body(cx, 352, 470, 642, 72, 112, 172)
    return polys


def draw(c, u, i, t):
    bob = 4.0 * math.sin(i * 0.5)
    if i < 30:
        draw_polys(c, transform_polys(chen(), translate=(0, bob)))
    elif i < 60:
        draw_polys(c, transform_polys(ran(), translate=(0, bob)))
    else:
        draw_polys(c, transform_polys(tewi(), translate=(0, bob)))
        c.invert()                        # hard polarity flip -> Tewi W-on-B


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw)
    print(f"Scene 17: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

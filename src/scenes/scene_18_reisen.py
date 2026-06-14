"""Scene 18 -- Reisen's finger-gun beam splits the screen (f3660-3750, 90 fr).

W-on-B throughout (continues Scene 17's Tewi). Reisen -- long hair, tall rabbit
ears -- is first seen from behind (ref f3691), then turns side-on (a horizontal
squash sells the turn) and levels her arm into her trademark FINGER-GUN pose and
fires (ref f3736). The shot's trace remains as a thin horizontal white line that
cuts the whole screen in two (ref f3766, just past this scene's end), persisting
as the 18->19 handoff: Momiji answers the horizontal cut with a vertical one.

17->18: continuous W-on-B (Tewi -> Reisen). 18->19: the horizontal beam at
BEAM_Y persists into Scene 19. Built inline.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: E402,F403
from shapes import (  # noqa: E402
    ellipse_poly, ribbon, head, dress_body, long_hair, limb, draw_polys,
)

SCENE_START_FRAME = 3660
SCENE_END_FRAME = 3750
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / 30.0   # 3.0 s

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

BEAM_Y = 336        # height of the horizontal beam (shared with Scene 19)
HAND_X = 360        # where the finger-gun hand ends up (beam grows out from here)


def rabbit_ear(bx, by, dx, up, w=22):
    return ribbon([(bx, by), (bx + dx * 0.4, by - up * 0.5), (bx + dx, by - up)],
                  [w, w * 0.92, w * 0.5])


def squash_x(polys, factor, ox):
    """Non-uniform horizontal squash about x=ox (fakes a turn)."""
    return [[(ox + (x - ox) * factor, y) for x, y in p] for p in polys]


def reisen_rear():
    cx = 500
    polys = []
    polys += rabbit_ear(cx - 30, 150, -14, 162, 24)
    polys += rabbit_ear(cx + 30, 150, 14, 162, 24)
    polys += ellipse_poly(cx, 196, 50, 56)            # back of head
    polys += long_hair(cx, 188, 72, 300)              # long hair down the back
    polys += dress_body(cx, 240, 380, 600, 64, 84, 140)
    polys += limb([(cx - 26, 580), (cx - 30, 660), (cx - 32, 706)], [18, 14, 11])
    polys += limb([(cx + 26, 580), (cx + 30, 660), (cx + 32, 706)], [18, 14, 11])
    polys += limb([(cx - 60, 252), (cx - 92, 340), (cx - 96, 412)], [15, 12, 9])
    polys += limb([(cx + 60, 252), (cx + 92, 340), (cx + 96, 412)], [15, 12, 9])
    return polys


def reisen_fire(arm=1.0):
    """Side-on Reisen facing left; *arm* raises the lead arm into the firing pose."""
    cx = 532
    polys = []
    polys += rabbit_ear(cx - 4, 150, -16, 156, 22)
    polys += rabbit_ear(cx + 30, 150, 14, 156, 22)
    polys += long_hair(cx + 26, 186, 42, 226)         # hair trailing behind
    polys += head(cx + 4, 196, 42)
    polys += dress_body(cx, 238, 372, 590, 56, 72, 124)
    polys += limb([(cx - 18, 568), (cx - 24, 652), (cx - 26, 704)], [16, 13, 11])
    polys += limb([(cx + 22, 568), (cx + 28, 652), (cx + 30, 704)], [16, 13, 11])
    # trailing (back) arm hanging down
    polys += limb([(cx + 42, 256), (cx + 60, 330), (cx + 52, 396)], [14, 11, 8])
    # lead arm: rest (down) -> extended horizontal finger-gun
    sx, sy = cx - 34, 256
    hx = lerp(cx - 28, HAND_X, arm)
    hy = lerp(370, BEAM_Y, arm)
    ex = lerp(cx - 52, (sx + hx) / 2 - 8, arm)
    ey = lerp(330, (sy + hy) / 2 - 6, arm)
    polys += limb([(sx, sy), (ex, ey), (hx, hy)], [14, 11, 8])
    # pointing finger-gun hand
    polys += [[(hx, hy - 9), (hx - 34, hy - 5), (hx - 34, hy + 4), (hx, hy + 9)]]
    return polys


def draw_beam(c, extent):
    if extent <= 0:
        return
    lx = lerp(HAND_X, 0, extent)
    rx = lerp(HAND_X, 960, extent)
    c.rectangle(lx, BEAM_Y - 4, rx, BEAM_Y + 4)       # white (bg is black)


def draw(c, u, i, t):
    if i < 26:                                        # rear view, slight sway
        sway = 6.0 * math.sin(i * 0.18)
        polys = reisen_rear()
        draw_polys(c, [[(x + sway, y) for x, y in p] for p in polys])
    elif i < 34:                                      # turn out (squash the rear thin)
        e = ease((i - 26) / 8.0, "in")
        draw_polys(c, squash_x(reisen_rear(), lerp(1.0, 0.16, e), 500))
    elif i < 44:                                      # turn in (expand the side view)
        e = ease((i - 34) / 10.0, "out")
        draw_polys(c, squash_x(reisen_fire(0.0), lerp(0.16, 1.0, e), 532))
    else:                                             # raise arm, then fire
        arm = ease(clamp01((i - 44) / 22.0), "in_out")
        draw_polys(c, reisen_fire(arm))
        if i >= 70:
            draw_beam(c, ease(clamp01((i - 70) / 15.0), "out"))


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME, )
    n = render_scene(writer, SCENE_DURATION, draw, bg=BLACK)
    print(f"Scene 18: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

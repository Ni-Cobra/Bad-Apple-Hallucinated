"""Scene 14 -- Eirin and the full moon (f2970-3150, 180 frames, W-on-B).

Continues Scene 13's handoff: opens on the clean white moon at (372,272) r=120
on black (Scene 13's exact end state). Over the first second the camera settles
the moon to the upper-LEFT (and a soft gray glow blooms around it -- the only
gray element here, the documented moon halo). Eirin rises in at the RIGHT, head
bowed (ref f3001 ~local 30), then reaches her arm out toward the moon (ref f3091
~local 120) and -- renouncing it -- lowers the arm as the camera swings: a pure
horizontal pan carries the moon to the top-RIGHT while Eirin slides off the right
edge. The constant moon<->Eirin gap means they never overlap during the pan.

14->15 handoff: last frame is the glowing moon at the TOP-RIGHT ~(820,218) r=146
on otherwise-black, left side clear -- Scene 15 (Kaguya) mirrors this composition,
entering from the left.

Eirin is built inline from the toolkit idiom (peaked nurse cap + long single
braid + floor-length gown), her identifying silhouette features.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: E402,F403
from shapes import (  # noqa: E402
    circle_poly, ellipse_poly, ribbon, transform_polys, draw_polys, head,
)

SCENE_START_FRAME = 2970
SCENE_END_FRAME = 3150
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / 30.0   # 6.0 s

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

BX = 655          # Eirin's body-centre x at rest (she stands at the right)


# ---------------------------------------------------------------------------
# The moon with its soft gray glow (the one documented gray element here)
# ---------------------------------------------------------------------------

def draw_moon(c, cx, cy, r, halo_t):
    """White lunar disc with a soft gray halo ramped in by *halo_t* in [0,1].

    Scene 13 handed off a hard-edged disc; halo_t lets the glow bloom in over
    the first frames so the boundary stays continuous.
    """
    rings = 8
    for k in range(rings, 0, -1):
        f = k / rings                       # 1.0 (outer) .. ~0.1 (inner)
        rad = r * (1.0 + 0.85 * f)
        gray = int(halo_t * (210 * (1.0 - f) ** 1.6))
        if gray > 0:
            c.circle(cx, cy, rad, color=gray)
    c.circle(cx, cy, r, color=WHITE)


# ---------------------------------------------------------------------------
# Eirin (inline) -- facing LEFT toward the moon
# ---------------------------------------------------------------------------

def eirin(reach=0.0, bow=1.0):
    """Eirin Yagokoro as a white silhouette, facing left.

    *reach* in [0,1] swings the near arm from at-her-side up toward the moon.
    *bow* in [0,1] tilts the head/cap forward-down (bowed when not reaching).
    """
    polys = []
    hx = BX - 6 - 6 * bow
    hy = 176 + 11 * bow

    # long single braid down the back (right side) -- her signature
    polys += ribbon([(BX + 14, 150), (BX + 30, 280), (BX + 40, 420),
                     (BX + 34, 540)], [16, 21, 15, 4])

    # back/far arm, hanging at the side (adds bulk behind the gown)
    polys += ribbon([(BX + 40, 236), (BX + 56, 332), (BX + 52, 424)],
                    [14, 11, 7])

    # floor-length gown: vertical front (left), billowing train (right)
    polys.append([
        (BX - 44, 226), (BX + 44, 224),                       # shoulders
        (BX + 52, 300), (BX + 64, 430), (BX + 112, 600),
        (BX + 150, 700),                                       # back train, bottom-right
        (BX - 96, 700),                                        # hem bottom-left
        (BX - 78, 540), (BX - 64, 400), (BX - 54, 300),       # vertical front edge
    ])

    # head + peaked nurse cap (forward-leaning peak)
    polys += head(hx, hy, 42)
    polys.append([(hx - 36, hy - 24), (hx + 22, hy - 28),
                  (hx - 22, hy - 78)])                          # peak tip up-forward
    # small front fringe of hair
    polys.append([(hx - 38, hy - 6), (hx - 30, hy + 34),
                  (hx - 16, hy + 30), (hx - 24, hy - 8)])

    # near/front arm -- swings up to reach the moon (upper-left)
    handx = lerp(BX - 52, BX - 214, reach)
    handy = lerp(392, 318, reach)
    elbowx = lerp(BX - 56, BX - 122, reach)
    elbowy = lerp(322, 330, reach)
    polys += ribbon([(BX - 42, 234), (elbowx, elbowy), (handx, handy)],
                    [16, 12, 7])
    return polys


# ---------------------------------------------------------------------------
# Composition over the scene
# ---------------------------------------------------------------------------

def state(i):
    """Return (moon (cx,cy,r), halo_t, pan_dx, eirin_yoff, reach_t) for frame i."""
    halo_t = ease(clamp01(i / 18.0), "out")

    if i <= 30:                                  # camera settles to the upper-left
        u = ease(i / 30.0, "in_out")
        mcx, mcy, mr = lerp(372, 130, u), lerp(272, 218, u), lerp(120, 146, u)
        pan = 0.0
    elif i <= 130:                               # hold the composition
        mcx, mcy, mr, pan = 130.0, 218.0, 146.0, 0.0
    else:                                        # camera swings: pure pan to the right
        u = ease((i - 130) / 49.0, "in_out")
        pan = lerp(0.0, 690.0, u)
        mcx, mcy, mr = 130.0 + pan, 218.0, 146.0

    yoff = lerp(140.0, 0.0, ease(clamp01(i / 26.0), "out"))   # Eirin rises in

    if i < 95:
        reach = 0.0
    elif i < 120:
        reach = ease((i - 95) / 25.0, "in_out")
    elif i < 134:
        reach = 1.0
    else:
        reach = lerp(1.0, 0.0, ease(clamp01((i - 134) / 22.0), "in_out"))
    return (mcx, mcy, mr), halo_t, pan, yoff, reach


def draw(c, u, i, t):
    (mcx, mcy, mr), halo_t, pan, yoff, reach = state(i)
    draw_moon(c, mcx, mcy, mr, halo_t)
    polys = eirin(reach=reach, bow=1.0 - reach)
    polys = transform_polys(polys, translate=(pan, yoff))
    draw_polys(c, polys)


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw, bg=BLACK)
    print(f"Scene 14: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

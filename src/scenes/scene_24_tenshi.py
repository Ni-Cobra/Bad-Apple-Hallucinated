"""Scene 24 -- Tenshi's swagger; the face-off (f4410-4650, 240 fr). W-on-B.

Revealed from behind Yukari's fan, Tenshi plants her hands on her hips in a cocky
full-body pose under a diagonal spotlight beam from the top-right corner (ref
f4426). She gestures grandly, flicking her long hair (ref f4501), then a close-up
holding up her peach/keystone (ref f4561). Quick alternating shots of Yukari and
Tenshi end with the two facing each other in profile, noses almost touching
(lean-in, ref f4621).

23->24: continuous W-on-B (fan shut -> Tenshi). 24->25: figure-ground FLIP -- the
black negative space BETWEEN the two white profiles is re-read as Aya's black
crow wing (Scene 25 flips to B-on-W). This scene ends on that two-profile face-off
so Scene 25 can invert it.

Tenshi from the shared tenshi() builder; the profile heads built inline from the
shared toolkit (mob_cap/head/long_hair + the peaked-hat feature).
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: E402,F403
from shapes import (  # noqa: E402
    head, mob_cap, long_hair, ellipse_poly, draw_polys, transform_polys, tenshi,
)

SCENE_START_FRAME = 4410
SCENE_END_FRAME = 4650
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / 30.0   # 8.0 s

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

A_END = 66          # full-body swagger in the corner spotlight (ref f4426)
B_END = 130         # push in; grand gesture + hair flick (ref f4501)
C_END = 188         # close-up holding up the peach (ref f4561)
D1_END = 206        # quick cut to Yukari
# 206..239 -> two-profile lean-in face-off (ref f4621)


def spotlight(c):
    """A bright white diagonal beam from the top-right corner (ref f4426)."""
    c.polygon([(700, 0), (960, 0), (960, 250)], color=WHITE)


def yukari_profile_head(cx, cy, face=1, scale=1.0):
    """Yukari's profile head: mob cap + head + nose, facing +x (face=1)/-x."""
    polys = []
    polys += long_hair(cx - 26 * face, cy - 4, 48, 230)
    polys += head(cx, cy, 50)
    polys += mob_cap(cx, cy - 32, 82, 50)
    polys += [[(cx + 48 * face, cy - 10), (cx + 74 * face, cy + 6),
               (cx + 46 * face, cy + 20)]]                    # nose
    if scale != 1.0:
        polys = transform_polys(polys, scale=scale, origin=(cx, cy))
    return polys


def tenshi_profile_head(cx, cy, face=-1, scale=1.0):
    """Tenshi's profile head: peaked hat + head + nose, facing -x (face=-1)/+x."""
    polys = []
    R = 50
    polys += long_hair(cx - 26 * face, cy - 4, 50, 240)
    polys += head(cx, cy, R)
    cyt = cy - R * 0.72
    polys += ellipse_poly(cx, cyt, 48, 22)
    polys += [[(cx - 16, cyt - 2), (cx - 86, cyt - 46), (cx - 34, cyt - 16)]]
    polys += [[(cx + 16, cyt - 2), (cx + 86, cyt - 46), (cx + 34, cyt - 16)]]
    polys += [[(cx - 13, cyt - 6), (cx, cyt - 50), (cx + 13, cyt - 6)]]
    polys += [[(cx + 48 * face, cy - 10), (cx + 74 * face, cy + 6),
               (cx + 46 * face, cy + 20)]]                    # nose
    if scale != 1.0:
        polys = transform_polys(polys, scale=scale, origin=(cx, cy))
    return polys


def draw(c, u, i, t):
    # ---- Phase A: corner spotlight, full-body hands-on-hips swagger ----------
    if i < A_END:
        spotlight(c)
        # small white ground pool under her (the lit spot)
        c.ellipse(480, 560, 92, 16, color=WHITE)
        draw_polys(c, tenshi(480, 548, scale=0.62, pose="hips"))
        return

    # ---- Phase B: push in; grand gesture + hair flick -----------------------
    if i < B_END:
        b = (i - A_END) / float(B_END - A_END)
        spotlight(c)
        scale = lerp(0.62, 1.06, ease(b, "in_out"))
        foot = lerp(548, 760, ease(b, "in_out"))         # camera pushes in
        draw_polys(c, tenshi(480, foot, scale=scale, pose="flick"))
        return

    # ---- Phase C: close-up holding up the peach -----------------------------
    if i < C_END:
        cprog = (i - B_END) / float(C_END - B_END)
        scale = lerp(1.06, 1.5, ease(cprog, "in_out"))
        foot = lerp(760, 980, ease(cprog, "in_out"))
        draw_polys(c, tenshi(470, foot, scale=scale, pose="peach"))
        return

    # ---- Phase D1: quick cut to Yukari --------------------------------------
    if i < D1_END:
        draw_polys(c, yukari_profile_head(470, 350, face=1, scale=1.7))
        return

    # ---- Phase D2: two-profile lean-in face-off (ref f4621) -----------------
    d = (i - D1_END) / float(SCENE_END_FRAME - SCENE_START_FRAME - D1_END)
    lean = ease(d, "in_out")
    # Yukari (left, facing right) and Tenshi (right, facing left) lean toward x=480
    yx = lerp(300, 372, lean)
    tx = lerp(660, 588, lean)
    draw_polys(c, yukari_profile_head(yx, 348, face=1, scale=1.5))
    draw_polys(c, tenshi_profile_head(tx, 348, face=-1, scale=1.5))


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw, bg=BLACK)
    print(f"Scene 24: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

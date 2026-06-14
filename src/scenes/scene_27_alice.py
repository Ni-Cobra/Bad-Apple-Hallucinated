"""Scene 27 -- Alice drops her doll (f5040-5220, 180 fr). B-on-W.

26->27: the last sake drop (Scene 26's end, the shared drop() falling near
(452,206)) morphs into a BIRD'S-EYE view of Alice standing far below, doll in hand
(the only top-down camera in the video, ref f5086). Cut to profile: Alice
(short bob + hairband) holds her DOLL up on her open palm, regarding it (ref
f5161). Then she simply LETS IT FALL -- the doll tumbles alone through the white
frame (ref f5221).

27->28: the falling doll morphs into Nitori (Scene 28 continues from the tumbling
shared doll() shape).

Alice built inline from the toolkit; drop()/doll() are the shared handoff shapes.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: E402,F403
from shapes import (  # noqa: E402
    head, ellipse_poly, circle_poly, ribbon, draw_polys, transform_polys,
    drop, doll,
)

SCENE_START_FRAME = 5040
SCENE_END_FRAME = 5220
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / 30.0   # 6.0 s

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

A_END = 50          # drop -> overhead (bird's-eye) Alice (ref f5086)
B_END = 132         # cut to profile: holds the doll up on her palm (ref f5161)
# 132..179 -> lets the doll fall; it tumbles alone (ref f5221)

DOLL_HX, DOLL_HY = 332, 408     # where the doll rests on her palm (profile shot)


def overhead_alice(cx, cy, s=1.0):
    """Alice seen from directly ABOVE: top of the head, a rounded back/shoulders
    mass, and a small arm reaching out with the doll (the only top-down shot)."""
    polys = []
    polys += ellipse_poly(cx, cy + 16 * s, 42 * s, 46 * s)      # back / shoulders
    polys += circle_poly(cx, cy - 20 * s, 25 * s)               # crown of the head
    polys += ribbon([(cx + 20 * s, cy + 4 * s), (cx + 40 * s, cy + 16 * s)],
                    [10 * s, 6 * s])                            # arm
    polys += circle_poly(cx + 50 * s, cy + 20 * s, 12 * s)      # doll held out
    return polys


def alice_profile(hx, hy, scale=1.0, hold_doll=True):
    """Alice in profile facing LEFT: rounded head with a short bob + hairband,
    body descending off-frame, near arm reaching down-left to hold the doll up."""
    R = 50
    polys = []
    # short bob hair massed behind the head (to the right), jaw length
    polys += [[(hx + 4, hy - R * 0.96), (hx + R * 0.92, hy - R * 0.68),
               (hx + R * 1.06, hy - R * 0.02), (hx + R * 0.95, hy + R * 0.62),
               (hx + R * 0.66, hy + R * 0.92), (hx + R * 0.18, hy + R * 0.74),
               (hx + 8, hy + R * 0.46)]]
    polys += head(hx, hy, R)
    # hairband: a thin arch band over the crown (Alice's feature)
    polys += [[(hx - R * 0.62, hy - R * 0.74), (hx - R * 0.28, hy - R * 1.16),
               (hx + R * 0.5, hy - R * 1.02), (hx + R * 0.5, hy - R * 0.84),
               (hx - R * 0.24, hy - R * 0.96)]]
    polys += [[(hx - R * 0.9, hy - 4), (hx - R * 1.2, hy + 5), (hx - R * 0.86, hy + 16)]]  # nose
    neck_y = hy + R * 0.84
    polys += [[(hx - 16, neck_y), (hx + 18, neck_y), (hx + 20, neck_y + 30), (hx - 18, neck_y + 30)]]
    polys += [[(hx - 32, neck_y + 24), (hx + 34, neck_y + 24),
               (hx + 54, neck_y + 280), (hx - 48, neck_y + 280)]]   # torso descending off-frame
    if hold_doll:
        polys += ribbon([(hx - 18, neck_y + 46), (hx - 96, neck_y + 116),
                         (DOLL_HX + 8, DOLL_HY + 34)], [16, 12, 9])  # arm to the palm
    if scale != 1.0:
        polys = transform_polys(polys, scale=scale, origin=(hx, hy))
    return polys


def draw(c, u, i, t):
    # ---- Phase A: drop -> overhead Alice ------------------------------------
    if i < A_END:
        if i < 24:                              # the drop falls and morphs into the body mass
            m = ease(i / 24.0, "in_out")
            dx, dy = lerp(406, 442, m), lerp(239, 372, m)   # continues Scene 26's drop
            drop_poly = drop(dx, dy, r=lerp(20, 46, m))[0]
            body = ellipse_poly(442, 388, 42, 46)[0]
            draw_polys(c, [morph_polys(drop_poly, body, m, n=64)])
            if m > 0.45:                        # crown of the head grows up as it resolves
                g = ease(clamp01((m - 0.45) / 0.55), "out")
                draw_polys(c, circle_poly(442, 372, 25 * g))
            return
        g = ease((i - 24) / float(A_END - 24), "out")
        draw_polys(c, overhead_alice(442, 388, s=lerp(0.9, 1.0, g)))
        return

    # ---- Phase B: cut to profile, holding the doll up on her palm -----------
    if i < B_END:
        b = (i - A_END) / float(B_END - A_END)
        # gentle "regarding" motion: tiny head bob + the held doll lifts a hair
        bob = 5 * math.sin(b * math.pi * 2)
        draw_polys(c, alice_profile(584, 206 + bob, scale=1.0))
        draw_polys(c, doll(DOLL_HX, DOLL_HY - bob * 0.6, scale=1.18))
        return

    # ---- Phase C: lets the doll fall; it tumbles alone (handoff) ------------
    cp = (i - B_END) / float(SCENE_END_FRAME - SCENE_START_FRAME - B_END)   # 0..1
    if cp < 0.45:                               # she's still there, hand opening / lowering
        draw_polys(c, alice_profile(584, 206, scale=1.0, hold_doll=cp < 0.18))
    p = ease(cp, "in")
    dx = lerp(DOLL_HX, 446, p)
    dy = lerp(DOLL_HY, 352, p) + 120 * p * p    # accelerating fall (camera follows)
    ang = 3.4 * p                               # tumbling
    draw_polys(c, transform_polys(doll(dx, dy, scale=1.18), rotate=ang, origin=(dx, dy)))


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw)              # B-on-W (default)
    print(f"Scene 27: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

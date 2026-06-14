"""Scene 28 -- Nitori's chase and dive (f5220-5430, 210 fr).
B-on-W -> flips to W-on-B with the splash (end of chorus 2, lyric "turn white").

27->28: the falling doll (Scene 27's end, the shared doll() tumbling near
(446,472)) morphs into Nitori, who hits the ground RUNNING (dynamic run, ref
f5251). Close-up of her ARM reaching out, fingers spread, to grab what she chases
(ref f5341). She DIVES headlong; the impact throws up a FOUNTAIN of white spray on
black (ref f5431) -- the polarity inversion lands exactly on the "turn white"
lyric and the section seam.

28->29: the spray hangs in the air and becomes flower petals -- the plume rises
into the shared SPLASH_FIELD positions, which Scene 29 morphs into petals.

Nitori built inline from the toolkit; doll() + SPLASH_FIELD are the shared handoffs.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: E402,F403
from shapes import (  # noqa: E402
    head, ellipse_poly, ribbon, draw_polys, transform_polys,
    doll, SPLASH_FIELD,
)

SCENE_START_FRAME = 5220
SCENE_END_FRAME = 5430
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / 30.0   # 7.0 s

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

A_END = 55          # doll -> Nitori, hits the ground running (ref f5251)
B_END = 125         # close-up: arm reaching out, fingers spread (ref f5341)
DIVE_END = 168      # dives headlong
# 168..209 -> impact: white spray fountain on black, flipped to W-on-B (ref f5431)

IMPACT = (470, 700)


def nitori_run(cx, cy, scale=1.0):
    """Nitori mid-run, dynamic, facing RIGHT: a low cap with a short brim, two
    braids streaming back-left, body leaning forward, skirt flaring back, legs
    striding. (cx,cy) is the waist anchor; figure ~370 px tall."""
    R = 42
    polys = []
    hx, hy = cx + 42, cy - 150                  # head forward (leaning right)
    polys += ribbon([(hx - 26, hy + 6), (hx - 92, hy + 28), (hx - 156, hy + 16)], [16, 11, 4])  # braid
    polys += ribbon([(hx - 24, hy + 24), (hx - 88, hy + 64), (hx - 152, hy + 70)], [14, 10, 4])  # braid
    polys += head(hx, hy, R)
    polys += ellipse_poly(hx, hy - R * 0.66, 44, 22)                                   # cap dome
    polys += [[(hx + R * 0.5, hy - R * 0.7), (hx + R * 1.4, hy - R * 0.5), (hx + R * 0.5, hy - R * 0.34)]]  # brim
    neck_y = hy + R * 0.8
    polys += [[(hx - 30, neck_y), (hx + 24, neck_y), (cx + 18, cy), (cx - 34, cy)]]    # torso, leaning
    polys += [[(cx - 34, cy), (cx + 18, cy), (cx + 30, cy + 72), (cx - 80, cy + 88)]]  # skirt flaring back
    polys += ribbon([(cx - 12, cy + 60), (cx - 58, cy + 120), (cx - 96, cy + 150)], [16, 12, 8])  # back leg
    polys += ribbon([(cx + 8, cy + 64), (cx + 32, cy + 150), (cx + 26, cy + 218)], [16, 13, 9])   # front leg
    polys += ribbon([(cx + 6, neck_y + 20), (cx + 72, cy - 8), (cx + 122, cy - 30)], [14, 11, 7])  # reaching arm
    polys += ribbon([(cx - 24, neck_y + 18), (cx - 72, cy + 10), (cx - 108, cy - 2)], [14, 10, 6])  # trailing arm
    if scale != 1.0:
        polys = transform_polys(polys, scale=scale, origin=(cx, cy))
    return polys


def reaching_arm(spread=1.0, scale=1.0):
    """Close-up of a forearm entering from the lower-right, hand and spread
    fingers reaching to the upper-left (ref f5341). *spread* fans the fingers."""
    polys = []
    polys += ribbon([(960, 372), (650, 220), (392, 132)], [78, 60, 40])     # forearm
    palm = (372, 132)
    polys += [[(palm[0] + 36, palm[1] + 30), (palm[0] - 4, palm[1] + 44),
               (palm[0] - 40, palm[1] + 14), (palm[0] - 22, palm[1] - 30),
               (palm[0] + 28, palm[1] - 22)]]                               # palm wedge
    base_ang = -2.05
    for k in range(5):
        ang = base_ang - spread * (0.62 * (k - 2) / 2.0) - 0.5 * spread
        ln = [70, 96, 104, 96, 74][k]
        fx = palm[0] - 10 + ln * math.cos(ang)
        fy = palm[1] - 6 + ln * math.sin(ang)
        polys += ribbon([(palm[0] - 10, palm[1] - 4), (fx, fy)], [14 - k * 0.6, 6])
    if scale != 1.0:
        polys = transform_polys(polys, scale=scale, origin=(560, 220))
    return polys


def draw(c, u, i, t):
    # ---- Phase A: doll -> Nitori, hits the ground running -------------------
    if i < A_END:
        if i < 22:                              # the tumbling doll morphs/grows up
            m = ease(i / 22.0, "in_out")
            dx, dy = lerp(446, 442, m), lerp(472, 430, m)
            draw_polys(c, transform_polys(doll(dx, dy, scale=lerp(1.18, 2.7, m)),
                                          rotate=lerp(3.4, 6.1, m), origin=(dx, dy)))
            return
        g = ease((i - 22) / float(A_END - 22), "out")
        bob = 6 * math.sin((i - 22) * 0.5)
        draw_polys(c, nitori_run(440, 384 + bob, scale=lerp(0.84, 1.0, g)))
        return

    # ---- Phase B: close-up, arm reaching out, fingers spread ----------------
    if i < B_END:
        b = (i - A_END) / float(B_END - A_END)
        draw_polys(c, reaching_arm(spread=ease(b, "out"), scale=lerp(0.92, 1.04, b)))
        return

    # ---- Phase C1: dives headlong -------------------------------------------
    if i < DIVE_END:
        d = ease((i - B_END) / float(DIVE_END - B_END), "in")
        nx, ny = lerp(430, 470, d), lerp(286, 612, d)
        body = nitori_run(nx, ny, scale=lerp(1.0, 0.66, d))
        draw_polys(c, transform_polys(body, rotate=lerp(0.25, 1.55, d), origin=(nx, ny)))
        return

    # ---- Phase C2: impact -- white spray fountain on black (W-on-B flip) ----
    c.fill(BLACK)
    sp = (i - DIVE_END) / float(SCENE_END_FRAME - SCENE_START_FRAME - DIVE_END)   # 0..1
    for sx, sy, ss in SPLASH_FIELD:
        synorm = (700 - sy) / 612.0                      # 0 bottom .. 1 top of plume
        delay = 0.42 * synorm                            # higher droplets arrive later
        pr = ease(clamp01((sp - delay) / (1 - delay + 1e-6)), "out")
        px = lerp(IMPACT[0], sx, pr)
        py = lerp(IMPACT[1], sy, pr)
        rad = ss * clamp01(pr * 2.4)
        if rad > 0.4:
            c.circle(px, py, rad, color=WHITE)


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw)              # B-on-W; flips to W-on-B at impact
    print(f"Scene 28: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

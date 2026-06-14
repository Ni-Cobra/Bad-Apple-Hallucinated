"""Scene 22 -- Kanako & Suwako; the gap "switches the TV off"
(f3990-4230, 240 fr). B-on-W.

Kanako appears first, tall and stately in a long dress, profile (ref f4021).
Suwako then pops up HAT-FIRST -- her broad flat hat rising before her body --
and lands in a goofy frog-like arms-out pose (both verified f4081). The camera
pushes in to a back-to-back two-shot pose (ref f4171). They exit via what looks
like an old TV switching off: the frame collapses into a horizontal eye-shaped
slit with a white octagon centre (ref f4231).

21->22: Hina's spin clears the stage; Kanako rises in (B-on-W). 22->23: the
"TV-off" slit IS one of Yukari's gaps (sukima) -- Scene 23 flips to W-on-B and
Yukari emerges from it. End state matches shared gap_sukima: a black almond lens
centred at (480,360), half-height ~78 px, with a white octagon (r~56) centre.
Kanako/Suwako built inline (Suwako's flat hat is the identifying feature; per
PROJECT.md sec.4 gray discipline NO floor shadows here -- gray is reserved).
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: E402,F403
from shapes import (  # noqa: E402
    ellipse_poly, circle_poly, head, ribbon, draw_polys, transform_polys,
)

SCENE_START_FRAME = 3990
SCENE_END_FRAME = 4230
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / 30.0   # 8.0 s

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

# local-frame phase boundaries
A_END = 58          # Kanako established at left
B_END = 120         # Suwako popped up hat-first, both posing
C_END = 198         # camera pushed in to the back-to-back two-shot
# 198..239 -> TV-off collapse to the gap


def kanako(cx, foot_y, scale=1.0, face=-1):
    """Tall stately Kanako in profile, long floor-length dress (ref f4021).

    Authored facing LEFT (nose/bust to the left, hair bulging back-right) with a
    real front-to-back width that never collapses; face=+1 mirrors the whole
    silhouette so the body keeps its depth either way.
    """
    polys = []
    hy = foot_y - 470          # head centre; figure ~ 520 px tall
    R = 50
    polys += ellipse_poly(cx + 14, hy - 2, R * 0.96, R * 1.08)   # hair mass (back = right)
    polys += ellipse_poly(cx + 6, hy - R * 1.02, 14, 20)         # small top ornament
    polys += head(cx - 4, hy, R * 0.9)
    polys += [[(cx - R * 0.86, hy - 16), (cx - R * 1.18, hy + 4),
               (cx - R * 0.86, hy + 26)]]                        # nose (faces left)
    neck_y = hy + R * 0.9
    polys += [[(cx - 16, neck_y), (cx + 16, neck_y),
               (cx + 16, neck_y + 28), (cx - 16, neck_y + 28)]]  # neck
    by = neck_y + 26
    # bodice: real width, bust bulging toward the front (left)
    polys += [[(cx - 30, by), (cx + 34, by + 4),
               (cx + 40, by + 116), (cx - 46, by + 120)]]
    polys += ellipse_poly(cx - 34, by + 44, 22, 26)              # bust (front)
    waist_y = by + 116
    # long floor-length A-line skirt (proper width, slight back-sweep)
    polys += [[(cx - 44, waist_y), (cx + 44, waist_y),
               (cx + 78, foot_y - 10), (cx + 86, foot_y),
               (cx - 92, foot_y), (cx - 80, foot_y - 12)]]
    if face == 1:
        polys = [[(2 * cx - x, y) for x, y in p] for p in polys]
    if scale != 1.0:
        polys = transform_polys(polys, scale=scale, origin=(cx, foot_y))
    return polys


def suwako(cx, foot_y, scale=1.0, arm=1.0):
    """Short Suwako with her broad flat frog-hat (the identifying feature) and
    arms flung out in a goofy pose. *arm* scales how far the arms spread."""
    polys = []
    hy = foot_y - 210                       # shoulder line
    brim_y = hy - 96                         # hat brim line
    # broad flat hat: wide drooping brim
    polys += [[(cx - 156, brim_y), (cx - 70, brim_y - 16),
               (cx + 70, brim_y - 16), (cx + 156, brim_y),
               (cx + 78, brim_y + 30), (cx - 78, brim_y + 30)]]
    polys += ellipse_poly(cx, brim_y - 14, 50, 38)           # dome top
    polys += circle_poly(cx - 24, brim_y - 40, 13)           # frog-eye bump
    polys += circle_poly(cx + 24, brim_y - 40, 13)           # frog-eye bump
    polys += head(cx, hy - 50, 36)                           # head under hat
    polys += [[(cx - 46, hy - 16), (cx + 46, hy - 16),
               (cx + 60, foot_y), (cx - 60, foot_y)]]        # short dress/body
    # arms flung out to the sides (frog pose)
    polys += ribbon([(cx - 38, hy + 6), (cx - 104, hy + 2 - 6 * arm),
                     (cx - 150 * arm, hy + 30)], [15, 11, 7])
    polys += ribbon([(cx + 38, hy + 6), (cx + 104, hy + 2 - 6 * arm),
                     (cx + 150 * arm, hy + 30)], [15, 11, 7])
    if scale != 1.0:
        polys = transform_polys(polys, scale=scale, origin=(cx, foot_y))
    return polys


def octagon(cx, cy, r):
    return [(cx + r * math.cos(math.pi / 8 + k * math.pi / 4),
             cy + r * math.sin(math.pi / 8 + k * math.pi / 4)) for k in range(8)]


def tv_off(c, c01):
    """Collapse the (black) frame into the eye-shaped gap: white eyelids close
    from top and bottom leaving a black almond lens, then a white octagon iris
    opens at the centre. c01 in [0,1]; c01=1 is the final gap state."""
    c.fill(WHITE)
    W, yc = 960, 360
    e = ease(c01, "in_out")
    n = 72
    top, bot = [], []
    for k in range(n + 1):
        x = W * k / n
        final_half = 78 * math.sin(math.pi * x / W)     # almond/lens profile
        top.append((x, yc - lerp(360, final_half, e)))
    for k in range(n, -1, -1):
        x = W * k / n
        final_half = 78 * math.sin(math.pi * x / W)
        bot.append((x, yc + lerp(360, final_half, e)))
    c.polygon(top + bot, color=BLACK)
    # white octagon iris opens in the centre near the end
    orad = 56 * ease(clamp01((c01 - 0.5) / 0.5), "out")
    if orad > 2:
        c.polygon(octagon(480, yc, orad), color=WHITE)


def draw(c, u, i, t):
    if i >= C_END:
        tv_off(c, (i - C_END) / float(SCENE_END_FRAME - SCENE_START_FRAME - 1 - C_END))
        return

    polys = []
    # --- Kanako: rises in at the left, then established ---
    if i < A_END:
        ky = lerp(900, 660, ease(clamp01(i / 44.0), "out"))   # rise from below
    else:
        ky = 660
    polys += kanako(372, ky, face=-1)

    # --- Suwako: pops up HAT-FIRST from the bottom-right (frame edge clips her) ---
    if i >= 30:
        rise = ease(clamp01((i - 30) / 60.0), "out")
        sfoot = lerp(1240, 680, rise)        # starts fully below screen -> hat enters first
        polys += suwako(690, sfoot, arm=clamp01((i - 60) / 30.0))

    base = polys
    # --- camera push-in to the back-to-back two-shot (ref f4171) ---
    if i >= B_END:
        cs = (i - B_END) / float(C_END - B_END)
        scale = lerp(1.0, 2.0, ease(cs, "in_out"))
        base = transform_polys(base, scale=scale, origin=(500, 300),
                               translate=(0, 30 * ease(cs, "in_out")))
    draw_polys(c, base)
    # black bloom over the last push-in frames -> seamless into the TV-off black
    if i >= 184:
        e = ease(clamp01((i - 184) / float(C_END - 184)), "in")
        c.rectangle(480 - 480 * e, 360 - 360 * e, 480 + 480 * e, 360 + 360 * e)


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw)
    print(f"Scene 22: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

"""Scene 13 -- Keine x2 inside the blaze; the clockwise spin into the moon.
Frames 2790-2969 (180 fr).

SCENES.md: flames fill the screen (ref f2731, two figures emerging at the bottom).
Inside the fire the two Keine forms appear facing each other -- human Keine (left,
peaked historian cap) and horned hakutaku Keine (right) -- and clasp hands at the
centre (mirrored pair, ref f2881). The whole composition then rotates CLOCKWISE,
smearing into a spiral (ref f2941) that resolves into a full moon. Polarity is the
most fluid passage of the video: flame whiteout (B-on-W) -> the pair reads W-on-B
-> the spiral mixes both -> a clean white moon on black.

Continuity in (12->13): Scene 12 ended with the blaze engulfing the frame and two
forms emerging at the bottom; this scene opens on that whiteout and resolves it
into the Keine pair. Handoff out (13->14): the spiral becomes Scene 14's full
moon -- the last frame leaves a clean white moon drifting toward the upper-left
(Eirin's moon hangs top-LEFT). Built inline; gray fire allowed (PROJECT.md sec.4).
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: F401,F403
from shapes import (  # noqa: E402
    ellipse_poly, limb, ribbon, circle_poly, moon,
    draw_polys, transform_polys,
)

SCENE_START_FRAME = 2790
SCENE_END_FRAME = 2970
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / FPS  # 6.0 s
NFR = SCENE_END_FRAME - SCENE_START_FRAME                     # 180

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

CX, CY = 480, 360
A_END = 34        # the flame whiteout recedes, revealing the pair
CLASP = 92        # hands fully clasped (ref f2881)
SPIN = 100        # the clockwise spin begins
MOON_F = 150      # the spiral has resolved into the moon
MOON_END = (372, 272)   # final moon centre (drifting top-left for Scene 14)

GRAY_OUT, GRAY_MID, CORE = 118, 186, 246


def flame(c, cx, by, h, t, layers=3):
    cols = [GRAY_OUT, GRAY_MID, CORE]
    for k in range(layers):
        f = 1.0 - k / (layers + 0.4)
        hh, ww = h * f, h * 0.30 * f
        wob = 0.18 * math.sin(t * 7 + k * 1.3)
        wob2 = 0.14 * math.sin(t * 5 + k)
        c.polygon([
            (cx, by),
            (cx - ww, by - hh * 0.30),
            (cx - ww * 0.55 * (1 + wob), by - hh * 0.62),
            (cx - ww * 0.30, by - hh * 0.86),
            (cx + ww * 0.18 * (1 + wob2), by - hh),
            (cx + ww * 0.34, by - hh * 0.84),
            (cx + ww * 0.55 * (1 - wob), by - hh * 0.58),
            (cx + ww, by - hh * 0.28),
        ], color=cols[k])


def keine_pair(cx, clasp_t):
    """Two mirrored figures facing each other: human Keine (left, peaked cap) and
    hakutaku Keine (right, horns), bodies fanning to the bottom corners, arms
    coming inward to clasped praying-hands at the centre (clasp_t in [0,1])."""
    polys = []
    # bodies: broad swept cloaks meeting near the top centre, fanning out + down
    polys += [[(cx - 16, 150), (cx - 116, 300), (cx - 232, 720),
               (cx - 44, 720), (cx - 8, 360)]]
    polys += [[(cx + 16, 150), (cx + 116, 300), (cx + 232, 720),
               (cx + 44, 720), (cx + 8, 360)]]
    # heads at top centre, tilting toward each other
    polys += ellipse_poly(cx - 48, 124, 34, 40, rot=0.34)
    polys += ellipse_poly(cx + 48, 124, 34, 40, rot=-0.34)
    # LEFT = human Keine: a peaked historian cap pointing up toward centre
    polys += [[(cx - 78, 116), (cx - 26, 64), (cx - 10, 92), (cx - 48, 142)]]
    # RIGHT = hakutaku Keine: two horns pointing up-and-out
    polys += [[(cx + 26, 100), (cx + 14, 44), (cx + 38, 74)]]
    polys += [[(cx + 50, 102), (cx + 76, 50), (cx + 82, 84)]]
    # arms inward to the clasped hands at the centre (rise as clasp_t -> 1)
    gy = lerp(300, 248, clasp_t)
    polys += limb([(cx - 42, 214), (cx - 26, lerp(252, 236, clasp_t)), (cx, gy)], [13, 10, 7])
    polys += limb([(cx + 42, 214), (cx + 26, lerp(252, 236, clasp_t)), (cx, gy)], [13, 10, 7])
    # clasped praying-hands (a slim upward leaf) appears as they meet
    if clasp_t > 0.25:
        ph = 34 * clamp01((clasp_t - 0.25) / 0.75)
        polys += [[(cx - 11, gy + 12), (cx, gy - ph), (cx + 11, gy + 12)]]
    return polys


def spiral_comma(cx, cy, rot, reach, width0):
    """A black comma/spiral arm curling clockwise from the centre (the smear)."""
    N = 44
    center = []
    widths = []
    for k in range(N + 1):
        f = k / N
        ang = rot + f * 2.2 * math.pi          # clockwise sweep
        rr = reach * f
        center.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        widths.append(lerp(width0, 1.5, f))
    return ribbon(center, widths)


def draw(c: Canvas, u: float, i: int, t: float) -> None:
    # ---- Phase A: the flame whiteout recedes, the pair grows in ----
    if i < SPIN:
        # gray fire around the base throughout the pair's beat
        for sgn in (-1, 1):
            flame(c, CX + sgn * 150, 700, lerp(380, 200, clamp01(i / A_END)), t + sgn)
            flame(c, CX + sgn * 60, 720, lerp(300, 170, clamp01(i / A_END)), t - sgn)
        if i < A_END:
            # receding whiteout core (continues Scene 12's blaze)
            wh = lerp(820, 150, ease(i / A_END, "in_out"))
            flame(c, CX, 470, wh, t, layers=3)
        # the mirrored Keine pair
        g = ease(clamp01((i - 6) / 30), "out")
        clasp_t = ease(clamp01((i - A_END) / (CLASP - A_END)), "in_out")
        pair = keine_pair(CX, clasp_t)
        pair = transform_polys(pair, scale=lerp(0.5, 1.0, g), origin=(CX, 420))
        draw_polys(c, pair, color=WHITE)
        return

    # ---- Phase B: clockwise spin -> spiral -> moon ----
    p = clamp01((i - SPIN) / (NFR - SPIN))
    # the pair rotates clockwise, shrinking into the centre and vanishing
    if p < 0.6:
        sp = ease(clamp01(p / 0.6), "in")
        pair = keine_pair(CX, 1.0)
        pair = transform_polys(pair, scale=lerp(1.0, 0.18, sp),
                               rotate=sp * 1.7 * math.pi, origin=(CX, CY))
        draw_polys(c, pair, color=WHITE)

    # the growing white moon (clean disc), drifting toward the top-left
    mt = ease(clamp01((i - SPIN) / (MOON_F - SPIN)), "in_out")
    mr = lerp(40, 120, mt)
    drift = ease(clamp01((i - MOON_F) / (NFR - MOON_F)), "in_out")
    mx = lerp(CX, MOON_END[0], drift)
    my = lerp(CY, MOON_END[1], drift)
    draw_polys(c, circle_poly(mx, my, mr, n=64), color=WHITE)

    # the black spiral comma smears clockwise over the disc, then unwinds away
    sm = clamp01((i - SPIN) / (MOON_F - SPIN))
    if sm < 0.98:
        rot = -math.pi / 2 + sm * 2.4 * math.pi          # clockwise
        reach = lerp(120, 30, sm)
        width0 = lerp(60, 4, sm)
        draw_polys(c, spiral_comma(mx, my, rot, reach, width0), color=BLACK)


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw, bg=BLACK)
    print(f"Scene 13: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

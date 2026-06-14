"""Scene 12 -- Mokou's fire (CHORUS 1 begins).
Frames 2526-2789 (264 fr).

SCENES.md: Mokou (very long hair, hair bow) stands on black (ref f2566, head
bowed). She conjures a flame on each open palm -- the fire is rendered with soft
GRAY texture, the only textured element so far (one-hand flame ref f2641) -- then
claps the two flames together (~1:30-1:32) and the fire grows. Polarity W-on-B.
Transition out: the combined blaze engulfs the whole frame (ref f2731 at local
~205 already shows flames filling the screen, two figures emerging at the bottom).

Continuity in (11->12): Scene 11 ended with the vertical Rod of Remorse standing
on the seam. The chorus-1 downbeat flips the field to full W-on-B and that vertical
column widens (squash-x reveal) into Mokou -- the rod morphs into her. Handoff out
(12->13): the blaze fills the frame and two Keine forms begin emerging at the
bottom; Scene 13 continues from this flame whiteout.

Mokou + flames are built inline. Gray fire is allowed here (PROJECT.md sec.4).
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: F401,F403
from shapes import (  # noqa: E402
    head, dress_body, limb, long_hair, reimu_bow, ellipse_poly,
    draw_polys, transform_polys,
)

SCENE_START_FRAME = 2526
SCENE_END_FRAME = 2790
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / FPS  # 8.8 s
NFR = SCENE_END_FRAME - SCENE_START_FRAME                     # 264

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

CX = 480
A_END = 36        # rod -> Mokou squash-reveal
L_IGN = 70        # left flame ignites
R_IGN = 115       # right flame ignites
CLAP = 174        # palms come together
BLAZE = 205       # blaze fills the frame (ref f2731)

GRAY_OUT, GRAY_MID, CORE = 118, 186, 246    # soft-gray fire, white core


def squashx(polys, sx, cx=CX):
    """Scale every polygon's x toward cx (a vertical squash for the rod reveal)."""
    return [[(cx + (x - cx) * sx, y) for x, y in p] for p in polys]


def arm_to(sx, sy, palm):
    """An arm from shoulder (sx,sy) to a palm point, with a small open-palm cup.
    palm=None hangs the arm relaxed at the side."""
    if palm is None:
        return limb([(sx, sy), (sx - 2, sy + 86), (sx - 6, sy + 152)], [15, 12, 8])
    px, py = palm
    ex, ey = (sx + px) / 2, (sy + py) / 2 - 8
    polys = limb([(sx, sy), (ex, ey), (px, py)], [15, 12, 8])
    polys += [[(px - 20, py), (px + 20, py), (px + 13, py + 12), (px - 13, py + 12)]]
    return polys


def mokou(cx, lpalm, rpalm):
    """Mokou: big hair bow, very long hair, tunic + visible legs (trousers),
    arms reaching to the two palms."""
    polys = []
    polys += long_hair(cx, 166, 94, 430)          # very long, wide hair (signature)
    polys += reimu_bow(cx, 138, 98, 62)           # big hair bow on top
    polys += head(cx, 200, 42)
    polys += dress_body(cx, 252, 372, 556, 52, 60, 98)   # short tunic
    polys += limb([(cx - 22, 552), (cx - 26, 648), (cx - 28, 704)], [18, 14, 11])
    polys += limb([(cx + 22, 552), (cx + 30, 648), (cx + 34, 704)], [18, 14, 11])
    polys += arm_to(cx - 50, 268, lpalm)
    polys += arm_to(cx + 50, 268, rpalm)
    return polys


def flame(c, cx, by, h, t, layers=3):
    """Draw a soft-gray flickering flame tongue, base at (cx,by), tip up at by-h."""
    cols = [GRAY_OUT, GRAY_MID, CORE]
    for k in range(layers):
        f = 1.0 - k / (layers + 0.4)
        hh, ww = h * f, h * 0.30 * f
        wob = 0.18 * math.sin(t * 7 + k * 1.3)
        wob2 = 0.14 * math.sin(t * 5 + k)
        pts = [
            (cx, by),
            (cx - ww, by - hh * 0.30),
            (cx - ww * 0.55 * (1 + wob), by - hh * 0.62),
            (cx - ww * 0.30, by - hh * 0.86),
            (cx + ww * 0.18 * (1 + wob2), by - hh),       # tip leans
            (cx + ww * 0.34, by - hh * 0.84),
            (cx + ww * 0.55 * (1 - wob), by - hh * 0.58),
            (cx + ww, by - hh * 0.28),
        ]
        c.polygon(pts, color=cols[k])


def draw(c: Canvas, u: float, i: int, t: float) -> None:
    # ---- Phase A: the vertical rod widens (squash-x) into Mokou ----
    if i < A_END:
        sx = lerp(0.14, 1.0, ease(i / A_END, "in_out"))
        fig = mokou(CX, None, None)
        draw_polys(c, squashx(fig, sx), color=WHITE)
        return

    # palm positions over time -------------------------------------------------
    # left palm: rest -> extended out (screen-left) -> clapped to centre
    if i < L_IGN:
        lp = (CX - 34, 430)
    elif i < CLAP:
        e = ease(clamp01((i - L_IGN) / 40), "in_out")
        lp = (lerp(CX - 34, CX - 150, e), lerp(430, 360, e))
    else:
        e = ease(clamp01((i - CLAP) / 30), "in_out")
        lp = (lerp(CX - 150, CX - 12, e), 360)
    # right palm: stays down, then extends, then claps to centre
    if i < R_IGN:
        rp = (CX + 34, 430)
    elif i < CLAP:
        e = ease(clamp01((i - R_IGN) / 40), "in_out")
        rp = (lerp(CX + 34, CX + 150, e), lerp(430, 360, e))
    else:
        e = ease(clamp01((i - CLAP) / 30), "in_out")
        rp = (lerp(CX + 150, CX + 12, e), 360)

    # ---- figure (hidden once the blaze takes over near f2731) ----
    if i < BLAZE:
        draw_polys(c, mokou(CX, lp, rp), color=WHITE)

    # ---- flames ----
    if i < CLAP:
        if i >= L_IGN:
            lh = lerp(0, 150, ease(clamp01((i - L_IGN) / 40), "out"))
            flame(c, lp[0], lp[1] - 4, lh, t)
        if i >= R_IGN:
            rh = lerp(0, 150, ease(clamp01((i - R_IGN) / 40), "out"))
            flame(c, rp[0], rp[1] - 4, rh, t)
        return

    # ---- clap: the merged blaze grows to engulf the whole frame (ref f2731) ----
    # fast ramp so the flames already fill the screen by f2731 (i=205), then hold
    bz = ease(clamp01((i - CLAP) / (BLAZE + 16 - CLAP)), "out")
    # a wall of gray flame tongues spanning the width, rising from the floor
    ntong = 7
    for k in range(ntong):
        fx = lerp(40, WIDTH - 40, k / (ntong - 1))
        hk = lerp(150, 900, bz) * (0.66 + 0.34 * math.sin(k * 1.7 + 1))
        flame(c, fx, HEIGHT - 6, hk, t + k * 0.6)
    # the bright white-cored centre (the clapped flames merged) engulfing the frame
    flame(c, CX, HEIGHT - 6, lerp(240, 1000, bz), t, layers=3)
    # two Keine forms begin emerging at the bottom (ref f2731): narrow dark gaps
    if i >= BLAZE:
        ge = clamp01((i - BLAZE) / (NFR - BLAZE))
        gh = lerp(30, 150, ge)
        for sgn in (-1, 1):
            gx = CX + sgn * 116
            c.polygon([(gx - 24, HEIGHT), (gx - 20, HEIGHT - gh),
                       (gx, HEIGHT - gh - 16), (gx + 20, HEIGHT - gh),
                       (gx + 24, HEIGHT)], color=BLACK)


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw, bg=BLACK)
    print(f"Scene 12: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

"""Scene 23 -- Yukari emerges from the gap (f4230-4410, 180 fr). W-on-B.

22->23 FLIPS to W-on-B. The scene opens on the gap -- Scene 22's "TV-off" slit,
now read as one of Yukari's sukima: a white rift on black (the exact inverse of
Scene 22's last frame). Yukari rises OUT of it, pushing her round parasol up
through the gap first (round white canopy emergence, ref f4276), then fully
emerging with the parasol settled wide BEHIND her head (parasol-from-behind,
ref f4351). Finally she raises a folding fan, opens it (someone hidden behind),
and SNAPS it shut -- revealing Tenshi (handoff to Scene 24, which stays W-on-B).

Built from the shared toolkit (mob_cap, head, long_hair, dress_body, parasol,
fan_open, limb, plus tenshi for the reveal). The 22->23 boundary reproduces the
shared gap (full-width thin almond lens at y=360) inverted onto black.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: E402,F403
from shapes import (  # noqa: E402
    head, mob_cap, long_hair, dress_body, parasol, fan_open, limb,
    ellipse_poly, draw_polys, transform_polys, tenshi,
)

SCENE_START_FRAME = 4230
SCENE_END_FRAME = 4410
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / 30.0   # 6.0 s

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

A_END = 54          # parasol canopy pushed up through the gap, Yukari rising (ref f4276)
B_END = 120         # fully out, parasol settled wide behind her (ref f4351)
# 120..179 -> fan opens, holds, then snaps shut revealing Tenshi

CX = 480
SETTLED_HY = 188    # Yukari's head centre once she is fully out


def gap_rift(c, fade):
    """The sukima rift (white, on black): a full-width thin almond lens at y=360
    with a dark octagon notch -- the inverse of Scene 22's last frame. *fade* in
    [0,1] shrinks/closes it as Yukari takes over (fade=0 = full open)."""
    W, yc = 960, 360
    half = lerp(78, 4, ease(fade, "in"))
    n = 72
    top = [(W * k / n, yc - half * math.sin(math.pi * (k / n))) for k in range(n + 1)]
    bot = [(W * k / n, yc + half * math.sin(math.pi * (k / n))) for k in range(n, -1, -1)]
    c.polygon(top + bot, color=WHITE)
    onr = 56 * (1 - ease(fade, "in"))
    if onr > 2:
        # dark octagon notch in the centre of the white lens
        oct_pts = [(480 + onr * math.cos(math.pi / 8 + k * math.pi / 4),
                    yc + onr * math.sin(math.pi / 8 + k * math.pi / 4)) for k in range(8)]
        c.polygon(oct_pts, color=BLACK)


def yukari_fig(hy, arm=1.0, fan_t=0.0):
    """Yukari from the toolkit (mob cap + head + long hair + gown), arms spread,
    anchored by head centre (CX, hy). Returns (polys, right_hand_xy)."""
    polys = []
    polys += long_hair(CX, hy - 8, 72, 322)
    polys += dress_body(CX, hy + 48, hy + 206, hy + 452, 64, 86, 168)
    # arms spread out to the sides
    lhx = CX - 78 - 90 * arm
    polys += limb([(CX - 58, hy + 72), ((CX - 58 + lhx) / 2, hy + 58), (lhx, hy + 52)], [16, 12, 8])
    rhx = CX + 78 + 90 * arm
    rhy = hy + 52
    polys += limb([(CX + 58, hy + 72), ((CX + 58 + rhx) / 2, hy + 58), (rhx, rhy)], [16, 12, 8])
    polys += head(CX, hy, 47)
    polys += mob_cap(CX, hy - 28, 82, 50)
    return polys, (rhx, rhy)


def draw(c, u, i, t):
    # ---- Phase A: emergence from the gap -------------------------------------
    if i < A_END:
        a = i / float(A_END)
        # Yukari rises: head climbs from below the gap up to settled height
        hy = lerp(560, SETTLED_HY, ease(a, "out"))
        arm = ease(clamp01((i - 18) / 30.0), "out")          # arms spread as she clears
        # parasol pushes UP out of the gap to the top of frame
        pcy = lerp(360, 84, ease(a, "out"))
        pr = lerp(40, 96, ease(a, "out"))
        polys, (rhx, rhy) = yukari_fig(hy, arm=arm)
        # parasol with a long pole reaching down toward her hand
        pole_len = max(20, (hy + 70) - pcy)
        para = parasol(CX, pcy, r=pr, pole=pole_len, scallops=6)
        gap_rift(c, fade=ease(clamp01((i - 8) / 40.0), "in"))
        draw_polys(c, para)
        draw_polys(c, polys)
        return

    # ---- Phase B: fully out, parasol settles wide behind the head ------------
    if i < B_END:
        b = (i - A_END) / float(B_END - A_END)
        hy = SETTLED_HY
        polys, (rhx, rhy) = yukari_fig(hy, arm=1.0)
        # parasol drops from the top to behind/over her head and widens
        pcy = lerp(84, 128, ease(b, "in_out"))
        pr = lerp(96, 150, ease(b, "in_out"))
        pole_len = max(20, (hy + 30) - pcy)
        para = parasol(CX, pcy, r=pr, pole=pole_len, scallops=7)
        draw_polys(c, para)
        draw_polys(c, polys)
        return

    # ---- Phase C: fan opens, holds, snaps shut -> Tenshi revealed ------------
    cprog = (i - B_END) / float(SCENE_END_FRAME - SCENE_START_FRAME - B_END)  # 0..1
    hy = SETTLED_HY
    # parasol stays settled behind her
    pcy, pr = 128, 150
    pole_len = (hy + 30) - pcy

    # fan envelope: open (0->0.45), hold (0.45->0.78), snap shut (0.78->1)
    if cprog < 0.45:
        fan_t = ease(cprog / 0.45, "out")
    elif cprog < 0.78:
        fan_t = 1.0
    else:
        fan_t = 1.0 - ease((cprog - 0.78) / 0.22, "in")

    # Tenshi hidden behind the fan, revealed as it shuts (rises in over the end)
    reveal = ease(clamp01((cprog - 0.74) / 0.26), "out")

    para = parasol(CX, pcy, r=pr, pole=pole_len, scallops=7)
    polys, (rhx, rhy) = yukari_fig(hy, arm=0.55)
    draw_polys(c, para)
    draw_polys(c, polys)

    # Tenshi grows in (centre-right) where the fan was; mostly hidden until snap
    if reveal > 0.02:
        t_foot = 600
        tscale = 0.74
        tpolys = tenshi(560, t_foot, scale=tscale, pose="hips")
        # slide up into place as she is revealed
        tpolys = transform_polys(tpolys, translate=(0, lerp(60, 0, reveal)))
        draw_polys(c, tpolys)

    # the folding fan in Yukari's raised right hand, in front (covers Tenshi)
    if fan_t > 0.02:
        fan = fan_open(rhx, rhy, r=150 * fan_t, a0=-2.5, a1=-0.2, n=20)
        draw_polys(c, transform_polys(fan, rotate=0.15, origin=(rhx, rhy)))


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw, bg=BLACK)
    print(f"Scene 23: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

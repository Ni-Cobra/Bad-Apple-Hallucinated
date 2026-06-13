"""Scene 6 -- Sakuya: shards, twirl, knives.  Frames 1275-1499 (225 frames).

SCENES.md: White teacup shards scatter across the black frame (f1291). One shard
morphs into a small spinning figure with outstretched arms seen top-down (f1336) --
this is Sakuya twirling ("casting The World"), not Rumia. She lands facing the
camera as the maid (headband visible, f1381), draws her throwing knives and hurls
them (rear/3-4 view, f1441). Polarity W-on-B (inverted at the teacup shatter).

Continuity in (5->6): Scene 5 ended with the dropped `teacup` falling (B-on-W) at
~(240,580). The SHATTER is the polarity inversion, so this scene renders W-on-B
(bg=BLACK) and opens with the cup hitting and bursting into white shards there.
Handoff out (6->7): one thrown `knife` ends in flight with its tip prominent at
~(585,255); Scene 7 grows Flandre's `crystal_wing` prongs out of that knife tip
(continuous W-on-B, no flip at the boundary).

Sakuya is built inline; her identifying features are the frilly maid headdress
(band + frills) over side braids, and the thrown knives.
"""

import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: F401,F403
from shapes import (  # noqa: E402
    head, dress_body, limb, ellipse_poly, circle_poly, ribbon, teacup, knife,
    draw_polys, transform_polys,
)

SCENE_START_FRAME = 1275
SCENE_END_FRAME = 1500
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / FPS  # 7.5 s
NFR = SCENE_END_FRAME - SCENE_START_FRAME                      # 225

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

CX = 480
IMPACT = (240, 580)            # where Scene 5's teacup is falling -> shatters here
KNIFE_TIP = (660, 180)         # 6->7 handoff: thrown-knife tip at the last frame

# Fixed shard burst (seeded so it is identical every run).
_rng = random.Random(4242)
SHARDS = [(_rng.uniform(-2.9, -0.15),                      # launch angle (upward fan)
           _rng.uniform(9.0, 17.0),                        # speed px/frame
           _rng.uniform(12, 24),                           # size
           _rng.uniform(-0.25, 0.25))                      # spin
          for _ in range(17)]


def _shard(cx, cy, size, rot):
    pts = [(0, -size), (size * 0.55, size * 0.45), (-size * 0.45, size * 0.6)]
    ca, sa = math.cos(rot), math.sin(rot)
    return [[(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]]


def sakuya_twirl(cx, cy, r, angle):
    """Sakuya seen top-down, spinning with arms out (the 'not Rumia' twirl)."""
    polys = list(circle_poly(cx, cy, r))                   # flared skirt from above
    polys += circle_poly(cx, cy, r * 0.46)                 # head/torso lump
    for s in (1, -1):
        ax = cx + s * r * 1.8 * math.cos(angle)
        ay = cy + s * r * 1.8 * math.sin(angle)
        polys += ribbon([(cx, cy), (ax, ay)], [r * 0.3, r * 0.13])
    # apron ribbon trailing off (the streak once mistaken for Rumia's ribbon)
    bx = cx + r * 2.1 * math.cos(angle + 1.9)
    by = cy + r * 2.1 * math.sin(angle + 1.9)
    polys += ribbon([(cx, cy), ((cx + bx) / 2, (cy + by) / 2 - r * 0.4), (bx, by)],
                    [r * 0.2, r * 0.12, 2])
    return polys


def sakuya_maid(cx, arm="rest"):
    """Frontal maid Sakuya: frilly headdress over side braids, dress, posed arms."""
    polys = []
    polys += ellipse_poly(cx, 184, 58, 60)                 # hair mass behind
    polys += limb([(cx - 46, 172), (cx - 60, 252), (cx - 52, 322)], [12, 10, 6])  # braid
    polys += limb([(cx + 46, 172), (cx + 60, 252), (cx + 52, 322)], [12, 10, 6])  # braid
    polys += head(cx, 172, 44)
    polys += ellipse_poly(cx, 138, 50, 15)                 # headdress band
    for k in range(-2, 3):
        polys += circle_poly(cx + k * 21, 131, 9)          # headdress frills
    polys += dress_body(cx, 214, 350, 600, 54, 72, 132)
    if arm == "throw":
        # left arm flung forward, right arm cocked up-right releasing knives
        polys += limb([(cx - 52, 226), (cx - 96, 286), (cx - 118, 250)], [12, 10, 7])
        polys += limb([(cx + 52, 226), (cx + 116, 248), (cx + 168, 206)], [12, 10, 7])
    else:  # rest
        polys += limb([(cx - 52, 226), (cx - 86, 320), (cx - 90, 392)], [12, 10, 7])
        polys += limb([(cx + 52, 226), (cx + 86, 320), (cx + 90, 392)], [12, 10, 7])
    return polys


def _hsquash(polys, cx, k):
    return [[(cx + (x - cx) * k, y) for x, y in p] for p in polys]


def draw(c: Canvas, u: float, i: int, t: float) -> None:
    # ------------------------------------------------------------------ #
    # Phase A (i<55): teacup hits (W-on-B now) and shatters; shards scatter.
    # ------------------------------------------------------------------ #
    if i < 55:
        if i < 7:                                          # cup finishing its fall
            cup = teacup(IMPACT[0], IMPACT[1] - 40 + 6 * i, w=30)
            draw_polys(c, cup)
        else:
            s = i - 7
            for (ang, spd, sz, spin) in SHARDS:
                sx = IMPACT[0] + math.cos(ang) * spd * s
                sy = IMPACT[1] + math.sin(ang) * spd * s + 0.18 * s * s  # gravity
                if -40 < sx < WIDTH + 40 and sy < HEIGHT + 40:
                    draw_polys(c, _shard(sx, sy, sz, spin * s))
        # the spinning figure fades in toward the end of the burst
        if i >= 36:
            g = (i - 36) / 19.0
            draw_polys(c, sakuya_twirl(CX, 360, 18 + 18 * g, 0.4 * i))
        return

    # ------------------------------------------------------------------ #
    # Phase B (55<=i<98): the twirl spins, growing slightly (f1336).
    # ------------------------------------------------------------------ #
    if i < 98:
        g = ease(clamp01((i - 55) / 40.0), "out")
        r = lerp(36, 52, g)
        draw_polys(c, sakuya_twirl(CX, 360, r, 0.4 * i))
        return

    # ------------------------------------------------------------------ #
    # Phase C (98<=i<112): the twirl resolves/lands into the frontal maid.
    # ------------------------------------------------------------------ #
    if i < 112:
        a = ease((i - 98) / 14.0, "in_out")
        # grow the maid up from the spinning lump, fading the twirl out under it
        fig = transform_polys(sakuya_maid(CX, "rest"),
                              scale=lerp(0.42, 1.0, a), origin=(CX, 360))
        if a < 0.6:
            draw_polys(c, sakuya_twirl(CX, 360, lerp(52, 30, a), 0.4 * i))
        draw_polys(c, fig)
        return

    # ------------------------------------------------------------------ #
    # Phase D (112<=i<150): maid faces the camera (f1381), sways, readies.
    # ------------------------------------------------------------------ #
    if i < 150:
        sway = 10 * math.sin(2 * math.pi * (i - 112) / 60)
        arm_t = ease(clamp01((i - 132) / 18.0), "in")      # start winding up
        if arm_t > 0.5:
            fig = sakuya_maid(CX, "throw")
        else:
            fig = sakuya_maid(CX, "rest")
        fig = _hsquash(fig, CX, lerp(1.0, 0.86, arm_t))    # slight turn to 3/4
        fig = transform_polys(fig, translate=(sway, 0))
        draw_polys(c, fig)
        return

    # ------------------------------------------------------------------ #
    # Phase E (150<=i): 3/4-turned throw; knives streak up-right (f1441). One
    # 'hero' knife ends in flight with its tip at KNIFE_TIP (6->7 handoff).
    # ------------------------------------------------------------------ #
    fig = _hsquash(sakuya_maid(CX, "throw"), CX, 0.84)
    draw_polys(c, fig)

    hand = (CX + 168 * 0.84, 206)                          # right-hand release point
    # three knives released in sequence, flying up-right and off-frame
    for n in range(3):
        rel = 150 + n * 9
        if i >= rel:
            d = (i - rel)
            kx = hand[0] + 12.5 * d
            ky = hand[1] - 7.5 * d
            if kx < WIDTH + 60 and n < 2:                  # first two leave frame
                draw_polys(c, knife(kx, ky, length=92, angle=-0.54, w=9))
    # hero knife (n==2): flies clear of the figure into open upper-right space so
    # its tip is isolated at KNIFE_TIP by the last frame (Scene 7 grows the wing
    # prongs out of that tip).
    rel = 168
    if i >= rel:
        d = clamp01((i - rel) / (NFR - 1 - rel))
        length = lerp(70, 140, ease(d, "out"))
        ang = -0.54
        tipx, tipy = KNIFE_TIP
        cx = tipx - length * math.cos(ang)
        cy = tipy - length * math.sin(ang)
        cx = lerp(hand[0], cx, ease(d, "out"))
        cy = lerp(hand[1], cy, ease(d, "out"))
        draw_polys(c, knife(cx, cy, length=length, angle=ang, w=11))


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw, bg=BLACK)
    print(f"Scene 6: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

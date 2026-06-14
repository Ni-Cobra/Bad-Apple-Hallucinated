"""Scene 9 -- Yuyuko and the cherry petal.  Frames 1920-2129 (210 fr).

SCENES.md: close-ups of Yuyuko (mob cap with its signature fold). She opens her
folding fan and with a wave sends a single cherry petal floating off (~1:08); the
camera abandons her and follows the petal, zooming in until the petal fills the
frame (abstract close-up, ref f2011). Polarity W-on-B.

Continuity in (8->9): the viewpoint rotates from Youmu to Yuyuko beside the
half-bloomed tree -- Scene 9 opens already centered on Yuyuko (the tree's blossom
cloud still visible behind-left) and pushes in. Handoff out (9->10): the magnified
single petal fills the frame, near-horizontal, and Scene 10 morphs it into the
hull of Komachi's ferry. No polarity flip (both W-on-B). Shared shapes `yuyuko`,
`cherry_tree`, `sakura_petal` from the asset library.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: F401,F403
from shapes import (  # noqa: E402
    cherry_tree, yuyuko, sakura_petal, draw_polys, transform_polys,
)

SCENE_START_FRAME = 1920
SCENE_END_FRAME = 2130
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / FPS  # 7.0 s
NFR = SCENE_END_FRAME - SCENE_START_FRAME                      # 210

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

CX = 480
RELEASE = 50      # local frame the single petal detaches from the fan
FOLLOW = 70       # camera leaves Yuyuko and follows the petal (petal fills ~f2010-2040)


def cam(polys, s, fx, fy):
    return transform_polys(polys, scale=s, origin=(fx, fy), translate=(480 - fx, 360 - fy))


# A few ambient drifting petals (background), fixed seeds.
AMBIENT = [(150, -40, 26, 0.0), (330, -160, 22, 1.6), (700, -90, 24, 3.1),
           (820, -220, 20, 4.4)]


def petal_pos(i):
    """World position of the single 'hero' petal after release (drifts up-right)."""
    k = clamp01((i - RELEASE) / 100.0)
    x = lerp(CX + 96, CX + 210, ease(k, "out")) + 30 * math.sin(i * 0.05)
    y = lerp(250, 150, ease(k, "in_out"))
    return x, y


def draw(c: Canvas, u: float, i: int, t: float) -> None:
    # background ambient petals (skip once we are tight on the hero petal)
    if i < FOLLOW + 40:
        for x0, y0, w, ph in AMBIENT:
            y = (y0 + (i * 1.5) % 840)
            draw_polys(c, sakura_petal(x0 + 24 * math.sin(i * 0.04 + ph), y,
                                       w=w, h=w * 1.4, rot=ph + i * 0.04))

    if i < FOLLOW:
        # ---- Yuyuko close-up: push in, open the fan, wave, release a petal ----
        s = lerp(0.82, 1.5, ease(clamp01(i / 46.0), "in_out"))
        fy = lerp(330, 205, ease(clamp01(i / 46.0), "in_out"))
        fan_t = ease(clamp01((i - 12) / 26.0), "out")
        arm_t = ease(clamp01((i - 34) / 30.0), "in_out")          # raise/wave arm
        polys = []
        # tree blossom cloud lingering behind-left for continuity (fades as we push in)
        if i < 46:
            polys += cherry_tree(150, 720, height=520, bloom_side=-1,
                                 spread=300, bloom_t=1.0)
        polys += yuyuko(cx=CX, fan_t=fan_t, arm_t=arm_t)
        draw_polys(c, cam(polys, s, CX + 40, fy))
        # the hero petal, just leaving the fan after RELEASE
        if i >= RELEASE:
            px, py = petal_pos(i)
            draw_polys(c, cam(sakura_petal(px, py, w=34, h=48,
                                           rot=0.4 + (i - RELEASE) * 0.04),
                              s, CX + 40, fy))
        return

    # ---- Phase C: camera follows the petal and zooms until it fills the frame ----
    px, py = petal_pos(i)
    z = ease(clamp01((i - FOLLOW) / 54.0), "in_out")
    s = lerp(1.5, 9.5, z)
    rot = lerp(0.55, math.pi / 2 - 0.1, z)        # rotate toward horizontal (boat hull)
    grow = lerp(34, 40, z)
    draw_polys(c, cam(sakura_petal(px, py, w=grow, h=grow * 1.45, rot=rot), s, px, py))


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw, bg=BLACK)
    print(f"Scene 9: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

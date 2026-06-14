"""Scene 8 -- Youmu's sword flourish.  Frames 1710-1919 (210 fr).  VERSE 2.

SCENES.md: Youmu stands center holding her two swords (Roukanken & Hakurouken),
performs a chiburi (blood-flick) and sheathes them. Cherry petals drift; a light
beam cuts the upper frame. Yuyuko stands small in the left background. The huge
half-bloomed Saigyou Ayakashi cherry tree (one side bare branches, one side dense
bloom) dominates as the camera turns toward Yuyuko. Refs: f1726 (close Youmu +
swords), f1801 (tree + tiny Yuyuko). Polarity W-on-B throughout.

Continuity in (7->8): Scene 7 ended B-on-W with a white blade slash across
Flandre's chest -- that blade is Youmu's sword. The 7->8 boundary FLIPS back to
W-on-B (hard cut expected, PROJECT.md sec.6 rule 3); Scene 8 opens on a close-up
of Youmu's long sword held out horizontally (echoing the slash) and carries the
cut into her chiburi. Handoff out (8->9): camera settles on the half-bloomed tree
with Yuyuko small beside it; Scene 9 continues as a Yuyuko close-up. Shared shapes
`cherry_tree`, `yuyuko`, `sakura_petal` from the asset library make the boundary
consistent. Youmu is built inline (two swords + Myon half-ghost = her read).
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: F401,F403
from shapes import (  # noqa: E402
    head, dress_body, limb, ellipse_poly, circle_poly, ribbon,
    cherry_tree, yuyuko, sakura_petal, draw_polys, transform_polys,
)

SCENE_START_FRAME = 1710
SCENE_END_FRAME = 1920
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / FPS  # 7.0 s
NFR = SCENE_END_FRAME - SCENE_START_FRAME                      # 210

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

CX = 480
A_END = 40        # close-up chiburi
B_END = 84        # sheathe + pull-back begins
# drifting petals: fixed (x, base_y, w, phase) seeds; fall + rotate per frame
PETALS = [(170, -40, 30, 0.0), (360, -120, 26, 1.4), (560, -200, 34, 2.6),
          (720, -80, 28, 4.0), (250, -260, 24, 5.1), (840, -180, 30, 0.7)]


def youmu(cx=480, sheathe=0.0, chiburi=0.0):
    """Youmu: silver bob, knee skirt, two swords, Myon half-ghost beside her.

    *sheathe* 0 -> long sword extended to the right (the chiburi flick); 1 -> both
    swords crossed in an X behind her back. *chiburi* lowers the extended tip.
    """
    polys = []
    # crossed swords behind the back (an X over the shoulders), grows with sheathe
    if sheathe > 0.04:
        L = 168 * min(1.0, sheathe / 0.9)
        polys += ribbon([(cx - 8, 236), (cx - 8 - L * 0.65, 236 - L)], [9, 2])
        polys += ribbon([(cx + 8, 236), (cx + 8 + L * 0.65, 236 - L)], [9, 2])
    # hair bob + head
    polys += ellipse_poly(cx, 156, 56, 52)
    polys += head(cx, 168, 42)
    # body: vest + flared knee skirt
    polys += dress_body(cx, 214, 332, 476, 50, 60, 108)
    # legs
    polys += limb([(cx - 24, 476), (cx - 28, 548), (cx - 30, 606)], [16, 13, 10])
    polys += limb([(cx + 24, 476), (cx + 32, 548), (cx + 40, 606)], [16, 13, 10])
    # Myon (half-ghost) floating to her left -- an identifying read
    mx, my = cx - 144, 252
    polys += circle_poly(mx, my, 24, n=20)
    polys += [[(mx - 20, my + 4), (mx - 12, my + 38), (mx, my + 18),
               (mx + 12, my + 40), (mx + 20, my + 4)]]
    # long sword extended to the right for the chiburi (retracts as she sheathes)
    reach = 1.0 - min(1.0, sheathe / 0.6)
    if reach > 0.02:
        tipy = lerp(252, 318, chiburi)
        ex = cx + 60 + 280 * reach
        polys += ribbon([(cx + 54, 252), ((cx + 54 + ex) / 2, lerp(250, tipy, 0.5)),
                         (ex, tipy)], [11, 7, 2])
        polys += limb([(cx + 46, 232), (cx + 54, 250), (cx + 56, 252)], [13, 11, 9])
    # left arm (holds the short Hakurouken low across the body)
    polys += limb([(cx - 46, 232), (cx - 64, 296), (cx - 70, 346)], [13, 11, 8])
    return polys


def cam(polys, s, fx, fy):
    """Camera: map world focus (fx,fy) to screen center (480,360) at zoom *s*."""
    return transform_polys(polys, scale=s, origin=(fx, fy), translate=(480 - fx, 360 - fy))


def draw_petals(c, i, count, y_span=820, speed=1.0):
    for k in range(count):
        x, y0, w, ph = PETALS[k]
        y = (y0 + (i * 1.6 * speed) % y_span)
        rot = ph + i * 0.05
        sway = 26 * math.sin(i * 0.04 + ph)
        draw_polys(c, sakura_petal(x + sway, y, w=w, h=w * 1.4, rot=rot))


def draw(c: Canvas, u: float, i: int, t: float) -> None:
    # ---- Phase A: close-up, long sword out, chiburi flick (echoes the slash) ----
    if i < A_END:
        chib = ease(clamp01((i - 18) / 20.0), "in_out")     # flick down ~f1728+
        fig = youmu(CX, sheathe=0.0, chiburi=chib)
        draw_polys(c, cam(fig, 1.7, CX + 120, 250))         # zoomed on torso+blade
        draw_petals(c, i, 2)
        return

    # ---- Phase B: sheathe (swords cross behind), light beam, pull-back begins ----
    if i < B_END:
        p = (i - A_END) / (B_END - A_END)
        sh = ease(clamp01(p / 0.8), "in_out")
        s = lerp(1.7, 1.0, ease(p, "in_out"))
        fy = lerp(250, 360, ease(p, "in_out"))
        fig = youmu(CX, sheathe=sh, chiburi=1.0)
        draw_polys(c, cam(fig, s, CX + lerp(120, 0, ease(p, "in_out")), fy))
        # light beam slicing the upper-left frame
        beam_a = clamp01((i - A_END) / 12.0)
        if beam_a > 0:
            bw = 14 * beam_a
            c.polygon([(0, 70), (0, 70 + bw), (620, 220 + bw), (620, 220)])
        draw_petals(c, i, 4)
        return

    # ---- Phase C: full reveal -- half-bloomed tree dominates, Yuyuko small bg ----
    p = clamp01((i - B_END) / 34.0)                          # settle the camera
    s = lerp(1.0, 0.92, ease(p, "out"))
    polys = []
    # the half-bloomed Saigyou Ayakashi: dense bloom-cloud (left) + bare branches (right)
    polys += cherry_tree(330, 700, height=520, bloom_side=-1, spread=300, bloom_t=1.0)
    # Youmu finished and small at the tree base (the camera has turned away from her)
    polys += transform_polys(youmu(CX, sheathe=1.0, chiburi=1.0),
                             scale=0.46, origin=(CX, 360),
                             translate=(-70, 188))
    # Yuyuko small in the lower-right background (the handoff target)
    polys += transform_polys(yuyuko(cx=770), scale=0.44, origin=(770, 360),
                             translate=(0, 180))
    draw_polys(c, cam(polys, s, 460, 380))
    draw_petals(c, i, 6)


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw, bg=BLACK)
    print(f"Scene 8: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

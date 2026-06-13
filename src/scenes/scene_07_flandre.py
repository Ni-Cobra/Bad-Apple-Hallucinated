"""Scene 7 -- Flandre: wings, inversion, the "slice".  Frames 1500-1709 (210 fr).

SCENES.md: a row of Flandre's crystal-drop wing prongs emerges from the knife tip
(f1516). Pull back: Flandre (side ponytail) spreads her arms and shows both open
hands (f1591). On the accent ~0:54 the WHOLE FRAME INVERTS and she breaks into her
grin; at ~0:55.5 a horizontal blade flash crosses her chest (f1666) -- reads as her
being "sliced" (the blade is Youmu's). Polarity W-on-B (0:50-0:54) -> inverts
mid-scene to B-on-W (0:54-0:57); one of only two mid-scene inversions on a held
character.

Continuity in (6->7): Scene 6's thrown `knife` ended in flight with its tip at
(660,180), W-on-B. This scene opens on that same knife and grows the shared
`crystal_wing` prongs out of its tip, then Flandre unfolds from there. No flip at
the boundary (both W-on-B). Handoff out (7->8): this scene ends B-on-W with the
horizontal blade across Flandre's chest -- that blade is Youmu's sword, which
Scene 8 carries on (flipping back to W-on-B).

Flandre is built inline; identifying features are the angular `crystal_wing`s
(diamond prongs) on both sides and the single side ponytail.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: F401,F403
from shapes import (  # noqa: E402
    head, dress_body, mob_cap, limb, ponytail, ellipse_poly, circle_poly,
    knife, crystal_wing, draw_polys, transform_polys,
)

SCENE_START_FRAME = 1500
SCENE_END_FRAME = 1710
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / FPS  # 7.0 s
NFR = SCENE_END_FRAME - SCENE_START_FRAME                      # 210

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

CX = 480
KNIFE_TIP = (660, 180)         # 6->7 handoff: matches Scene 6's last frame
INVERT_AT = 120                # local frame of the mid-scene polarity flip (~0:54)


def flandre(cx, wing_t=1.0, arm_t=1.0):
    """Front-facing Flandre: crystal wings both sides, side ponytail, small cap.

    *wing_t* grows the wings; *arm_t* spreads the arms out with open hands.
    """
    polys = []
    polys += crystal_wing(cx - 44, 250, span=150, side=-1, prongs=5, t=wing_t)
    polys += crystal_wing(cx + 44, 250, span=150, side=1, prongs=5, t=wing_t)
    polys += ellipse_poly(cx, 178, 52, 52)                 # short hair
    polys += ponytail(cx - 42, 168, dx=-72, dy=150, w=24)  # left side ponytail
    polys += head(cx, 172, 44)
    polys += mob_cap(cx, 150, 58, 36)                      # small cap
    polys += dress_body(cx, 210, 340, 586, 52, 68, 124)
    lmid = (lerp(cx - 84, cx - 120, arm_t), lerp(316, 250, arm_t))
    lend = (lerp(cx - 90, cx - 170, arm_t), lerp(388, 232, arm_t))
    rmid = (lerp(cx + 84, cx + 120, arm_t), lerp(316, 250, arm_t))
    rend = (lerp(cx + 90, cx + 170, arm_t), lerp(388, 232, arm_t))
    polys += limb([(cx - 50, 224), lmid, lend], [12, 10, 8])
    polys += limb([(cx + 50, 224), rmid, rend], [12, 10, 8])
    if arm_t > 0.6:                                        # open hands when spread
        polys += circle_poly(lend[0], lend[1], 11)
        polys += circle_poly(rend[0], rend[1], 11)
    return polys


def draw(c: Canvas, u: float, i: int, t: float) -> None:
    # ------------------------------------------------------------------ #
    # Phase A (i<52): crystal prongs emerge from the knife tip (f1516), then
    # Flandre unfolds from that point and grows to full size.
    # ------------------------------------------------------------------ #
    if i < 52:
        if i < 26:                                         # the incoming knife
            draw_polys(c, knife(540, 252, length=140, angle=-0.54, w=11))
        if 4 <= i < 30:                                    # prongs growing off the tip
            pt = ease(clamp01((i - 4) / 14.0), "out")
            draw_polys(c, crystal_wing(KNIFE_TIP[0], KNIFE_TIP[1],
                                       span=120, side=-1, prongs=5, t=pt))
        if i >= 12:                                        # Flandre unfolds from the tip
            s = lerp(0.2, 1.0, ease(clamp01((i - 12) / 38.0), "out"))
            wt = clamp01((i - 12) / 30.0)
            fig = flandre(CX, wing_t=wt, arm_t=0.0)
            fig = transform_polys(fig, scale=s, origin=KNIFE_TIP)
            draw_polys(c, fig)
        return

    # ------------------------------------------------------------------ #
    # Phase B (52<=i<INVERT_AT): full Flandre spreads her arms (f1591), W-on-B.
    # ------------------------------------------------------------------ #
    if i < INVERT_AT:
        arm_t = ease(clamp01((i - 54) / 34.0), "out")      # fully spread by ~f1591
        sway = 8 * math.sin(2 * math.pi * (i - 52) / 60)
        fig = flandre(CX, wing_t=1.0, arm_t=arm_t)
        fig = transform_polys(fig, translate=(sway, 0))
        draw_polys(c, fig)
        return

    # ------------------------------------------------------------------ #
    # Phase C (i>=INVERT_AT): hard inversion flash -> B-on-W; grin; then the
    # horizontal blade flash sweeps across her chest (f1666) and holds.
    # Drawn white-on-black as usual, with the blade in the pre-invert background
    # colour (BLACK) so it becomes a white slash after the frame is inverted.
    # ------------------------------------------------------------------ #
    sway = 6 * math.sin(2 * math.pi * (i - 52) / 60)
    fig = flandre(CX, wing_t=1.0, arm_t=1.0)
    fig = transform_polys(fig, translate=(sway, 0))
    draw_polys(c, fig)

    if i >= 148:                                           # the slicing blade
        sweep = ease(clamp01((i - 148) / 24.0), "out")
        x0 = CX - 250 + sway
        x1 = lerp(CX - 250, CX + 270, sweep) + sway
        yb = 292
        blade = [(x0, yb - 9), (x1 - 16, yb - 11), (x1, yb),
                 (x1 - 16, yb + 11), (x0, yb + 9)]
        c.polygon(blade, color=BLACK)                      # -> white slash post-invert

    c.invert()


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw, bg=BLACK)
    print(f"Scene 7: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

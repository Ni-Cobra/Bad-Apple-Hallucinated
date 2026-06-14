"""Scene 31 -- The drop from the blade; crown splash (f5850-5970, 120 fr).
W-on-B.  Object scene, no characters.

30->31: opens on Scene 30's exact end state -- the shared blade_tip() fang from
the upper-left with a drop gathering at its point. The drop swells (ref f5881),
detaches and falls; it lands and erupts into a perfect milk-crown splash, a white
coronet on a pool at the bottom (ref f5941, shared crown_splash()).

31->32: the crown's pool sends a water COLUMN rising upward -- Scene 32 morphs
that column into PC-98 Reimu rising with the water.

blade_tip() + crown_splash() + drop() are shared shapes.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: E402,F403
from shapes import (  # noqa: E402
    blade_tip, crown_splash, drop, ellipse_poly, draw_polys, transform_polys,
)

SCENE_START_FRAME = 5850
SCENE_END_FRAME = 5970
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / 30.0   # 4.0 s

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

BLADE_TIP = (500.0, 268.0)          # shared with Scene 30 (blade_tip default)
TIP_DROP = (BLADE_TIP[0] - 4, BLADE_TIP[1] + 24)   # where the drop hangs
SPLASH = (480.0, 540.0)             # crown coronet centre
POOL = (480.0, 620.0)               # pool ellipse centre (bottom of frame)

HANG_END = 36       # drop gathers/hangs at the blade tip (ref f5881 ~ local 31)
FALL_END = 78       # drop detaches and falls to the impact
PEAK = 92           # crown splash at full height (ref f5941 ~ local 91)
# 92..119 -> the pool sends a water column rising (hand-off to Scene 32)


def draw(c, u, i, t):
    c.fill(BLACK)

    # ---- drop gathers at the blade tip --------------------------------------
    if i < HANG_END:
        draw_polys(c, blade_tip(BLADE_TIP), color=WHITE)
        dg = ease(i / float(HANG_END), "out")
        c.circle(TIP_DROP[0], TIP_DROP[1] + 8 * dg, 11 + 4 * dg, color=WHITE)
        return

    # ---- drop detaches and falls; blade pans up out of frame ----------------
    if i < FALL_END:
        f = (i - HANG_END) / float(FALL_END - HANG_END)
        ef = ease(f, "in")
        if f < 0.7:                                   # blade recedes upward
            draw_polys(c, transform_polys(blade_tip(BLADE_TIP),
                                          translate=(0, -ef * 320)), color=WHITE)
        dx = lerp(TIP_DROP[0], SPLASH[0], ef)
        dy = lerp(TIP_DROP[1] + 6, 720, ef)           # falls off the bottom edge
        draw_polys(c, drop(dx, dy, r=16), color=WHITE)
        return

    # ---- impact: milk-crown splash erupts from the pool ---------------------
    cs = ease(clamp01((i - FALL_END) / float(PEAK - FALL_END)), "out")
    # rising water column for the 31->32 hand-off (after the peak)
    col_h = 0.0
    if i >= PEAK:
        col_h = ease((i - PEAK) / float(SCENE_END_FRAME - SCENE_START_FRAME - PEAK), "out") * 384.0

    draw_polys(c, ellipse_poly(POOL[0], POOL[1], 218, 96), color=WHITE)   # pool
    if col_h > 1.0:                                   # the column climbing out of the pool
        c.polygon([(POOL[0] - 50, POOL[1] - 6), (POOL[0] - 24, POOL[1] - col_h),
                   (POOL[0] + 24, POOL[1] - col_h), (POOL[0] + 50, POOL[1] - 6)],
                  color=WHITE)
        c.circle(POOL[0], POOL[1] - col_h, 22, color=WHITE)              # blob at the column head
    # coronet -- full at the peak, then subsides as the column takes over
    crown_t = cs * (1.0 - 0.55 * clamp01(col_h / 384.0))
    if crown_t > 0.02:
        draw_polys(c, crown_splash(SPLASH[0], SPLASH[1], r=164, spikes=11, t=crown_t),
                   color=WHITE)


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw, bg=BLACK)   # W-on-B
    print(f"Scene 31: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

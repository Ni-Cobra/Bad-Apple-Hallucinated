"""Scene 35 -- Final shots: Marisa ascends, Reimu + apple, zoom to black (f6420-6569,
150 fr).  Split -> solid black.  LOOP POINT.

34->35: opens on the split the yin-yang resolves into -- left WHITE field, right
BLACK field (light-left / dark-right, continuing the orb's orientation).  From the
dark region's white eye, white Marisa rides her broom up and away into the sky
(ref f6451 ~ local f31).  From the light region's black eye, black Reimu (hair
down, no sleeve ruffles -- shared `reimu_hairdown`) stands holding the apple
(ref f6511 ~ local f91).  The camera then zooms INTO Reimu's black silhouette
until the frame is SOLID BLACK (ref f6556 ~ local f136) -- identical to Scene 1's
frame 0, closing the loop.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: E402,F403
from shapes import (  # noqa: E402
    reimu_hairdown, marisa_broom, apple, draw_polys, transform_polys,
)

SCENE_START_FRAME = 6420
SCENE_END_FRAME = 6570
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / 30.0   # 5.0 s

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

SEAM = 480.0
GROW_DONE = 50             # figures grown into place
FLY_DONE = 64             # Marisa has left the top of the frame
ZOOM_START = 96
ZOOM_DONE = 136            # solid black reached (ref f6556 ~ local f136)

REIMU_CX = 360.0
REIMU_DY = 60.0
REIMU_ORIGIN = (360.0, 440.0)   # torso interior -- the zoom anchor


def reimu_black(scale=1.0):
    base = transform_polys(reimu_hairdown(480), translate=(REIMU_CX - 480, REIMU_DY),
                           origin=(480, 360))
    if scale != 1.0:
        base = transform_polys(base, scale=scale, origin=REIMU_ORIGIN)
    return base


def draw(c, u, i, t):
    # --- the split: white left field, black right field ----------------------
    c.fill(BLACK)
    c.rectangle(0, 0, SEAM, HEIGHT, color=WHITE)

    # --- final zoom into Reimu's black silhouette -> solid black --------------
    if i >= ZOOM_DONE:
        c.fill(BLACK)
        return
    if i >= ZOOM_START:
        zt = ease((i - ZOOM_START) / float(ZOOM_DONE - ZOOM_START), "in_out")
        draw_polys(c, apple(REIMU_CX + 96, 548, r=34), color=BLACK)
        draw_polys(c, reimu_black(lerp(1.0, 20.0, zt)), color=BLACK)
        return

    # --- Marisa (white) flies up-and-away on the black right -----------------
    if i < FLY_DONE:
        ft = i / float(FLY_DONE)
        mscale = lerp(0.16, 0.82, ease(clamp01(i / float(GROW_DONE * 0.6)), "out"))
        mx = lerp(540.0, 940.0, ease(ft, "in"))
        my = lerp(214.0, -200.0, ease(ft, "in"))
        draw_polys(c, marisa_broom(mx, my, scale=mscale, facing=1), color=WHITE)

    # --- Reimu (black) grows into place on the white left, holds the apple ---
    grow = ease(clamp01(i / float(GROW_DONE)), "in_out")
    rscale = lerp(0.12, 1.0, grow)
    draw_polys(c, apple(REIMU_CX + 96, 548, r=34 * grow), color=BLACK)
    draw_polys(c, reimu_black(rscale), color=BLACK)


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw, bg=BLACK)
    print(f"Scene 35: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

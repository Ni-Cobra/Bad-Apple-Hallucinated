"""Scene 3 -- Marisa's broom flight to the SDM.  Frames 450-854 (405 frames).

SCENES.md: Marisa swoops in, catches Reimu's airborne apple, flies right-to-left
across a STARRY NIGHT SKY (white stars on black). The Scarlet Devil Mansion
silhouette rises from the lower-left as she descends. She eats the apple and
drops the core, which falls alone through the black frame and bounces once.
Polarity W-on-B (the only star-field backdrop in the video).

Continuity in (2->3): Scene 2 left the `apple` airborne at (540,140); the 2->3
flip lands here, so this scene is W-on-B from frame 0 and the apple is now white.
Handoff out (3->4): ends on the shared `apple_core` falling at frame centre
(~480,430) for Scene 4 to morph into Patchouli (polarity flips back to B-on-W).
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: F401,F403
from shapes import (  # noqa: E402
    marisa_broom, apple, apple_core, sdm_skyline, draw_stars,
    draw_polys, transform_polys,
)

SCENE_START_FRAME = 450
SCENE_END_FRAME = 855
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / FPS  # 13.5 s
NFR = SCENE_END_FRAME - SCENE_START_FRAME                      # 405

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

APPLE_IN = (540, 140)           # where Scene 2 left the airborne apple
CORE_REST = (480, 430)          # handoff position for Scene 4


def marisa_xy(i):
    """Eased right-to-left descending flight path."""
    p = ease(clamp01(i / 300.0), "in_out")
    x = lerp(640, 250, p)
    y = lerp(190, 330, p)
    return x, y


def draw(c: Canvas, u: float, i: int, t: float) -> None:
    draw_stars(c)  # fixed white star field on black, every frame

    mx, my = marisa_xy(i)

    # ---- Scarlet Devil Mansion rising from the lower-left during descent ---- #
    if 170 <= i < 326:
        rise = ease(clamp01((i - 170) / 90.0), "out")
        sink = ease(clamp01((i - 300) / 26.0), "in")     # slides away before the core fall
        sky_dy = lerp(180, 0, rise) + 200 * sink
        draw_polys(c, transform_polys(sdm_skyline(base_x=170, base_y=720, w=320, h=210),
                                      translate=(0, sky_dy)))

    # ---------------------------------------------------------------- #
    # Marisa + apple flight (i<315), then she "eats" it and drops the core.
    # ---------------------------------------------------------------- #
    if i < 326:
        draw_polys(c, transform_polys(marisa_broom(facing=-1),
                                      translate=(mx - 480, my - 360), scale=0.9))

    if i < 30:
        # catch: apple drifts from the handoff point into Marisa's reach.
        p = ease(i / 30.0, "out")
        ax = lerp(APPLE_IN[0], mx - 56, p)
        ay = lerp(APPLE_IN[1], my - 44, p)
        draw_polys(c, apple(ax, ay, r=28))
    elif i < 290:
        # apple carried near her hands/face during the flight.
        draw_polys(c, apple(mx - 56, my - 44, r=28))
    elif i < 315:
        # eating: apple shrinks near her mouth.
        s = 1.0 - 0.55 * ease((i - 290) / 25.0, "in")
        draw_polys(c, apple(mx - 50, my - 48, r=28 * s))
    else:
        # ---- core drops, falls through the black frame, bounces once ---- #
        # release point ~ Marisa's last hand position
        rx, ry = marisa_xy(314)
        sx, sy = rx - 50, ry - 40
        k = (i - 315) / float(NFR - 315)        # 0..1 over the remaining frames
        # one damped bounce in y, drifting toward frame centre in x
        floor = 600
        if k < 0.45:
            fy = ease(k / 0.45, "in")
            y = lerp(sy, floor, fy)
        else:
            kb = (k - 0.45) / 0.55
            y = floor - (floor - CORE_REST[1]) * ease(kb, "out") \
                - 70 * math.sin(math.pi * kb)   # the bounce hop
        x = lerp(sx, CORE_REST[0], ease(k, "in_out"))
        spin = 0.6 * math.sin(2 * math.pi * k * 2)
        draw_polys(c, transform_polys(apple_core(x, y, r=24),
                                      rotate=spin, origin=(x, y)))


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw, bg=BLACK)
    print(f"Scene 3: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

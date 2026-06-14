"""Scene 34 -- The spinning yin-yang orb (f6270-6420, 150 fr).  OUTRO begins.

33->34: opens on the yin-yang the reaching hands curled into (r=360, centre
(480,360), angle=pi -- light/white on the left, dark/black on the right, matching
Scene 33's left-white / right-black split).  The taiji orb spins for several
seconds (ref f6301 ~ local f31, ref f6391 ~ local f121), decelerating back to the
same angle=pi so its two eyes seed the final two shots.

34->35: the dark region's white eye becomes Marisa; the light region's black eye
becomes Reimu (Scene 35 opens on the same light-left / dark-right division).
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: E402,F403
from shapes import draw_yinyang  # noqa: E402

SCENE_START_FRAME = 6270
SCENE_END_FRAME = 6420
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / 30.0   # 5.0 s

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

ORB = (480.0, 360.0)
ORB_R = 360.0
SPINS = 3                    # full turns, decelerating; ends back at angle=pi


def draw(c, u, i, t):
    c.fill(BLACK)
    angle = math.pi + ease(u, "out") * (SPINS * 2.0 * math.pi)
    draw_yinyang(c, ORB[0], ORB[1], ORB_R, angle=angle)


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw, bg=BLACK)
    print(f"Scene 34: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

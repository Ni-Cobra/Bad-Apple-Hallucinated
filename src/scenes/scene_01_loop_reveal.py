"""Scene 1 -- Black screen / zoom-out reveal (loop point).  Frames 0-119.

SCENES.md: opens on a SOLID BLACK screen (f15 still black); the camera pulls
back and the blackness is revealed to be Reimu's silhouette seen from BEHIND
(big hair bow, detached sleeves); by f120 she is a full-figure black silhouette.
Polarity: solid black -> resolves to B-on-W. Loops from Scene 35 (which ends on
solid black) and continues into Scene 2.

Realisation: we zoom OUT from deep inside her torso (a solid interior point), so
the opening frames are pure black; an eased scale brings the whole back-view
figure into frame by the end.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: F401,F403
from shapes import reimu_back, draw_polys, transform_polys  # noqa: E402

SCENE_START_FRAME = 0
SCENE_END_FRAME = 120
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / FPS  # 4.0 s

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

# Zoom-out parameters: start so far inside the torso that the frame is solid
# black, hold briefly (f15 must still be black), then ease out to full figure.
ZOOM_ORIGIN = (480, 400)     # a solid interior point of reimu_back's torso
ZOOM_START = 8.5             # initial scale (figure covers the whole viewport)
HOLD = 0.10                  # fraction of the scene held fully black


def draw(c: Canvas, u: float, i: int, t: float) -> None:
    reveal = ease(clamp01((u - HOLD) / (1.0 - HOLD)), "in_out")
    scale = lerp(ZOOM_START, 1.0, reveal)
    figure = transform_polys(reimu_back(), scale=scale, origin=ZOOM_ORIGIN)
    draw_polys(c, figure)


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw)
    print(f"Scene 1: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

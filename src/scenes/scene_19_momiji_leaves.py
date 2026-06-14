"""Scene 19 -- Momiji's vertical slash; the screen shatters into leaves
(f3750-3810, 60 fr). W-on-B -> flips to B-on-W as the quadrants become leaves.

Opens on the persisting horizontal white beam from Scene 18 (W-on-B). Momiji
(wolf ears, sword) leaps through and slashes VERTICALLY -- a white vertical line
grows down the frame, crossing the beam, so the frame is now quartered. On the
accent the four quadrants peel away and turn into giant falling LEAVES (maple +
ginkgo, the shared shapes) and the polarity flips to B-on-W (ref f3796).

18->19: the horizontal beam at BEAM_Y is continuous. 19->20: the leaves rain
down onto Sanae's scene (Scene 20, B-on-W). Built inline; Momiji is a
blink-and-miss transition character.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: E402,F403
from shapes import (  # noqa: E402
    leaf_maple, leaf_ginkgo, ellipse_poly, head, dress_body, draw_polys,
)

SCENE_START_FRAME = 3750
SCENE_END_FRAME = 3810
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / 30.0   # 2.0 s

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

BEAM_Y = 336        # must match Scene 18
FLIP = 24           # local frame: quadrants -> leaves, polarity flips to B-on-W

# four leaves, one per quadrant: (builder, x0, y0, fall, spin, radius)
LEAVES = [
    (leaf_maple,  244, 196, 150, -0.34, 140),
    (leaf_ginkgo, 716, 168, 168,  0.40, 138),
    (leaf_ginkgo, 252, 520, 130, -0.52, 126),
    (leaf_maple,  708, 540, 150,  0.32, 144),
]


def momiji(prog):
    """A small wolf-tengu figure sweeping downward as she slashes."""
    cx = 480
    cy = lerp(110, 600, prog)
    polys = []
    polys += ellipse_poly(cx, cy - 4, 40, 38)              # short hair
    polys += [[(cx - 30, cy - 22), (cx - 8, cy - 26), (cx - 22, cy - 66)]]   # wolf ears
    polys += [[(cx + 30, cy - 22), (cx + 8, cy - 26), (cx + 22, cy - 66)]]
    polys += head(cx, cy, 32)
    polys += dress_body(cx, cy + 30, cy + 118, cy + 214, 38, 52, 88)
    return polys


def draw_leaves(c, i):
    p = (i - FLIP) / float(SCENE_END_FRAME - SCENE_START_FRAME - 1 - FLIP)
    for fn, x0, y0, fall, spin, r in LEAVES:
        y = y0 + fall * ease(p, "in")
        x = x0 + 38 * math.sin(p * 3.0 + x0)
        draw_polys(c, fn(x, y, r, spin * p * 2.0))


def draw(c, u, i, t):
    if i < FLIP:
        # Phase A (W-on-B): draw black, invert -> white cross + Momiji on black.
        c.rectangle(0, BEAM_Y - 4, 960, BEAM_Y + 4)        # horizontal beam (from sc18)
        slash = clamp01((i - 4) / 14.0)
        if slash > 0:
            c.rectangle(475, 0, 485, lerp(0, 720, ease(slash, "out")))   # vertical slash
        if i < 15:
            draw_polys(c, momiji(clamp01(i / 14.0)))
        c.invert()
    else:
        # Phase B/C (B-on-W): the four quadrants are now falling leaves.
        draw_leaves(c, i)


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw)
    print(f"Scene 19: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

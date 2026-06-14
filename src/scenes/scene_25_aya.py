"""Scene 25 -- Aya the reporter (f4650-4830, 180 fr). B-on-W (CHORUS 2 begins).

24->25 figure-ground FLIP: the black negative space between Yukari's and Tenshi's
two white profiles is re-read as a large black feathered crow wing filling the
left frame (ref f4666) -- polarity is now B-on-W. Pull back to the signature shot:
Aya in profile (facing left) with her tokin hat, wings folded behind, WRITING in
her notebook with a pen (ref f4741). Done writing, she TOSSES the pen over her
shoulder; it tumbles alone across the white frame (ref f4816).

25->26: the tumbling pen's shaft morphs into Suika's horn -- this scene ends on
the shared pen() shape isolated and tumbling so Scene 26 continues from it.

Aya + the crow wing built inline from the toolkit; the tossed pen is the shared
pen() handoff shape.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: E402,F403
from shapes import (  # noqa: E402
    head, circle_poly, ribbon, draw_polys, transform_polys, pen,
)

SCENE_START_FRAME = 4650
SCENE_END_FRAME = 4830
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / 30.0   # 6.0 s

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

A_END = 50          # crow wing fills the frame (ref f4666)
B_END = 122         # pull back to Aya writing in her notebook (ref f4741)
# 122..179 -> toss the pen; it tumbles alone across the frame (ref f4816)


def crow_wing(rx, ry, height=520, span=360, n=13, grow=1.0, flip=1):
    """A crow wing rooted at (rx, ry) (top), hanging down with the wing tip at the
    bottom: a smooth leading edge bulging to the RIGHT and a clearly FEATHERED
    trailing edge down the LEFT. *flip*=-1 mirrors it (feathers to the right) for
    a wing folded behind a left-facing figure. *grow* scales it for the reveal."""
    H = height * grow
    S = span * grow
    lead = bezier_points([(rx, ry),
                          (rx + S * 0.92, ry + H * 0.12),
                          (rx + S * 0.52, ry + H * 0.56),
                          (rx + S * 0.06, ry + H)], 18)
    tip = lead[-1]
    edge = []
    for k in range(n + 1):
        f = k / n
        # spine from tip back up to the root, bulging left
        bx = lerp(tip[0], rx - S * 0.12, f) - S * 0.32 * math.sin(math.pi * f)
        by = lerp(tip[1], ry + H * 0.02, f)
        fl = (0.25 + 0.75 * math.sin(math.pi * min(1.0, 0.10 + 0.95 * f))) * (0.17 * H)
        edge.append((bx, by))                              # inner notch
        edge.append((bx - fl, by + fl * 0.34))             # feather tip (out to the left)
    poly = lead + edge
    if flip == -1:
        poly = [(2 * rx - x, y) for x, y in poly]
    return [poly]


def aya(hx, hy, scale=1.0):
    """Aya in profile facing LEFT: tokin-topped head with a clear nose, short hair
    behind, a crow wing folded behind-right, writing in a notebook held in front
    with a pen."""
    R = 50
    polys = []
    # folded wing behind, to the lower-right (mirrored so feathers point right)
    polys += crow_wing(hx + 26, hy - 14, height=300, span=150, n=9, flip=-1)
    # short jagged hair bob behind the head (to the right) -- kept off the face side
    polys += [[(hx + 6, hy - R * 0.95), (hx + R * 0.7, hy - R * 0.78),
               (hx + R * 1.04, hy - R * 0.2), (hx + R * 1.0, hy + R * 0.34),
               (hx + R * 1.18, hy + R * 0.5), (hx + R * 0.66, hy + R * 0.62),
               (hx + R * 0.86, hy + R * 0.9), (hx + 8, hy + R * 0.78)]]
    polys += head(hx, hy, R)
    polys += circle_poly(hx + 6, hy - R * 0.92, 15)                  # bun
    polys += [[(hx - 6, hy - R * 0.9), (hx + 6, hy - R * 1.5), (hx + 18, hy - R * 0.9)]]  # tokin
    polys += [[(hx - R * 0.86, hy - 12), (hx - R * 1.2, hy + 6),
               (hx - R * 0.82, hy + 20)]]                            # nose (faces left)
    neck_y = hy + R * 0.9
    polys += [[(hx - 14, neck_y), (hx + 16, neck_y),
               (hx + 18, neck_y + 30), (hx - 16, neck_y + 30)]]      # neck
    polys += [[(hx - 24, neck_y + 24), (hx + 24, neck_y + 28),
               (hx + 30, neck_y + 150), (hx - 48, neck_y + 150)]]    # torso, leaning forward
    # notebook held in front (lower-left), tilted
    nb_cx, nb_cy = hx - 96, hy + 150
    notebook = transform([(nb_cx - 54, nb_cy - 40), (nb_cx + 54, nb_cy - 40),
                          (nb_cx + 54, nb_cy + 40), (nb_cx - 54, nb_cy + 40)],
                         rotate=-0.25, origin=(nb_cx, nb_cy))
    polys += [notebook]
    # arms: near (right) hand brings the pen across; far (left) supports the notebook
    polys += ribbon([(hx + 10, neck_y + 42), (hx - 42, hy + 140), (nb_cx + 38, nb_cy - 8)], [15, 11, 8])
    polys += ribbon([(hx - 14, neck_y + 46), (hx - 62, hy + 150), (nb_cx - 8, nb_cy + 18)], [14, 10, 8])
    polys += pen(nb_cx + 22, nb_cy - 12, length=118, angle=-0.30)    # the pen, writing
    if scale != 1.0:
        polys = transform_polys(polys, scale=scale, origin=(hx, hy))
    return polys


def draw(c, u, i, t):
    # ---- Phase A: crow wing fills the frame (figure-ground flip resolve) -----
    if i < A_END:
        grow = lerp(0.74, 1.0, ease(clamp01(i / 24.0), "out"))
        draw_polys(c, crow_wing(330, 36, height=560, span=380, n=15, grow=grow))
        return

    # ---- Phase B: pull back to Aya writing ----------------------------------
    if i < B_END:
        b = (i - A_END) / float(B_END - A_END)
        scale = lerp(1.45, 1.0, ease(b, "in_out"))
        hx = lerp(470, 540, ease(b, "in_out"))
        hy = lerp(250, 244, ease(b, "in_out"))
        draw_polys(c, aya(hx, hy, scale=scale))
        return

    # ---- Phase C: toss the pen; it tumbles alone across the frame -----------
    cprog = (i - B_END) / float(SCENE_END_FRAME - SCENE_START_FRAME - B_END)  # 0..1
    if cprog < 0.5:
        draw_polys(c, aya(540, 244, scale=1.0))            # still present, lowering the hand
    p = ease(cprog, "in_out")
    px = lerp(470, 250, p)
    py = lerp(420, 250, p) - 120 * math.sin(math.pi * p)   # arched toss
    ang = lerp(-0.3, -1.4, p) + 2.4 * p                     # tumbling rotation
    draw_polys(c, pen(px, py, length=150, angle=ang))


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw)              # B-on-W (default)
    print(f"Scene 25: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

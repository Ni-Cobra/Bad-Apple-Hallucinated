"""Scene 11 -- Eiki Shiki at the black/white seam.
Frames 2370-2525 (156 fr).

SCENES.md: on the perfectly split screen (LEFT black / RIGHT white) Eiki appears
straddling the centerline as a MIRRORED DUAL-POLARITY silhouette -- white on the
black side, black on the white side (ref f2386, one of the most reproduced frames
of the video). She raises and swings her Rod of Remorse, held vertically ON the
seam (ref f2461). Polarity = the split, both at once.

Continuity in (10->11): Scene 10 ended on a clean 50/50 split, LEFT half black /
RIGHT half white at x=480; this scene opens on that exact field and Eiki rises at
the seam. Handoff out (11->12): the vertical Rod morphs into Mokou on the chorus-1
downbeat -- Scene 12 flips to W-on-B (full black), so the rod is left standing
vertical and centered on the last frame for Scene 12 to grow Mokou out of it.

Eiki is built inline (tall tate-eboshi judge's cap + flaring robe) ONCE, centered
on the seam, then drawn twice via clip_polys_x: the x<=480 half in white (on the
black left field) and the x>=480 half in black (on the white right field), so the
seam mirrors exactly. The shared `rod_of_remorse` rides the seam the same way.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: F401,F403
from shapes import (  # noqa: E402
    head, dress_body, limb, ellipse_poly,
    rod_of_remorse, draw_polys, transform_polys, clip_polys_x,
)

SCENE_START_FRAME = 2370
SCENE_END_FRAME = 2526
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / FPS  # 5.2 s
NFR = SCENE_END_FRAME - SCENE_START_FRAME                     # 156

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

CX = 480          # the seam (matches Scene 10's split and Scene 12's morph axis)
GRIP_Y = 472      # where her clasped hands hold the rod
A_END = 44        # Eiki rises at the seam
B_END = 112       # raises the Rod to full vertical height


def eiki(cx):
    """Eiki, frontal and symmetric about the seam: tall tate-eboshi judge's cap,
    head, a wide flaring robe, arms clasped at the centre on the rod."""
    polys = []
    hy = 235                                   # head centre
    # tall eboshi cap (slightly bulbous folded top)
    polys += [[(cx - 36, hy - 28), (cx - 22, hy - 150), (cx - 26, hy - 172),
               (cx, hy - 180), (cx + 26, hy - 172), (cx + 22, hy - 150),
               (cx + 36, hy - 28)]]
    polys += head(cx, hy, 41)
    # flaring judge's robe (long, wide hem to the floor)
    polys += dress_body(cx, 305, 440, 706, 46, 66, 150)
    # symmetric arms meeting at the clasped hands on the seam
    polys += limb([(cx - 46, 318), (cx - 40, 402), (cx, GRIP_Y)], [15, 12, 9])
    polys += limb([(cx + 46, 318), (cx + 40, 402), (cx, GRIP_Y)], [15, 12, 9])
    return polys


def draw(c: Canvas, u: float, i: int, t: float) -> None:
    # --- the split field: black left (bg), white right half ---
    c.rectangle(CX, 0, WIDTH, HEIGHT, color=WHITE)

    # rise-in scale for the whole figure (grows up from the floor)
    if i < A_END:
        g = lerp(0.6, 1.0, ease(clamp01(i / A_END), "out"))
    else:
        g = 1.0
    sway = 0.0  # stays centred on the seam (the mirror must hold)

    fig = eiki(CX)
    fig = transform_polys(fig, scale=g, origin=(CX, 706), translate=(sway, 0))

    # the Rod of Remorse, vertical on the seam: short while she rises, then lifts
    # to full height (ref f2461) and is held for the Scene 12 morph handoff.
    if i < A_END:
        rod_len = 80
    elif i < B_END:
        rod_len = lerp(80, 312, ease((i - A_END) / (B_END - A_END), "in_out"))
    else:
        rod_len = 312
    rod = rod_of_remorse(CX, GRIP_Y, length=rod_len, angle=-math.pi / 2)
    rod = transform_polys(rod, scale=g, origin=(CX, 706))

    allpolys = fig + rod
    # dual polarity: left half white (on black), right half black (on white)
    draw_polys(c, clip_polys_x(allpolys, CX, "left"), color=WHITE)
    draw_polys(c, clip_polys_x(allpolys, CX, "right"), color=BLACK)


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw, bg=BLACK)
    print(f"Scene 11: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

"""Scene 21 -- Hina's pirouette wipe (f3930-3990, 60 fr). B-on-W.

Hina bursts in and pirouettes across the frame, skirt flared wide by the spin
(ref f3976), "wiping" the leaves and Sanae off the screen -- a literal spin
transition (she is the misfortune goddess always depicted spinning). She is a
black silhouette on white throughout.

20->21: Hina bursts in over Scene 20's caught-leaf close-up (both B-on-W).
21->22: her wipe clears the stage for the Moriya gods (Scene 22 Kanako rises in,
stays B-on-W). Built inline: twin up-swept hair tails + top bow + big flared
bell skirt; the spin is an x-squash pulse + hem sway + arm swing.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: E402,F403
from shapes import (  # noqa: E402
    ellipse_poly, head, ribbon, leaf_maple, leaf_ginkgo,
    draw_polys, transform_polys,
)

SCENE_START_FRAME = 3930
SCENE_END_FRAME = 3990
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / 30.0   # 2.0 s

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

TURNS = 2.4         # full pirouette turns across the scene


def hina(cx, spin, sway, sx, scale=1.0):
    """Pirouetting Hina. *spin* drives arm/hair phase, *sway* slides the flared
    hem, *sx* is the x-squash (figure facing -> edge-on as she turns)."""
    hy = 150
    polys = []
    # twin up-swept hair tails + top bow (the identifying feature)
    polys += ribbon([(cx - 8, hy - 30), (cx - 46, hy - 96), (cx - 70, hy - 150)],
                    [16, 10, 3])                            # left tail up-out
    polys += ribbon([(cx + 8, hy - 30), (cx + 46, hy - 96), (cx + 70, hy - 150)],
                    [16, 10, 3])                            # right tail up-out
    polys += ellipse_poly(cx - 26, hy - 40, 22, 16)         # bow loop L
    polys += ellipse_poly(cx + 26, hy - 40, 22, 16)         # bow loop R
    polys += ellipse_poly(cx, hy - 40, 10, 12)              # bow knot
    # head + hair frame
    polys += ellipse_poly(cx, hy, 48, 50)                   # hair behind
    polys += head(cx, hy + 2, 42)
    # bodice
    polys += [[(cx - 40, hy + 40), (cx + 40, hy + 40),
               (cx + 52, hy + 150), (cx - 52, hy + 150)]]
    # arms swung out (swing with the spin)
    aL = 0.5 + 0.4 * math.sin(spin)
    aR = 0.5 - 0.4 * math.sin(spin)
    polys += ribbon([(cx - 40, hy + 70), (cx - 120, hy + 60 + 80 * aL),
                     (cx - 168, hy + 40 + 150 * aL)], [16, 12, 7])
    polys += ribbon([(cx + 40, hy + 70), (cx + 120, hy + 60 + 80 * aR),
                     (cx + 168, hy + 40 + 150 * aR)], [16, 12, 7])
    # big flared bell skirt (waist -> very wide pointed hem), sways with the spin
    waist_y = hy + 150
    hem_y = 660
    hw = 250
    skirt = [(cx - 54, waist_y), (cx + 54, waist_y)]
    pts = 9
    for k in range(pts + 1):
        f = k / pts
        x = cx + hw - 2 * hw * f + sway
        dip = 26 if k % 2 == 0 else 0          # scalloped/pointed hem
        skirt.append((x, hem_y + dip))
    polys += [skirt]
    # apply the spin x-squash about the central axis, then a slight body tilt
    polys = [[(cx + (x - cx) * sx, y) for x, y in poly] for poly in polys]
    polys = transform_polys(polys, rotate=0.10 * math.sin(spin * 0.5),
                            origin=(cx, hy + 220))
    if scale != 1.0:
        polys = transform_polys(polys, scale=scale, origin=(cx, hy + 220))
    return polys


# a couple of leftover leaves the pirouette sweeps away in the first frames
SWEPT = [(leaf_maple, 150, 250, -0.4, 120), (leaf_ginkgo, 820, 300, 0.5, 116)]


def draw(c, u, i, t):
    # leftover leaves fly off-frame as Hina's spin "wipes" the stage
    fly = ease(clamp01(i / 18.0), "in")
    for fn, x0, y0, spin0, r in SWEPT:
        x = x0 + (x0 - 480) * 1.8 * fly
        y = y0 - 120 * fly
        if fly < 1.0:
            draw_polys(c, fn(x, y, r, spin0 + fly * 2))
    spin = u * TURNS * 2 * math.pi
    sx = 0.34 + 0.66 * abs(math.cos(spin))      # facing -> edge-on pulse
    sway = 46 * math.sin(spin)
    grow = lerp(0.82, 1.0, ease(clamp01(i / 10.0), "out"))
    draw_polys(c, hina(480, spin, sway, sx, scale=grow))


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw)
    print(f"Scene 21: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

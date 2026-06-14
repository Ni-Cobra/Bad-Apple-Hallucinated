"""Scene 33 -- PC-98 Marisa upside-down; the two reach for each other (f6090-6270,
180 fr).  Dual polarity -- the video's thesis made literal: left half is a WHITE
field (black inverted Marisa), right half is a BLACK field (white Reimu).

32->33: opens on Scene 32's risen white Reimu on black.  A white vertical column
grows where the water was; a BLACK Marisa hangs upside-down inside it (ref f6106).
The column widens leftward into a full left-white / right-black 50/50 split
(ref f6181), Marisa drifting to the top-left, Reimu to the lower-right.  The two
stretch their hands toward each other across the seam (ref f6241).

33->34: as the hands meet, the straight seam curls into a yin-yang that grows to
fill the frame -- Scene 34 opens on that orb (same r=360, angle=pi, centre 480,360).
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: E402,F403
from shapes import (  # noqa: E402
    reimu_hairdown, witch_hat, head, long_hair, dress_body, limb,
    draw_polys, transform_polys, ribbon, draw_yinyang,
)

SCENE_START_FRAME = 6090
SCENE_END_FRAME = 6270
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / 30.0   # 6.0 s

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

SEAM = 480.0
REIMU_DY = 44.0             # Scene 32's hand-off position (frame 0 must match)

BAND_IN = 6                 # the white column starts to appear
SPLIT_DONE = 86            # full 50/50 split reached (ref f6181 ~ local f91)
REACH_DONE = 152           # hands meet at the seam (ref f6241 ~ local f151)
CURL_END = 180             # seam fully curled into the yin-yang (-> Scene 34)


def marisa_pc98(cx, foot_y):
    """Old-works Marisa, upright & canonical: witch hat + long hair + cloak-dress.
    Built upright; the scene flips her 180 deg to hang her upside-down."""
    polys = []
    hy = foot_y - 440
    polys += long_hair(cx, hy - 6, 50, 250)
    polys += head(cx, hy, 42)
    polys += witch_hat(cx, hy - 30, height=120, brim_w=104, tip_dx=46)
    neck, waist, hem = hy + 40, hy + 130, foot_y - 12
    polys += dress_body(cx, neck, waist, hem, 52, 70, 120)
    polys += limb([(cx - 44, neck + 8), (cx - 70, waist), (cx - 72, waist + 64)], [13, 10, 7])
    polys += limb([(cx + 44, neck + 8), (cx + 70, waist), (cx + 72, waist + 64)], [13, 10, 7])
    return polys


# canonical Marisa, pre-flipped to hang head-down about her own centre (480, 380)
_MARISA_FLIPPED = transform_polys(marisa_pc98(480, 600), rotate=math.pi, origin=(480, 380))


def marisa_hanging(cx, cy, scale=0.72):
    """The upside-down Marisa centred at (cx, cy)."""
    return transform_polys(_MARISA_FLIPPED, scale=scale,
                           translate=(cx - 480, cy - 380), origin=(480, 380))


def reimu_white(cx, dy, scale=1.0):
    return transform_polys(reimu_hairdown(480), translate=(cx - 480, dy),
                           scale=scale, origin=(480, 360))


def draw(c, u, i, t):
    c.fill(BLACK)

    # --- curl-out into the yin-yang (last beat -> Scene 34) -------------------
    if i >= REACH_DONE:
        curl = ease((i - REACH_DONE) / float(CURL_END - REACH_DONE), "in_out")
        # figures still visible while the orb grows over them, then swallowed
        if curl < 0.5:
            _draw_split(c, 1.0, reach=1.0)
        draw_yinyang(c, SEAM, 360.0, max(1.0, 360.0 * curl), angle=math.pi)
        return

    # progress of the split opening and of the reach
    sp = ease(clamp01((i - BAND_IN) / float(SPLIT_DONE - BAND_IN)), "in_out")
    reach = ease(clamp01((i - SPLIT_DONE) / float(REACH_DONE - SPLIT_DONE)), "in_out")
    _draw_split(c, sp, reach=reach)


def _draw_split(c, sp, reach=0.0):
    """Draw the dual-polarity composition. sp = split-open amount [0,1],
    reach = hand-reach amount [0,1]."""
    # white left field grows from the seam leftward to fill the half
    lx = lerp(SEAM, 0.0, sp)
    if lx < SEAM - 1:
        c.rectangle(lx, 0, SEAM, HEIGHT, color=WHITE)

    # --- black Marisa, hanging upside-down, drifting to the top-left ----------
    mcx = lerp(442.0, 232.0, sp)
    mcy = lerp(250.0, 214.0, sp)
    draw_polys(c, marisa_hanging(mcx, mcy), color=BLACK)
    if reach > 0.0:                                # reaching arm toward the seam
        hx, hy = lerp(mcx + 36, SEAM - 6, reach), lerp(mcy + 96, 352.0, reach)
        draw_polys(c, ribbon([(mcx + 30, mcy + 70), ((mcx + hx) / 2, (mcy + 90 + hy) / 2),
                              (hx, hy)], [12, 9, 6]), color=BLACK)

    # --- white Reimu, in the black right field, looking up -------------------
    rcx = lerp(480.0, 648.0, sp)
    rdy = lerp(REIMU_DY, 96.0, sp)
    draw_polys(c, reimu_white(rcx, rdy), color=WHITE)
    if reach > 0.0:                                # reaching arm toward the seam
        sx, sy = rcx - 56, rdy + 300
        hx, hy = lerp(sx, SEAM + 6, reach), lerp(sy, 368.0, reach)
        draw_polys(c, ribbon([(sx, sy), ((sx + hx) / 2, (sy + hy) / 2 - 14),
                              (hx, hy)], [13, 10, 7]), color=WHITE)


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw, bg=BLACK)
    print(f"Scene 33: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

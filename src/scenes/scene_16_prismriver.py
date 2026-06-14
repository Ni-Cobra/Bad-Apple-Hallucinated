"""Scene 16 -- Prismriver Ensemble concert (f3363-3570, 207 frames, B-on-W).

The instrumental interlude. On Scene 15's white field, the three poltergeist
sisters rise/fade in as BLACK silhouettes -- Lyrica at her keyboard (left),
Merlin on trumpet (centre), Lunasa on violin (right) -- each with a soft GRAY
floor shadow (the documented gray element unique to this scene). The camera
establishes the trio small at the bottom (ref f3376), pushes in to the full
shadowed trio (ref f3451), tours to a two-shot of the right pair with Lunasa's
violin prominent (ref f3511), then settles on Lyrica, who lifts a hand and WAVES
as if introducing the next act -- the gesture that cues Scene 17's face chain.

16->17 handoff: ends on Lyrica's intro wave; Scene 17 cuts to Chen (stays B-on-W).
Sisters built inline (dress_body + instrument props). Opens on solid white so the
15->16 boundary is continuous with Scene 15's whiteout.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: E402,F403
from shapes import (  # noqa: E402
    ellipse_poly, ribbon, dress_body, head, draw_polys,
)

SCENE_START_FRAME = 3363
SCENE_END_FRAME = 3570
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / 30.0   # 6.9 s

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

GRAY = 120     # soft floor-shadow gray (B-on-W: darker than white, lighter than ink)

# Stage layout (authored in screen coords for the full-trio "f3451" framing) -----
LYRICA_X = 210
MERLIN_X = 468
LUNASA_X = 740
FLOOR_Y = 548


# ---------------------------------------------------------------------------
# Hats / crowns
# ---------------------------------------------------------------------------

def tiara(cx, cy, w=30, spikes=4):
    pts = [(cx - w, cy + 10)]
    for k in range(spikes * 2 + 1):
        f = k / (spikes * 2)
        pts.append((cx - w + 2 * w * f, cy - (16 if k % 2 else 2)))
    pts.append((cx + w, cy + 10))
    return [pts]


def star_crown(cx, cy, h=44):
    return [[(cx - 26, cy + 22), (cx - 12, cy - 4), (cx, cy - h),
             (cx + 12, cy - 4), (cx + 26, cy + 22)]]


def antenna_hat(cx, cy):
    polys = ellipse_poly(cx, cy + 8, 30, 17)
    polys += ribbon([(cx - 4, cy), (cx - 10, cy - 30)], [4, 2])
    polys += ribbon([(cx + 12, cy + 2), (cx + 20, cy - 26)], [4, 2])
    return polys


# ---------------------------------------------------------------------------
# The three sisters (inline) -- screen coords, black ink
# ---------------------------------------------------------------------------

def lyrica(wave_t=0.0):
    cx = LYRICA_X
    polys = []
    # keyboard: a slanted slab in front, lower-left
    polys.append([(cx - 158, 472), (cx - 14, 436), (cx + 44, 470), (cx - 100, 516)])
    polys += dress_body(cx, 248, 372, 512, 42, 56, 92)        # bent-over short dress
    polys += head(cx - 4, 210, 34)
    polys += tiara(cx - 4, 178, 30)
    polys += ribbon([(cx - 30, 274), (cx - 82, 364), (cx - 116, 452)], [12, 9, 6])  # L arm to keys
    if wave_t < 0.5:
        polys += ribbon([(cx + 26, 274), (cx + 8, 360), (cx - 34, 452)], [12, 9, 6])  # R arm to keys
    else:
        wx = cx + 56 + 16 * math.sin(wave_t * 7.0)           # raised hand, waving
        polys += ribbon([(cx + 26, 268), (cx + 58, 206), (wx, 150)], [12, 9, 6])
    return polys


def merlin(bob=0.0):
    cx = MERLIN_X
    polys = []
    polys += dress_body(cx, 232, 366, FLOOR_Y, 46, 62, 112, sway=0.5 * bob)
    polys += head(cx, 192 + bob, 36)
    polys += star_crown(cx, 150 + bob, 46)
    mouth = (cx - 28, 188 + bob)
    bell = (cx - 158, 150 + bob)
    polys += ribbon([(cx - 40, 252), (cx - 72, 214), (mouth[0] + 4, mouth[1] - 2)], [12, 9, 6])
    polys += ribbon([(cx + 40, 252), (cx + 8, 208), (mouth[0] + 6, mouth[1] + 4)], [12, 9, 6])
    polys += ribbon([mouth, (cx - 92, 168 + bob), bell], [7, 9, 5])   # trumpet tube
    polys += ellipse_poly(bell[0] - 6, bell[1] - 2, 22, 26, rot=0.5)  # bell
    return polys


def lunasa(bow_phase=0.0):
    cx = LUNASA_X
    polys = []
    polys += dress_body(cx, 232, 366, FLOOR_Y, 46, 62, 112)
    polys += head(cx - 8, 188, 36)
    polys += antenna_hat(cx - 8, 152)
    vx, vy = cx - 56, 214                                     # violin under chin
    polys += ellipse_poly(vx, vy, 32, 18, rot=-0.45)
    polys += ribbon([(vx - 20, vy - 8), (vx - 74, vy - 48)], [5, 3])  # neck + scroll
    polys += ribbon([(cx - 38, 252), (cx - 72, 226), (vx - 62, vy - 40)], [12, 9, 6])  # L arm
    # bow drawn across the strings (slides with bow_phase)
    slide = 24 * math.sin(bow_phase)
    bstart = (vx - 96 + slide, vy - 16 + slide * 0.3)
    bend = (vx + 44 + slide, vy + 34 + slide * 0.3)
    polys += ribbon([bstart, bend], [3, 3])
    polys += ribbon([(cx + 40, 252), (cx + 18, 262), (bend[0] + 8, bend[1] + 2)], [12, 9, 6])  # R arm
    return polys


def shadow_polys():
    """Three skewed gray parallelograms on the floor under the sisters."""
    out = []
    for cx, w in ((LYRICA_X - 40, 150), (MERLIN_X, 120), (LUNASA_X, 120)):
        out.append([(cx - w * 0.5, FLOOR_Y + 14), (cx + w * 0.45, FLOOR_Y + 14),
                    (cx - w * 0.1, FLOOR_Y + 104), (cx - w * 0.95, FLOOR_Y + 104)])
    return out


# ---------------------------------------------------------------------------
# Camera tour
# ---------------------------------------------------------------------------

def cam_apply(polys, scale, focus, extra=(0.0, 0.0)):
    fx, fy = focus
    ex, ey = extra
    return [[((x - fx) * scale + 480 + ex, (y - fy) * scale + 360 + ey)
             for x, y in p] for p in polys]


def camera(i):
    """Return (scale, focus, extra) for frame i."""
    if i < 30:                                   # rise/fade in, wide framing
        s = ease(i / 30.0, "out")
        return 0.62, (470.0, 200.0), (0.0, lerp(420.0, 0.0, s))
    if i < 66:                                   # push in to the full trio
        u = ease((i - 30) / 36.0, "in_out")
        return lerp(0.62, 1.0, u), (lerp(470.0, 480.0, u), lerp(200.0, 360.0, u)), (0.0, 0.0)
    if i < 112:                                  # hold the full shadowed trio (f3451)
        u = ease((i - 66) / 46.0, "in_out")
        return lerp(1.0, 1.08, u), (480.0, 360.0), (0.0, 0.0)
    if i < 166:                                  # tour to the right pair (f3511)
        u = ease((i - 112) / 54.0, "in_out")
        return lerp(1.08, 1.7, u), (lerp(480.0, 628.0, u), lerp(360.0, 300.0, u)), (0.0, 0.0)
    u = ease(clamp01((i - 166) / 30.0), "in_out")  # settle on Lyrica for the wave
    return lerp(1.7, 1.5, u), (lerp(628.0, 232.0, u), lerp(300.0, 250.0, u)), (0.0, 0.0)


def draw(c, u, i, t):
    scale, focus, extra = camera(i)
    bob = 5.0 * math.sin(i * 0.22)
    wave_t = clamp01((i - 185) / 22.0)

    draw_polys(c, cam_apply(shadow_polys(), scale, focus, extra), color=GRAY)
    figs = lyrica(wave_t) + merlin(bob) + lunasa(i * 0.30)
    draw_polys(c, cam_apply(figs, scale, focus, extra))


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw)
    print(f"Scene 16: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

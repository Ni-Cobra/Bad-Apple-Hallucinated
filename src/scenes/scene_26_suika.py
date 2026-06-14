"""Scene 26 -- Suika drains the gourd (f4830-5040, 210 fr). B-on-W.

25->26: the tumbling pen (Scene 25's end, the shared pen() shape near (250,250),
tilted ~1.0 rad) morphs into one of Suika's oni HORNS, and Suika grows in beneath
it hoisting her two-lobed sake GOURD (chain links readable, ref f4861). She drinks
with theatrical abandon -- gourd raised to her mouth, free arm flung out (ref
f4951). The gourd runs dry: raised overhead and tipped fully upside down it yields
ONE last falling DROP while the camera tilts up off her (ref f5041 ~= Scene 27's
opening frame).

26->27: the camera follows the falling drop -> Scene 27 continues it (drop becomes
Alice seen from above). This scene ends on the shared drop() high in frame.

Suika built inline from the toolkit; gourd/drop are the shared handoff shapes.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: E402,F403
from shapes import (  # noqa: E402
    head, ellipse_poly, ribbon, circle_poly, draw_polys, transform_polys,
    pen, gourd, drop,
)

SCENE_START_FRAME = 4830
SCENE_END_FRAME = 5040
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / 30.0   # 7.0 s

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

A_END = 30          # pen->horn morph + Suika assembles, hoisting the gourd (ref f4861)
B_END = 120         # hoist -> big drink, gourd at the mouth (ref f4951)
# 120..209 -> drain: gourd overhead & tipped, last drop falls, camera tilts up (f5041)

HX, HY = 470, 238   # Suika's head centre at the hoist pose
R = 46


def left_horn(htx, hty):
    """Suika's left oni horn (the pen-morph target) at head centre (htx,hty)."""
    return [(htx - 30, hty - R * 0.7), (htx - 50, hty - R * 1.95), (htx - 12, hty - R * 0.95)]


def suika(hx, hy, gx, gy, grot, fx, fy, drink=0.0, scale=1.0):
    """Suika facing LEFT: two oni horns + a huge trailing ponytail; her front
    (left) arm raises the two-lobed gourd to (gx,gy) near her mouth and the back
    (right) arm is flung out to (fx,fy); a chain hangs from the gourd. *drink*
    (0..1) tilts her head back as she swigs."""
    polys = []
    htx = hx + 8 * drink
    hty = hy - 6 * drink
    # huge ponytail: thick, sweeping down-right behind her, very long
    polys += ribbon([(hx + 30, hy - 28), (hx + 80, hy + 44),
                     (hx + 98, hy + 184), (hx + 78, hy + 332),
                     (hx + 52, hy + 470)], [34, 44, 38, 24, 6])
    polys += ellipse_poly(hx + 14, hy - 2, 50, 54)               # hair mass behind head
    polys += head(htx, hty, R)
    polys += [[(htx - R * 0.86, hty - 6 - 8 * drink),            # nose nub, faces LEFT
               (htx - R * 1.16, hty + 2 - 10 * drink),
               (htx - R * 0.82, hty + 14 - 6 * drink)]]
    polys += [left_horn(htx, hty)]                               # left horn
    polys += [[(htx + 6, hty - R * 0.82), (htx + 30, hty - R * 2.05),
               (htx + 34, hty - R * 0.78)]]                      # right horn
    neck_y = hy + R * 0.82
    polys += [[(hx - 22, neck_y), (hx + 30, neck_y),
               (hx + 40, neck_y + 132), (hx - 30, neck_y + 132)]]   # torso
    sy = neck_y + 132
    polys += [[(hx - 30, sy), (hx + 40, sy), (hx + 66, sy + 116),
               (hx - 58, sy + 116)]]                                # skirt
    fy2 = sy + 116
    polys += [[(hx - 30, fy2), (hx - 2, fy2), (hx - 10, fy2 + 94), (hx - 38, fy2 + 94)]]  # leg
    polys += [[(hx + 8, fy2), (hx + 40, fy2), (hx + 52, fy2 + 94), (hx + 22, fy2 + 94)]]  # leg
    # front (left) arm raising the gourd
    polys += ribbon([(hx - 20, neck_y + 20),
                     ((hx - 20 + gx) / 2 - 16, (neck_y + 20 + gy) / 2 + 22), (gx, gy)],
                    [16, 13, 9])
    # back (right) arm flung out
    polys += ribbon([(hx + 26, neck_y + 16),
                     ((hx + 26 + fx) / 2, (neck_y + 16 + fy) / 2), (fx, fy)],
                    [16, 12, 7])
    polys += transform_polys(gourd(gx, gy, r=62), rotate=grot, origin=(gx, gy))
    for k in range(6):                                           # chain hanging from the gourd
        f = (k + 0.6) / 6
        polys += ellipse_poly(lerp(gx, gx - 12, f), lerp(gy + 52, gy + 188, f), 7, 10)
    if scale != 1.0:
        polys = transform_polys(polys, scale=scale, origin=(hx, hy))
    return polys


def draw(c, u, i, t):
    # ---- Phase A: pen -> horn morph, Suika grows into the hoist pose ---------
    if i < A_END:
        if i < 16:                                  # pen morphs into the left horn
            m = ease(i / 16.0, "in_out")
            pen_poly = pen(lerp(250, 440, m), lerp(250, HY - R * 1.2, m),
                           length=lerp(150, 90, m), angle=lerp(1.0, -0.2, m))[0]
            draw_polys(c, [morph_polys(pen_poly, left_horn(HX, HY), m, n=64)])
            return
        g = ease((i - 16) / float(A_END - 16), "out")           # figure grows in
        draw_polys(c, suika(HX, HY, 330, 430, 0.3, 540, 40, drink=0.1,
                            scale=lerp(0.72, 1.0, g)))
        return

    # ---- Phase B: hoist -> big drink (gourd up to the mouth) -----------------
    if i < B_END:
        b = ease((i - A_END) / float(B_END - A_END), "in_out")
        gx = lerp(330, 352, b)
        gy = lerp(430, 172, b)
        grot = lerp(0.3, 1.95, b)
        fx = lerp(540, 770, b)
        fy = lerp(40, 150, b)
        draw_polys(c, suika(HX, HY, gx, gy, grot, fx, fy, drink=lerp(0.1, 1.0, b)))
        return

    # ---- Phase C: drain -- gourd raised high overhead & tipped, last drop ----
    cp = (i - B_END) / float(SCENE_END_FRAME - SCENE_START_FRAME - B_END)   # 0..1
    rise = ease(min(1.0, cp * 1.25), "in_out")
    gx = lerp(352, 470, rise)            # gourd swings up to centre-overhead
    gy = lerp(172, 78, rise)             # raised high, arm fully extended (stays visible)
    grot = lerp(1.95, math.pi + 0.4, rise)   # tips fully upside down to drain
    draw_polys(c, suika(HX, HY, gx, gy, grot, lerp(770, 600, cp), lerp(150, 300, cp), drink=1.0))
    # the last drop drips off the inverted gourd and arcs into open space to the
    # left (clear of her body); Scene 27's camera follows it from (406,239)
    if cp > 0.45:
        dp = ease(clamp01((cp - 0.45) / 0.55), "in")
        dx = lerp(gx - 30, 406, dp)
        dy = lerp(gy + 56, 239, dp)
        draw_polys(c, drop(dx, dy, r=20))


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw)              # B-on-W (default)
    print(f"Scene 26: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

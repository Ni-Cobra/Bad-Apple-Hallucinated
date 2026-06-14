"""Scene 10 -- Komachi on the Sanzu River; the screen is cut in half.
Frames 2130-2369 (240 fr).

SCENES.md: the petal becomes a white ferry boat drifting on black; Komachi stands
in it with her scythe over her shoulder (ref f2161). Close-up of Komachi swinging
the scythe across her body (ref f2251). At ~1:17-1:19 the scythe blade sweeps
across the screen and divides the entire frame into one black half and one white
half (wipe in progress, ref f2341). Polarity W-on-B -> ends as a 50/50 split.

Continuity in (9->10): Scene 9 ended on the single cherry petal magnified to fill
the frame (near-horizontal). Scene 10 opens on that same large petal and morphs it
into the boat hull (no flip; both W-on-B). Handoff out (10->11): the scythe wipe
leaves a clean vertical split -- LEFT half black, RIGHT half white -- and Eiki
rises straddling the seam (Scene 11). Shared shapes `sakura_petal`, `scythe` from
the asset library; Komachi (twin low tails + big scythe) is built inline.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: F401,F403
from shapes import (  # noqa: E402
    head, dress_body, limb, ellipse_poly, ribbon, circle_poly,
    sakura_petal, scythe, draw_polys, transform_polys,
)

SCENE_START_FRAME = 2130
SCENE_END_FRAME = 2370
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / FPS  # 8.0 s
NFR = SCENE_END_FRAME - SCENE_START_FRAME                      # 240

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

CX = 480
A_END = 50        # petal->boat, wide shot
B_END = 156       # close-up swing
SEAM_X = 480      # the split seam (matches Scene 11)

# Big near-horizontal petal (continues Scene 9's end) and the boat hull it morphs to.
PETAL_BIG = sakura_petal(480, 430, w=300, h=430, rot=math.pi / 2 - 0.12)[0]
BOAT = [(480 - 280, 430), (480 - 150, 472), (480 + 150, 472), (480 + 280, 430),
        (480 + 150, 410), (480 - 150, 410)]


def cam(polys, s, fx, fy):
    return transform_polys(polys, scale=s, origin=(fx, fy), translate=(480 - fx, 360 - fy))


def komachi(cx, cy, pole_ang=0.5, grip=None):
    """Komachi: twin low hair tails, vest+skirt, big scythe held by *pole_ang*
    (radians; +0.5 shoulders it up-right, -0.6 swings it up-left)."""
    polys = []
    gx, gy = grip if grip else (cx + 4, cy - 88)
    # scythe (canonical: blade at top, shaft down) rotated about its handle to the grip
    sc = scythe(0, 0, length=300, angle=math.pi / 2, blade=162, thick=10)
    polys += transform_polys(sc, rotate=pole_ang, origin=(0, 300),
                             translate=(gx, gy - 300))
    # hair + head
    polys += ellipse_poly(cx, cy - 156, 50, 46)
    polys += head(cx, cy - 150, 42)
    # two low side tails hanging past the shoulders
    polys += ribbon([(cx - 44, cy - 150), (cx - 60, cy - 56), (cx - 54, cy + 44)],
                    [18, 14, 6])
    polys += ribbon([(cx + 44, cy - 150), (cx + 60, cy - 56), (cx + 54, cy + 44)],
                    [18, 14, 6])
    # body + legs
    polys += dress_body(cx, cy - 116, cy + 12, cy + 152, 50, 62, 112)
    polys += limb([(cx - 22, cy + 152), (cx - 26, cy + 214), (cx - 28, cy + 256)],
                  [15, 12, 9])
    polys += limb([(cx + 22, cy + 152), (cx + 30, cy + 214), (cx + 36, cy + 256)],
                  [15, 12, 9])
    # arms to the grip
    polys += limb([(cx - 44, cy - 102), (cx - 14, cy - 94), (gx, gy)], [13, 11, 8])
    polys += limb([(cx + 44, cy - 102), (cx + 12, cy - 90), (gx + 6, gy - 6)],
                  [13, 11, 8])
    return polys


def draw(c: Canvas, u: float, i: int, t: float) -> None:
    # ---- Phase A: petal morphs to the boat; Komachi rises, scythe shouldered ----
    if i < A_END:
        bob = 6 * math.sin(i * 0.08)
        if i < 28:
            mt = ease(clamp01(i / 28.0), "in_out")
            hull = morph_polys(PETAL_BIG, BOAT, mt)
            c.polygon([(x, y + bob) for x, y in hull])
        else:
            c.polygon([(x, y + bob) for x, y in BOAT])
        if i >= 18:                                  # Komachi grows in, standing in the boat
            g = ease(clamp01((i - 18) / 14.0), "out")
            fig = komachi(CX, 360, pole_ang=0.6)
            fig = transform_polys(fig, scale=0.58 * g, origin=(CX, 360),
                                  translate=(0, 70 + bob))
            draw_polys(c, fig)
        return

    # ---- Phase B: push to a close-up; Komachi swings the scythe across her body ----
    if i < B_END:
        p = (i - A_END) / (B_END - A_END)
        s = lerp(0.8, 1.12, ease(clamp01(p / 0.5), "in_out"))
        sway = 8 * math.sin(i * 0.06)
        ang = lerp(0.7, -0.7, ease(clamp01((p - 0.2) / 0.62), "in_out"))   # swing across
        fig = komachi(CX + sway, 360, pole_ang=ang)
        draw_polys(c, cam(fig, s, CX, 360))
        return

    # ---- Phase C: the scythe blade wipes the frame into a black|white split ----
    p = clamp01((i - B_END) / (NFR - B_END))
    edge = lerp(WIDTH + 40, SEAM_X, ease(p, "in_out"))     # white front sweeps right->seam
    # white fills everything to the right of the leading edge
    if edge < WIDTH:
        c.rectangle(edge, 0, WIDTH, HEIGHT)
    # Komachi recedes on the (black) left during the first half of the wipe, then is gone
    if p < 0.6:
        fig = komachi(CX - 40, 360, pole_ang=-0.6)
        fig = transform_polys(fig, scale=lerp(0.8, 0.5, p), origin=(CX, 360),
                              translate=(lerp(0, -150, p), 0))
        draw_polys(c, fig)
        # cover anything that strayed past the leading edge with the white field again
        if edge < WIDTH:
            c.rectangle(edge, 0, WIDTH, HEIGHT)
    # the sweeping scythe blade rides the leading edge (a thin black crescent on white)
    if p < 0.96:
        ba = math.pi / 2
        outer = arc_pts(edge, 360, 300, ba - 1.1, ba + 1.1, 22)
        inner = arc_pts(edge - 26, 360, 280, ba + 1.1, ba - 1.1, 22)
        c.polygon(outer + inner, color=BLACK)


def arc_pts(cx, cy, r, a0, a1, n):
    return [(cx + r * math.cos(lerp(a0, a1, k / n)),
             cy + r * math.sin(lerp(a0, a1, k / n))) for k in range(n + 1)]


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw, bg=BLACK)
    print(f"Scene 10: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

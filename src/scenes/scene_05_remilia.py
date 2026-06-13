"""Scene 5 -- Remilia and the teacup.  Frames 1080-1274 (195 frames).

SCENES.md: Remilia appears (mob cap with ribbon, short hair) and spreads her
scalloped bat wings (f1111 at 0:37). Close-up profile: she holds a teacup out on
her hand (f1201 at 0:40) and lets it drop. Polarity B-on-W.

Continuity in (4->5): Scene 4 ended zoomed on Patchouli's raised, wagging index
finger (B-on-W). That finger -- the shared `raised_finger` handoff shape -- morphs
directly into Remilia: this scene opens on the same close-up finger, then zooms out
and grows the full figure under it, wings unfurling. Handoff out (5->6): the teacup
falls and SHATTERS; the shatter is the polarity inversion, so Scene 6 starts already
W-on-B with white shards. This scene ends B-on-W with the dropped `teacup` falling.

Remilia is built inline from the shared toolkit; her identifying silhouette features
are the mob cap (with a ribbon nub) over short hair and the scalloped `bat_wing`s.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: F401,F403
from shapes import (  # noqa: E402
    head, dress_body, mob_cap, limb, ellipse_poly, bat_wing, teacup,
    raised_finger, draw_polys, transform_polys,
)

SCENE_START_FRAME = 1080
SCENE_END_FRAME = 1275
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / FPS  # 6.5 s
NFR = SCENE_END_FRAME - SCENE_START_FRAME                      # 195

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

CX = 480


def remilia_front(cx, wing_t=1.0, arm_t=0.0):
    """Front-facing Remilia: short hair, mob cap + ribbon, scalloped bat wings.

    *wing_t* grows the wings as they spread; *arm_t* raises the right hand toward
    the face (used only for the opening morph from the raised finger).
    """
    polys = []
    # bat wings behind the body, rooted near the shoulders
    polys += bat_wing(cx - 46, 252, span=178, side=-1, t=wing_t)
    polys += bat_wing(cx + 46, 252, span=178, side=1, t=wing_t)
    # short hair mass + head
    polys += ellipse_poly(cx, 180, 56, 54)
    polys += head(cx, 172, 45)
    # mob cap + a small ribbon nub on the brim
    polys += mob_cap(cx, 150, 70, 44)
    polys += [[(cx - 58, 150), (cx - 38, 142), (cx - 40, 162)]]   # ribbon
    # body: knee-length dress (Remilia is small -> shorter hem)
    polys += dress_body(cx, 208, 338, 588, 54, 70, 128)
    # left arm relaxed at side
    polys += limb([(cx - 50, 222), (cx - 84, 300), (cx - 90, 372)], [12, 10, 7])
    # right arm: lerp between raised-to-face (arm_t=1) and relaxed (arm_t=0)
    j1 = (cx + 50, 222)
    mid = (lerp(cx + 84, cx + 56, arm_t), lerp(300, 196, arm_t))
    end = (lerp(cx + 90, cx + 54, arm_t), lerp(372, 138, arm_t))
    polys += limb([j1, mid, end], [12, 10, 7])
    return polys


def remilia_profile(cx, extend=1.0, head_y=176):
    """Profile Remilia facing LEFT, left arm extended out to hold the teacup.

    *extend* in [0,1] reaches the arm further out (and the palm is where the
    teacup sits). Wings are folded behind (small) in the close-up.
    """
    polys = []
    # folded wing peeking behind the back (right side)
    polys += bat_wing(cx + 30, 250, span=96, side=1, t=1.0)
    # head (facing left): hair bun at back-right, face profile to the left
    polys += ellipse_poly(cx + 18, head_y + 2, 50, 50)            # back hair
    polys += head(cx - 8, head_y, 44)
    polys += mob_cap(cx + 2, head_y - 24, 64, 42)
    polys += [[(cx + 50, head_y - 22), (cx + 70, head_y - 30), (cx + 62, head_y - 6)]]  # ribbon back
    # narrower (profile) body
    polys += dress_body(cx + 6, 212, 336, 584, 44, 60, 104)
    # extended left arm holding the cup out in front (to the left)
    handx = lerp(cx - 70, cx - 150, extend)
    handy = lerp(250, 250, extend)
    polys += limb([(cx - 16, 226), (cx - 90, 244), (handx, handy)], [13, 11, 8])
    return polys


def _hsquash(polys, cx, k):
    """Scale a poly-list horizontally about x=cx by factor k (the project's
    'turn-around' idiom: squash to edge-on, then expand into the new facing)."""
    return [[(cx + (x - cx) * k, y) for x, y in p] for p in polys]


def draw(c: Canvas, u: float, i: int, t: float) -> None:
    # ------------------------------------------------------------------ #
    # Phase A (i<30): the raised finger (Scene 4 handoff) morphs into Remilia.
    # Open as a zoomed close-up on the raised hand+finger (echoing Scene 4's
    # last frame), then zoom out while the body grows in and wings unfurl.
    # ------------------------------------------------------------------ #
    if i < 30:
        a = ease(i / 30.0, "out")
        zoom = lerp(2.0, 1.0, a)
        wing_t = ease(clamp01((i - 8) / 22.0), "out")
        arm_t = 1.0 - a                      # right hand starts up by the face
        fig = remilia_front(CX, wing_t=wing_t, arm_t=arm_t)
        fig = transform_polys(fig, scale=zoom, origin=(CX + 10, 180))
        fig = transform_polys(fig, translate=(0, lerp(20, 0, a)))
        draw_polys(c, fig)
        if i < 14:                            # the incoming finger, fading into the hand
            fade = 1.0 - i / 14.0
            fin = raised_finger(CX + 54, 142, length=72 + 26 * fade, w=18)
            fin = transform_polys(fin, scale=zoom, origin=(CX + 10, 180))
            fin = transform_polys(fin, translate=(0, lerp(20, 0, a)))
            draw_polys(c, fin)
        return

    # ------------------------------------------------------------------ #
    # Phase B (30<=i<110): front, wings fully spread, gentle sway (f1111).
    # ------------------------------------------------------------------ #
    if i < 110:
        sway = 14 * math.sin(2 * math.pi * (i - 30) / 70)
        rot = 0.035 * math.sin(2 * math.pi * (i - 30) / 70)
        flap = 0.92 + 0.08 * math.cos(2 * math.pi * (i - 30) / 35)
        fig = remilia_front(CX, wing_t=flap, arm_t=0.0)
        fig = transform_polys(fig, rotate=rot, origin=(CX, 360))
        fig = transform_polys(fig, translate=(sway, 0))
        draw_polys(c, fig)
        return

    # ------------------------------------------------------------------ #
    # Phase C (110<=i<128): turn front -> left profile via a horizontal squash
    # through edge-on (no pop), zooming into the close-up.
    # ------------------------------------------------------------------ #
    if i < 128:
        if i < 119:
            a = ease((i - 110) / 9.0, "in")
            k = lerp(1.0, 0.12, a)
            zoom = lerp(1.0, 1.18, a)
            fig = remilia_front(CX, wing_t=lerp(1.0, 0.5, a), arm_t=0.0)
        else:
            a = ease((i - 119) / 9.0, "out")
            k = lerp(0.12, 1.0, a)
            zoom = lerp(1.18, 1.35, a)
            fig = remilia_profile(CX, extend=0.0)
        fig = _hsquash(fig, CX, k)
        fig = transform_polys(fig, scale=zoom, origin=(CX, 300))
        draw_polys(c, fig)
        return

    # ------------------------------------------------------------------ #
    # Phase D (128<=i): profile close-up holding the teacup out (f1201), then
    # she lets it drop -- the cup falls (shatter+flip is owned by Scene 6, which
    # opens W-on-B with the shards). Keep the cup on-screen at the last frame.
    # ------------------------------------------------------------------ #
    zoom = 1.35
    reach = ease(clamp01((i - 128) / 24.0), "out")
    fig = remilia_profile(CX, extend=reach)
    fig = transform_polys(fig, scale=zoom, origin=(CX, 300))
    draw_polys(c, fig)

    palm = (lerp(CX - 70, CX - 150, reach), 250)
    if i < 168:
        cup = teacup(palm[0], palm[1] - 18, w=34)
        cup = transform_polys(cup, scale=zoom, origin=(CX, 300))
        draw_polys(c, cup)
    else:
        d = (i - 168) / 27.0
        fall = 300 * ease(clamp01(d), "in")          # accelerating, stays on-screen
        tumble = 2.0 * d
        cup = teacup(palm[0], palm[1] - 18, w=34)
        cup = transform_polys(cup, rotate=tumble, origin=(palm[0], palm[1] - 18))
        cup = transform_polys(cup, translate=(-14 * d, fall))
        cup = transform_polys(cup, scale=zoom, origin=(CX, 300))
        draw_polys(c, cup)


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw)
    print(f"Scene 5: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

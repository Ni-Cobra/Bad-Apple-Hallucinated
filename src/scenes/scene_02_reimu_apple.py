"""Scene 2 -- Reimu's intro dance with the apple.  Frames 120-449 (330 frames).

SCENES.md: Reimu sways/dances to the beat holding an apple. ~f241 close-up
profile, she raises the apple to her mouth as if to bite it; decides not to,
winds up (motion-blur spin ~f361) and TOSSES the apple high into the sky
(apple alone airborne by ~f436). Polarity B-on-W throughout. The 2->3 polarity
flip happens at the catch, so this scene stays B-on-W and ENDS with the airborne
apple (black on white); Scene 3 starts already inverted with Marisa catching it.

Continuity in (1->2): Scene 1 ended on the full back-view figure (reimu_back);
this scene opens on that back view, sways, then turns around to the front to
dance. Handoff out (2->3): the shared `apple` shape is left airborne near the
top of the frame at (540, 140) for Scene 3 to catch.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: F401,F403
from shapes import (  # noqa: E402
    reimu_back, reimu_front, apple, draw_polys, transform_polys, lerp_polys,
)

SCENE_START_FRAME = 120
SCENE_END_FRAME = 450
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / FPS  # 11.0 s
NFR = SCENE_END_FRAME - SCENE_START_FRAME                      # 330

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

CX = 480

# Apple-holding hand positions (screen-left hand of reimu_front):
HAND_NEUTRAL = (CX - 96, 388)   # arm down, apple at side
HAND_BITE = (CX - 40, 248)      # raised near the mouth
HAND_WIND = (CX - 150, 210)     # flung back during the wind-up
RELEASE_END = (540, 140)        # airborne handoff point for Scene 3


def squash_x(polys, cx, sx):
    """Horizontally scale polys about x=cx (used for the back->front turn)."""
    return [[(cx + (x - cx) * sx, y) for x, y in p] for p in polys]


def draw(c: Canvas, u: float, i: int, t: float) -> None:
    # ------------------------------------------------------------------ #
    # Phase A (i<40): back view continues from Scene 1, gentle sway.
    # ------------------------------------------------------------------ #
    if i < 40:
        sway = 10 * math.sin(2 * math.pi * i / 60)
        fig = transform_polys(reimu_back(), translate=(sway, 0))
        draw_polys(c, fig)
        return

    # ------------------------------------------------------------------ #
    # Phase B (40<=i<80): turn around -- squash the back to a sliver, then
    # grow the front out of the sliver.
    # ------------------------------------------------------------------ #
    if i < 80:
        tu = (i - 40) / 40.0
        if tu < 0.5:
            sx = 1.0 - 2.0 * tu
            draw_polys(c, squash_x(reimu_back(), CX, max(sx, 0.001)))
        else:
            sx = 2.0 * tu - 1.0
            draw_polys(c, squash_x(reimu_front(pose="neutral"), CX, max(sx, 0.001)))
        return

    # ------------------------------------------------------------------ #
    # Front-facing phases. Compute pose blend + apple position per phase.
    # ------------------------------------------------------------------ #
    bite_t = 0.0
    wind_t = 0.0
    apple_pos = None
    sway = 0.0
    rot = 0.0
    body_dy = 0.0
    draw_figure = True

    if i < 175:
        # Phase C: dance + near-bite. Bite peaks ~i=122 (f242).
        sway = 24 * math.sin(2 * math.pi * (i - 80) / 70)
        rot = 0.04 * math.sin(2 * math.pi * (i - 80) / 70)
        if 95 <= i <= 150:
            bite_t = math.sin(math.pi * (i - 95) / 55.0)
        hx = lerp(HAND_NEUTRAL[0], HAND_BITE[0], bite_t) + sway
        hy = lerp(HAND_NEUTRAL[1], HAND_BITE[1], bite_t)
        apple_pos = (hx, hy)

    elif i < 255:
        # Phase D: wind-up (fast spin-blur feel), apple flung back.
        wind_t = ease((i - 175) / 80.0, "in")
        spin = ease(clamp01((i - 205) / 50.0), "in")
        sway = 18 * math.sin(2 * math.pi * (i - 175) / 24)
        rot = (0.05 + 0.30 * spin) * math.sin(2 * math.pi * (i - 175) / 16)
        hx = lerp(HAND_NEUTRAL[0], HAND_WIND[0], wind_t) + sway
        hy = lerp(HAND_NEUTRAL[1], HAND_WIND[1], wind_t)
        apple_pos = (hx, hy)

    elif i < 312:
        # Phase E: release. Apple launches up across the frame; Reimu follows
        # through and the camera tilts up (figure slides off the bottom).
        rel = ease((i - 255) / 57.0, "out")
        wind_t = max(0.0, 1.0 - (i - 255) / 30.0)   # arms swing forward again
        body_dy = 560 * ease(clamp01((i - 262) / 50.0), "in")
        if body_dy > 730:
            draw_figure = False
        ax = lerp(HAND_WIND[0], RELEASE_END[0], rel)
        # a little upward arc overshoot then settle toward the handoff height
        ay = lerp(HAND_WIND[1], RELEASE_END[1], rel) - 60 * math.sin(math.pi * rel)
        apple_pos = (ax, ay)

    else:
        # Phase F (i>=312): apple alone, airborne, drifting to the handoff spot.
        draw_figure = False
        rel = ease((i - 312) / 18.0, "out")
        ax = lerp(RELEASE_END[0] - 6, RELEASE_END[0], rel)
        ay = lerp(RELEASE_END[1] + 18, RELEASE_END[1], rel)
        apple_pos = (ax, ay)

    if draw_figure:
        if bite_t > 0.0:
            fig = lerp_polys(reimu_front(pose="neutral"), reimu_front(pose="apple"), bite_t)
        elif wind_t > 0.0:
            fig = lerp_polys(reimu_front(pose="neutral"), reimu_front(pose="wind"), wind_t)
        else:
            fig = reimu_front(pose="neutral")
        fig = transform_polys(fig, rotate=rot, origin=(CX, 360))
        fig = transform_polys(fig, translate=(sway, body_dy))
        draw_polys(c, fig)

    if apple_pos is not None:
        draw_polys(c, apple(apple_pos[0], apple_pos[1], r=30))


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw)
    print(f"Scene 2: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

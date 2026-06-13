"""Scene 4 -- Patchouli's dance (VERSE 1 begins).  Frames 855-1079 (225 frames).

SCENES.md: the apple core transforms into Patchouli (vocals begin). She dances in
place with flowing hand gestures (full body f871; mob cap + extended arm f961).
The passage ends on a close-up of her profile with one index finger raised,
wagging (f1051). Polarity B-on-W (flips back from Scene 3 at the morph).

Continuity in (3->4): Scene 3 left the shared `apple_core` at (480,430) (white on
black); the flip lands here so the core is now black on white and grows into
Patchouli. Handoff out (4->5): ends zoomed on the raised, wagging index finger,
which Scene 5 morphs into Remilia (that micro-handoff shape is authored with the
scene-5 pair per shapes.py's note).

Patchouli is built inline from the shared figure toolkit (mob cap + long hair +
robe); her identifying silhouette feature is the mob/night cap over long hair.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: F401,F403
from shapes import (  # noqa: E402
    apple_core, head, dress_body, mob_cap, long_hair, limb,
    draw_polys, transform_polys, lerp_polys,
)

SCENE_START_FRAME = 855
SCENE_END_FRAME = 1080
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / FPS  # 7.5 s
NFR = SCENE_END_FRAME - SCENE_START_FRAME                      # 225

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

CX = 480
CORE_REST = (480, 430)          # where Scene 3 left the apple core


def patchouli(cx, mode="neutral"):
    """Patchouli silhouette; all modes share structure so they can be lerped.

    mode in {'neutral','arm_out','finger'} only changes the two arm limbs.
    """
    polys = []
    polys += long_hair(cx, 156, 64, 322)
    polys += dress_body(cx, 214, 360, 632, 60, 82, 150)
    polys += head(cx, 174, 46)
    polys += mob_cap(cx, 150, 78, 48)
    if mode == "arm_out":
        left = [(cx - 58, 234), (cx - 96, 318), (cx - 92, 398)]
        right = [(cx + 58, 234), (cx + 122, 300), (cx + 178, 296)]
    elif mode == "finger":
        # right arm raised, hand by the face, finger up (handoff to Remilia)
        left = [(cx - 58, 234), (cx - 90, 312), (cx - 70, 250)]
        right = [(cx + 50, 232), (cx + 70, 176), (cx + 80, 120)]
    else:  # neutral
        left = [(cx - 58, 234), (cx - 88, 320), (cx - 86, 400)]
        right = [(cx + 58, 234), (cx + 88, 320), (cx + 86, 400)]
    polys += limb(left, [14, 11, 8])
    polys += limb(right, [14, 11, 8])
    return polys


def draw(c: Canvas, u: float, i: int, t: float) -> None:
    # ------------------------------------------------------------------ #
    # Phase A (i<36): core morphs/grows into Patchouli.
    # ------------------------------------------------------------------ #
    if i < 36:
        g = ease(i / 36.0, "out")
        sc = lerp(0.14, 1.0, g)
        fig = transform_polys(patchouli(CX, "neutral"), scale=sc, origin=(CX, 412))
        draw_polys(c, fig)
        if i < 20:
            cs = 1.0 - i / 20.0
            draw_polys(c, transform_polys(apple_core(*CORE_REST, r=24),
                                          scale=max(cs, 0.05), origin=CORE_REST))
        return

    # ------------------------------------------------------------------ #
    # Phase B (36<=i<150): dance, extended-arm gesture peaking ~i=106 (f961).
    # ------------------------------------------------------------------ #
    if i < 150:
        sway = 16 * math.sin(2 * math.pi * (i - 36) / 80)
        rot = 0.05 * math.sin(2 * math.pi * (i - 36) / 80)
        arm_t = math.sin(math.pi * clamp01((i - 40) / 120.0))
        fig = lerp_polys(patchouli(CX, "neutral"), patchouli(CX, "arm_out"), arm_t)
        fig = transform_polys(fig, rotate=rot, origin=(CX, 360))
        fig = transform_polys(fig, translate=(sway, 0))
        draw_polys(c, fig)
        return

    # ------------------------------------------------------------------ #
    # Phase C (i>=150): raise index finger, zoom to the upper-body close-up,
    # finger wags. Ends as the scene-5 handoff.
    # ------------------------------------------------------------------ #
    finger_t = ease(clamp01((i - 150) / 25.0), "out")
    fig = lerp_polys(patchouli(CX, "neutral"), patchouli(CX, "finger"), finger_t)
    # zoom in on the raised hand/face
    zoom = lerp(1.0, 1.55, finger_t)
    fig = transform_polys(fig, scale=zoom, origin=(CX + 30, 210))
    fig = transform_polys(fig, translate=(0, 40 * finger_t))
    draw_polys(c, fig)

    if finger_t > 0.4:
        # the wagging finger tip (the handoff nub). Build it in figure space,
        # then apply the SAME zoom+translate the figure got.
        wag = 14 * math.sin(2 * math.pi * (i - 150) / 18)
        ftx = CX + 80 + wag      # finger top x (matches the 'finger' arm end)
        nub = [[(ftx - 9, 134), (ftx + 9, 134), (ftx + 5, 96), (ftx - 5, 96)]]
        nub = transform_polys(nub, scale=zoom, origin=(CX + 30, 210))
        nub = transform_polys(nub, translate=(0, 40 * finger_t))
        draw_polys(c, nub)


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw)
    print(f"Scene 4: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

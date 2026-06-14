"""Scene 15 -- Kaguya and the moon; whiteout (f3150-3363, 213 frames).

Mirror of Scene 14. W-on-B that ends in a full-frame WHITEOUT on the chorus-1
"turn white" lyric. Opens on Scene 14's exact handoff: the glowing moon at the
TOP-RIGHT (820,218) r146 on black. Kaguya enters from the LEFT, back turned,
very long straight hair (ref f3166 ~local 15), reaching up toward the moon. The
camera pushes in and -- via the project's horizontal-squash turn idiom -- swings
her to a profile CLOSE-UP (huge hair mass, ref f3241 ~local 90). On the final
line the view washes to PURE WHITE (ref f3331 ~local 180), held to the end.

15->16 handoff: the last frame is a solid-white field -- Scene 16 (Prismriver)
opens B-on-W with its trio fading in on exactly this white stage.

Kaguya built inline (rounded back-of-head + floor-length straight hair = her
identifying silhouette). The moon glow uses the same ring formula as Scene 14 so
the 14->15 boundary matches.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: E402,F403
from shapes import circle_poly, ellipse_poly, ribbon, draw_polys  # noqa: E402

SCENE_START_FRAME = 3150
SCENE_END_FRAME = 3363
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / 30.0   # 7.1 s

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

WHITE_START = 150     # whiteout begins growing
WHITE_FULL = 181      # pure white reached (~ref f3331 at local 180)


# ---------------------------------------------------------------------------
# Moon glow (identical ring formula to Scene 14 -> matching 14->15 boundary)
# ---------------------------------------------------------------------------

def draw_moon(c, cx, cy, r):
    rings = 8
    for k in range(rings, 0, -1):
        f = k / rings
        rad = r * (1.0 + 0.85 * f)
        gray = int(210 * (1.0 - f) ** 1.6)
        if gray > 0:
            c.circle(cx, cy, rad, color=gray)
    c.circle(cx, cy, r, color=WHITE)


# ---------------------------------------------------------------------------
# Kaguya (inline) -- canonical: centred x=480, head anchor (480,150)
# ---------------------------------------------------------------------------

def kaguya_back(arm_t=0.0):
    """Back view: rounded head, very long straight hair, narrow gown. *arm_t*
    raises her right arm up toward the moon (top-right)."""
    polys = []
    polys += ellipse_poly(480, 150, 50, 56)                       # back of head
    polys.append([                                                # long straight hair
        (480 - 58, 168), (480 + 58, 168),
        (480 + 66, 360), (480 + 56, 520), (480 + 40, 650),
        (480 - 40, 650), (480 - 56, 520), (480 - 66, 360)])
    polys.append([(480 - 46, 470), (480 + 46, 470),               # gown lower body
                  (480 + 58, 700), (480 - 58, 700)])
    if arm_t > 0.01:                                              # reaching arm up-right
        hx = lerp(480 + 50, 480 + 160, arm_t)
        hy = lerp(300, 150, arm_t)
        polys += ribbon([(480 + 38, 258), ((480 + 38 + hx) / 2, (258 + hy) / 2),
                         (hx, hy)], [16, 12, 7])
    return polys


def kaguya_profile():
    """Profile close-up facing LEFT, with the huge straight-hair mass on the
    right/back and a gentle reaching arm forward (ref f3241)."""
    polys = []
    polys.append([                                                # huge long hair mass
        (470, 116), (548, 140), (568, 300), (552, 470), (516, 632),
        (468, 690), (452, 560), (452, 360), (450, 208)])
    polys += ellipse_poly(486, 150, 46, 53)                       # skull
    polys.append([(452, 118), (438, 166), (428, 150), (446, 116)])  # bangs/fringe forward
    polys.append([(440, 158), (422, 176), (440, 190), (454, 182)])  # nose/chin hint
    polys.append([(458, 205), (520, 205), (544, 340), (440, 340)])  # shoulder/upper body
    polys += ribbon([(472, 252), (418, 246), (366, 230)], [15, 11, 7])  # arm forward
    return polys


def place(polys, cam, hx, hy, sqz=1.0):
    """Scale about the canonical head anchor (480,150) by *cam* (uniform) and an
    extra horizontal *sqz* (the turn squash), then anchor the head at (hx,hy)."""
    out = []
    for p in polys:
        out.append([((x - 480) * cam * sqz + hx, (y - 150) * cam + hy)
                    for x, y in p])
    return out


# ---------------------------------------------------------------------------
# Camera / composition
# ---------------------------------------------------------------------------

def cam_state(i):
    """Return (cam, head_x, head_y, turn) for frame i."""
    if i < 18:                                   # Kaguya slides in from off the left
        s = ease(i / 18.0, "out")
        return 0.9, lerp(-40.0, 300.0, s), 150.0, 0.0
    if i < 74:                                   # slow push-in, back view
        u = ease((i - 16) / 58.0, "in_out")
        return lerp(0.9, 1.06, u), lerp(300.0, 338.0, u), 150.0, 0.0
    if i < 90:                                   # turn (h-squash) + push to close-up
        u = ease((i - 74) / 16.0, "in_out")
        return lerp(1.06, 1.9, u), lerp(338.0, 432.0, u), lerp(150.0, 236.0, u), u
    return 1.9, 432.0, 236.0, 1.0                # held profile close-up


def moon_state(i):
    """Return (cx, cy, r); the moon drifts toward the top-right corner and exits."""
    if i < 74:
        return 820.0 + i * 0.7, 212.0 - i * 0.25, 146.0
    u = ease(clamp01((i - 74) / 36.0), "in_out")
    return lerp(872.0, 1140.0, u), lerp(193.0, 96.0, u), 146.0


def draw(c, u, i, t):
    if i >= WHITE_FULL:                          # held pure white to the end
        c.fill(WHITE)
        return

    mx, my, mr = moon_state(i)
    draw_moon(c, mx, my, mr)

    cam, hx, hy, turn = cam_state(i)
    sb = max(0.0, 1.0 - 2.0 * turn)              # back-view x-extent
    sp = max(0.0, 2.0 * turn - 1.0)              # profile x-extent
    if sb > 0.001:
        arm_t = ease(clamp01((i - 35) / 37.0), "in_out")
        draw_polys(c, place(kaguya_back(arm_t), cam, hx, hy, sb))
    if sp > 0.001:
        draw_polys(c, place(kaguya_profile(), cam, hx, hy, sp))

    if i >= WHITE_START:                         # the whiteout grows to fill
        wt = ease((i - WHITE_START) / (WHITE_FULL - WHITE_START), "in")
        c.circle(480, 360, lerp(0.0, 720.0, wt), color=WHITE)


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw, bg=BLACK)
    print(f"Scene 15: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

"""Scene 30 -- Elly takes the scythe (f5610-5850, 240 fr).
W-on-B  (brief mixed-polarity morph ~f5836).  The PC-98 era enters.

29->30: opens on Scene 29's closed-parasol shaft extended to the right (the
HANDOFF_* geometry). In a close-up Elly's hand reaches in from the RIGHT and
grasps it (ref f5641); the parasol becomes a scythe. Elly bends forward over it
(ref f5686), then poses in profile -- bonnet hat with ribbon, long curved blade
sweeping the frame (ref f5761). She is a WHITE silhouette. Near the end the
camera slides down the scythe to its blade tip with a brief polarity morph
(ref f5836).

30->31: ends on the downward-pointing blade tip (BLADE_TIP) with a drop starting
to gather -- Scene 31 (object scene) continues from there.

Elly built inline; the scythe is the shared scythe() prop.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: E402,F403
from shapes import (  # noqa: E402
    head, ellipse_poly, circle_poly, ribbon, arc_points, draw_polys,
    transform_polys, scythe, blade_tip,
)

SCENE_START_FRAME = 5610
SCENE_END_FRAME = 5850
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / 30.0   # 8.0 s

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

# --- timeline (local frames) -------------------------------------------------
GRASP_END = 44      # close-up: Elly's hand grasps the shaft from the right (f5641)
BEND_END = 88       # Elly bends forward over the scythe (f5686 ~ local 76)
POSE_END = 158      # Elly profile pose, blade sweeping (f5761 ~ local 151)
HOLD_END = 210      # hold the pose
# 210..239 -> camera slides down to the blade tip; mixed-polarity morph (f5836)

# 30->31 handoff: the downward blade tip the camera ends on (shared blade_tip()).
BLADE_TIP = (500.0, 268.0)


def cam(polys, scale, focus):
    """Zoom by *scale* about world point *focus*, mapping it to screen centre."""
    return transform_polys(polys, scale=scale, origin=focus,
                           translate=(480.0 - focus[0], 360.0 - focus[1]))


# ---------------------------------------------------------------------------
def grasp_handoff(g):
    """Close-up of the shaft hand-off (ref f5641): the horizontal parasol shaft,
    Yuka's forearm holding it from the left, Elly's hand/forearm reaching in from
    the right to grasp it (the parasol's hook curl hangs at the join).
    g in [0,1] slides Elly's grasping hand in and Yuka's arm out."""
    polys = []
    grip = (470.0, 360.0)
    polys += ribbon([(grip[0] - 230, 360.0), (grip[0] + 150, 360.0)], 16)   # shaft
    # parasol hook curl hanging under the join
    hook = arc_points(grip[0] + 78, 388.0, 22, -0.4, math.pi + 0.2, 14)
    polys += ribbon(hook, 11)
    # Yuka's forearm from the LEFT, retracting as g->1
    yx = lerp(-60.0, -200.0, g)
    polys += ribbon([(yx, 360.0), (grip[0] - 150, 358.0), (grip[0] - 36, 360.0)], [70, 40, 26])
    # Elly's forearm + grasping hand entering from the RIGHT
    ex = lerp(1060.0, grip[0] + 70, g)
    polys += ribbon([(ex + 220, 372.0), (ex + 60, 364.0), (grip[0] + 16, 360.0)], [66, 40, 24])
    palm = (grip[0] + 4, 360.0)
    for k in range(4):                                  # fingers curling over the shaft
        fa = -1.9 - 0.34 * k
        polys += ribbon([(palm[0] + 18 - 8 * k, 372.0),
                         (palm[0] + 10 - 8 * k + 22 * math.cos(fa),
                          372.0 + 22 * math.sin(fa))], [11, 7])
    # Elly's head entering top-right (g->1)
    hx = lerp(1120.0, 880.0, g)
    polys += ellipse_poly(hx, 150.0, 70, 60)
    return polys


def elly(cx, foot_y, scale=1.0, lean=0.0, bend=0.0):
    """Elly in profile facing RIGHT: a wide bonnet hat with a back ribbon bow,
    short hair, dress.  *bend* (0..1) pitches her forward over the scythe; *lean*
    tilts the upright pose."""
    R = 42.0
    Hy = foot_y - 296
    Hx = cx + 18
    neck_y = Hy + R * 0.9
    shoulder = (cx + 6, neck_y + 26)
    waist = (cx, foot_y - 150)
    polys = []
    # back ribbon bow on the bonnet
    polys.append([(Hx - 58, Hy - 30), (Hx - 96, Hy - 54), (Hx - 92, Hy - 8),
                  (Hx - 58, Hy + 4)])
    polys.append([(Hx - 58, Hy - 18), (Hx - 96, Hy + 4), (Hx - 92, Hy + 40),
                  (Hx - 58, Hy + 18)])
    # bonnet: rounded crown + wide brim sweeping forward over the face
    polys += ellipse_poly(Hx - 6, Hy - 10, 52, 40)
    polys.append([(Hx - 56, Hy + 2), (Hx + 70, Hy - 16), (Hx + 86, Hy + 4),
                  (Hx + 40, Hy + 20), (Hx - 48, Hy + 22)])
    polys += head(Hx, Hy, R)
    polys.append([(Hx + R * 0.82, Hy + 2), (Hx + R * 1.18, Hy + 12),
                  (Hx + R * 0.8, Hy + 20)])             # nose (faces right)
    # short hair tuft at the nape
    polys.append([(Hx - R * 0.7, Hy + 8), (Hx - R * 1.0, Hy + 40),
                  (Hx - R * 0.4, Hy + 44), (Hx - R * 0.2, Hy + 16)])
    polys.append([(Hx - 12, neck_y - 8), (Hx + 14, neck_y - 8),
                  (shoulder[0] + 14, shoulder[1]), (shoulder[0] - 16, shoulder[1])])  # neck
    # torso + flaring dress to the floor
    polys.append([(shoulder[0] + 22, shoulder[1] - 2), (shoulder[0] - 30, shoulder[1]),
                  (waist[0] - 26, waist[1]), (waist[0] - 70, foot_y),
                  (waist[0] + 84, foot_y), (waist[0] + 34, waist[1])])
    out = polys
    if bend:
        out = transform_polys(out, rotate=bend * 0.85, origin=(shoulder[0], shoulder[1]))
    elif lean:
        out = transform_polys(out, rotate=lean, origin=(cx, foot_y))
    if scale != 1.0:
        out = transform_polys(out, scale=scale, origin=(cx, foot_y))
    return out, (shoulder[0], shoulder[1] + 4)


def elly_arms(shoulder, grip):
    """Both arms reaching from the shoulders down to the scythe grip."""
    polys = []
    polys += ribbon([(shoulder[0] + 6, shoulder[1]),
                     ((shoulder[0] + grip[0]) / 2 + 14, (shoulder[1] + grip[1]) / 2 + 8),
                     (grip[0] + 8, grip[1])], [20, 15, 10])
    polys += ribbon([(shoulder[0] - 8, shoulder[1] + 6),
                     ((shoulder[0] + grip[0]) / 2 - 6, (shoulder[1] + grip[1]) / 2 + 18),
                     (grip[0] - 14, grip[1] + 6)], [18, 13, 9])
    return polys


def pose_scythe(t=1.0):
    """Elly's scythe in the pose: blade crescent low-right (tip pointing down for
    the Scene-31 hand-off), long snath sweeping up through her grip.  t grows the
    blade in as the parasol becomes a scythe."""
    pivot = (632.0, 556.0)
    polys = scythe(pivot[0], pivot[1], length=330, angle=math.radians(216),
                   blade=int(205 * t) + 8, thick=10)
    return polys, pivot


def draw(c, u, i, t):
    c.fill(BLACK)

    # ---- Beat 1: close-up shaft hand-off, Elly grasps from the right --------
    if i < GRASP_END:
        g = ease(i / float(GRASP_END), "in_out")
        draw_polys(c, grasp_handoff(g), color=WHITE)
        return

    # grip point where Elly holds the scythe in the standing pose
    GRIP = (468.0, 416.0)

    # ---- Beat 2: Elly bends forward over the scythe (f5686) -----------------
    if i < BEND_END:
        b = ease((i - GRASP_END) / float(BEND_END - GRASP_END), "in_out")
        sc, _ = pose_scythe(t=b)
        body, sh = elly(404, 660, scale=1.0, bend=lerp(0.95, 0.62, b))
        polys = sc + body + elly_arms(sh, GRIP)
        draw_polys(c, cam(polys, scale=lerp(1.18, 1.06, b), focus=(470, 470)), color=WHITE)
        return

    # ---- Beat 3: Elly straightens into the profile pose (f5761) -------------
    if i < POSE_END:
        p = ease((i - BEND_END) / float(POSE_END - BEND_END), "in_out")
        sc, _ = pose_scythe(t=1.0)
        body, sh = elly(404, 660, scale=1.0, bend=lerp(0.62, 0.0, p))
        polys = sc + body + elly_arms(sh, GRIP)
        draw_polys(c, cam(polys, scale=lerp(1.12, 1.34, p), focus=(452, 452)), color=WHITE)
        return

    # ---- Beat 4: hold the pose ----------------------------------------------
    if i < HOLD_END:
        sc, _ = pose_scythe(t=1.0)
        body, sh = elly(404, 660, scale=1.0)
        polys = sc + body + elly_arms(sh, GRIP)
        draw_polys(c, cam(polys, scale=1.34, focus=(452, 452)), color=WHITE)
        return

    # ---- Beat 5: slide the camera down the blade; polarity morph; blade tip --
    s = (i - HOLD_END) / float(SCENE_END_FRAME - SCENE_START_FRAME - HOLD_END)  # 0..1

    if s < 0.55:
        # slide/zoom DOWN the scythe toward the blade pivot, then invert for the
        # brief black-on-white morph (ref f5836 ~ s=0.53)
        es = ease(s / 0.55, "in")
        sc, pivot = pose_scythe(t=1.0)
        body, sh = elly(404, 660, scale=1.0)
        polys = sc + body + elly_arms(sh, GRIP)
        focus = (lerp(452, pivot[0] - 10, es), lerp(452, pivot[1] - 6, es))
        draw_polys(c, cam(polys, scale=lerp(1.34, 2.9, es), focus=focus), color=WHITE)
        if s > 0.30:
            c.invert()
        return

    # s in [0.55,1]: resolved to the clean downward blade tip + gathering drop
    draw_polys(c, blade_tip(BLADE_TIP), color=WHITE)
    dg = clamp01((s - 0.62) / 0.38)               # the drop swells at the tip
    if dg > 0:
        c.circle(BLADE_TIP[0] - 4, BLADE_TIP[1] + 14 + 10 * dg, 6 + 7 * dg, color=WHITE)


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw, bg=BLACK)   # W-on-B
    print(f"Scene 30: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

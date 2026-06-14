"""Scene 29 -- Petals and Yuka's parasol (f5430-5610, 180 fr).
W-on-B.  FINAL CHORUS, key change up (documented sync point).

28->29: opens on Scene 28's settled white spray plume on black -- the shared
SPLASH_FIELD droplets (continuous; Scene 28 already flipped to W-on-B at the
dive). On the key change the droplets morph into a STORM of swirling flower
petals filling the black frame (ref f5476). Among them Yuka stands in profile
facing right under her big OPEN parasol (ref f5551 -- one of the video's most
elegant stills). She then CLOSES the parasol and EXTENDS it out to her side.

29->30: the closed parasol is now a horizontal scythe shaft extended to the
right; Scene 30 has Elly's hand reach in from the right and take it. The handoff
shaft geometry is the HANDOFF_* constants below (Scene 30 reproduces them).

Yuka built inline; SPLASH_FIELD + sakura_petal are the shared handoff shapes.
"""

import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets"))
from renderlib import *  # noqa: E402,F403
from shapes import (  # noqa: E402
    SPLASH_FIELD, sakura_petal, head, ribbon, arc_points, draw_polys,
)

SCENE_START_FRAME = 5430
SCENE_END_FRAME = 5610
SCENE_DURATION = (SCENE_END_FRAME - SCENE_START_FRAME) / 30.0   # 6.0 s

FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frames")

# --- timeline (local frames) -------------------------------------------------
FORM_END = 46       # droplets -> swirling petal field fills the frame (ref f5476)
RISE_0, RISE_1 = 54, 92      # Yuka rises in AFTER the clean petal-field beat
HOLD_END = 122      # open-parasol still held (ref f5551 ~ local 121)
# 122..179 -> closes the parasol + extends it out to her side (handoff)

# --- 29->30 handoff: the closed parasol as a horizontal shaft to the right ----
HANDOFF_GRIP = (360.0, 442.0)       # Yuka's grip on the shaft, at the very end
HANDOFF_ANG = 0.0                   # shaft points straight right
HANDOFF_LUP = 205.0                 # grip -> furled tip (right end)
HANDOFF_LDN = 78.0                  # grip -> handle end (left)
# => tip (565,442), handle (282,442); Scene 30 grabs the tip end from the right.

# --- open-parasol pose (ref f5551) -------------------------------------------
ANG_OPEN = math.radians(-100.0)     # pole points up, tilted ~10deg left
GRIP_OPEN = (455.0, 372.0)
LUP_OPEN = 150.0
CANOPY_R = 244.0
LDN = 72.0                          # grip -> handle end (below the hand)


# ---------------------------------------------------------------------------
# Petal storm: each settled SPLASH_FIELD droplet morphs into a swirling petal.
# Half persist as petals (the swirling field); the rest fade out, leaving the
# moderate scatter the ref shows. Deterministic so frame 0 == Scene 28's end.
# ---------------------------------------------------------------------------
_rng = random.Random(5290)
PETALS = []
FADERS = []
for _k, (_sx, _sy, _ss) in enumerate(SPLASH_FIELD):
    if _k % 2 == 0:
        PETALS.append(dict(
            start=(_sx, _sy), ss=_ss,
            home=(_rng.uniform(28, 932), _rng.uniform(36, 690)),
            orb_r=_rng.uniform(16, 64),
            orb_ph=_rng.uniform(0.0, 2 * math.pi),
            orb_sp=_rng.uniform(0.5, 1.3) * (1 if _k % 4 < 2 else -1),
            spin=_rng.uniform(0.4, 1.2) * (1 if _k % 3 else -1),
            size=_rng.uniform(26, 60),
            drift=_rng.uniform(10, 26),
        ))
    else:
        FADERS.append((_sx, _sy, _ss))


def petal_live(p, tt):
    """The swirling live position/rotation of a settled petal at time tt (s)."""
    a = p["orb_ph"] + p["orb_sp"] * tt
    ox = p["orb_r"] * math.cos(a)
    oy = p["orb_r"] * math.sin(a)
    x = p["home"][0] + ox
    y = ((p["home"][1] + p["drift"] * tt + oy + 40.0) % 800.0) - 40.0
    rot = p["spin"] * tt + p["orb_ph"]
    return x, y, rot


def draw_petals(c, i):
    tt = i / 30.0
    if i < FORM_END:
        m = ease(i / float(FORM_END), "in_out")
        for sx, sy, ss in FADERS:                  # spray droplets fading away
            r = ss * (1.0 - clamp01(i / 30.0))
            if r > 0.4:
                c.circle(sx, sy, r, color=WHITE)
        for p in PETALS:                           # droplets morphing to petals
            lx, ly, lrot = petal_live(p, tt)
            x = lerp(p["start"][0], lx, m)
            y = lerp(p["start"][1], ly, m)
            h = lerp(p["ss"] * 1.7, p["size"], m)
            for poly in sakura_petal(x, y, w=h * 0.66, h=h, rot=lrot * m):
                c.polygon(poly, color=WHITE)
    else:
        for p in PETALS:
            x, y, rot = petal_live(p, tt)
            for poly in sakura_petal(x, y, w=p["size"] * 0.66, h=p["size"], rot=rot):
                c.polygon(poly, color=WHITE)


# ---------------------------------------------------------------------------
# Yuka + her parasol.  The canopy uses ONE morphing outline so the open dome
# (op=1) and the furled shaft bundle (op=0) are the same code path -> no pop.
# ---------------------------------------------------------------------------
def canopy_outline(tip, ang, r, op):
    """Parasol fabric. op=1 -> big round dome bulging +ang beyond *tip*;
    op=0 -> a thin furled sliver running back along the pole (-ang)."""
    d = (math.cos(ang), math.sin(ang))
    px, py = math.cos(ang + math.pi / 2), math.sin(ang + math.pi / 2)
    half_w = lerp(15.0, r, op)
    bulge = lerp(0.0, r * 0.92, op)
    furl = lerp(r * 0.95, 0.0, op)
    nseg = 18
    rim = []
    for k in range(nseg + 1):
        f = k / nseg
        lat = lerp(-half_w, half_w, f)
        prof = bulge * (math.sin(math.pi * f) ** 0.7)
        scal = (op * r * 0.04) * math.sin(f * nseg * math.pi)   # rim scallop
        rim.append((tip[0] + lat * px + (prof + scal) * d[0],
                    tip[1] + lat * py + (prof + scal) * d[1]))
    tail = (tip[0] - furl * d[0], tip[1] - furl * d[1])
    return rim + [tail]


def parasol_assembly(grip, ang, lup, ldn, r, op):
    polys = []
    d = (math.cos(ang), math.sin(ang))
    tip = (grip[0] + lup * d[0], grip[1] + lup * d[1])
    handle = (grip[0] - ldn * d[0], grip[1] - ldn * d[1])
    polys.append(canopy_outline(tip, ang, r, op))
    polys += ribbon([tip, grip, handle], 6)                     # pole
    # J hook at the handle end, curling back toward the canopy side
    ha = ang + math.pi
    hook = arc_points(handle[0] + 11 * math.cos(ha - math.pi / 2),
                      handle[1] + 11 * math.sin(ha - math.pi / 2),
                      11, ha + 1.4, ha - 1.4, 10)
    polys += ribbon(hook, 6)
    polys.append([(tip[0] + 7, tip[1]), (tip[0] - 7, tip[1] + 4),
                  (tip[0] - 3, tip[1] - 9)])                    # finial nub
    return polys, grip


def yuka_body(grip, yoff=0.0):
    """Yuka in profile facing RIGHT, gripping the pole at *grip*; long hair back,
    billowing wavy-hemmed gown.  yoff slides her vertically for the rise-in."""
    polys = []
    Hd = (515.0, 300.0 + yoff)
    R = 41.0
    shoulder = (492.0, 356.0 + yoff)
    waist = (470.0, 452.0 + yoff)
    hemy = 660.0 + yoff * 0.4
    # back hair: flows from the head back-left and down
    polys.append([
        (Hd[0] - 6, Hd[1] - R), (Hd[0] - 46, Hd[1] - R * 0.5),
        (Hd[0] - 70, Hd[1] + 40), (Hd[0] - 78, waist[1] - 20),
        (Hd[0] - 96, hemy - 60), (Hd[0] - 52, hemy - 50),
        (Hd[0] - 30, waist[1]), (Hd[0] - 18, shoulder[1]),
        (Hd[0] - 12, Hd[1] + R * 0.4),
    ])
    polys += head(Hd[0], Hd[1], R)
    polys.append([(Hd[0] + R * 0.84, Hd[1] - 4), (Hd[0] + R * 1.2, Hd[1] + 7),
                  (Hd[0] + R * 0.82, Hd[1] + 16)])              # nose bump (faces R)
    polys.append([(Hd[0] - 10, Hd[1] + R * 0.7), (Hd[0] + 16, Hd[1] + R * 0.7),
                  (shoulder[0] + 6, shoulder[1]), (shoulder[0] - 18, shoulder[1])])  # neck
    # billowing gown with a wavy hem
    hem = []
    for k in range(9):
        f = k / 8.0
        hx = lerp(waist[0] + 96, waist[0] - 118, f)
        hem.append((hx, hemy + 16 * math.sin(f * 3.2 * math.pi)))
    polys.append([(shoulder[0] + 12, shoulder[1] - 4), (shoulder[0] - 30, shoulder[1] - 2),
                  (waist[0] - 30, waist[1]), (waist[0] - 70, hemy - 30)]
                 + hem + [(waist[0] + 86, hemy - 26), (waist[0] + 30, waist[1])])
    # front (near) arm reaching up-left to grip the pole
    polys += ribbon([(shoulder[0] + 8, shoulder[1] + 16),
                     ((shoulder[0] + grip[0]) / 2 + 8, (shoulder[1] + grip[1]) / 2),
                     (grip[0], grip[1])], [19, 13, 9])
    return polys


def draw(c, u, i, t):
    c.fill(BLACK)
    draw_petals(c, i)

    if i < RISE_0:
        return                                  # petal storm only

    # Yuka rises in among the petals
    if i < RISE_1:
        yoff = lerp(250.0, 0.0, ease((i - RISE_0) / float(RISE_1 - RISE_0), "out"))
    else:
        yoff = 0.0

    if i < HOLD_END:
        grip = (GRIP_OPEN[0], GRIP_OPEN[1] + yoff)
        assembly, _ = parasol_assembly(grip, ANG_OPEN, LUP_OPEN, LDN, CANOPY_R, 1.0)
        draw_polys(c, yuka_body(grip, yoff), color=WHITE)
        draw_polys(c, assembly, color=WHITE)
    else:
        cl = ease((i - HOLD_END) / float(SCENE_END_FRAME - SCENE_START_FRAME - HOLD_END), "in_out")
        grip = (lerp(GRIP_OPEN[0], HANDOFF_GRIP[0], cl),
                lerp(GRIP_OPEN[1], HANDOFF_GRIP[1], cl))
        ang = lerp(ANG_OPEN, HANDOFF_ANG, cl)
        lup = lerp(LUP_OPEN, HANDOFF_LUP, cl)
        ldn = lerp(LDN, HANDOFF_LDN, cl)
        op = 1.0 - cl
        assembly, _ = parasol_assembly(grip, ang, lup, ldn, CANOPY_R, op)
        draw_polys(c, yuka_body(grip, 0.0), color=WHITE)
        draw_polys(c, assembly, color=WHITE)


if __name__ == "__main__":
    writer = FrameWriter(FRAMES_DIR, start_frame=SCENE_START_FRAME)
    n = render_scene(writer, SCENE_DURATION, draw, bg=BLACK)   # W-on-B
    print(f"Scene 29: wrote {n} frames "
          f"({SCENE_START_FRAME}..{writer.frame_index - 1})")

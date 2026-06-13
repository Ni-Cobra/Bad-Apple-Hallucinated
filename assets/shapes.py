"""shapes.py -- shared silhouette toolkit for the Bad Apple!! fan recreation.

This is Phase 1 of the project (see PROJECT.md sec.9). It provides ONE consistent
silhouette vocabulary that every scene imports, so (a) recurring characters look
the same across the video and (b) every shape that MORPHS across a scene boundary
is defined exactly ONCE and shared by both adjacent scenes (PROJECT.md sec.6 rule 2).

CONVENTIONS
-----------
* Every builder returns a `list[polygon]`, where each polygon is a `list[(x, y)]`
  in logical 960x720 pixels. Draw with `draw_polys(canvas, polys)`. Returning a
  uniform list-of-polys (even for single-polygon props) means `draw_polys`,
  `transform_polys`, and `mirror_polys` work on everything.
* Characters are authored at a CANONICAL position/size (standing figures: centred
  on x=480, head near y=120, hem/feet near y=640, ~520 px tall). Move/scale them
  for a scene with `transform_polys(reimu_front(), translate=..., scale=...)`.
* All silhouettes are pure ink (no colour arg); the Canvas decides black-on-white
  vs white-on-black via its polarity. The only colour overrides in this module are
  inside `draw_yinyang` (which is intrinsically two-tone) and the optional gray of
  `crown_splash`.

EXPORTED API
------------
Geometry helpers:
    circle_poly, ellipse_poly, ribbon, arc_points, mirror_x, mirror_polys,
    transform_polys, draw_polys, lerp_polys

Figure parts (style primitives, reused by characters & scenes):
    head, dress_body, limb, reimu_bow, detached_sleeve, witch_hat, mob_cap,
    long_hair, ponytail

Recurring characters (PROJECT.md sec.9):
    reimu_back   -- scene 1 reveal (back view, big bow)
    reimu_front  -- scenes 1-2 (front dancing, pose='neutral'|'apple'|'wind')
    reimu_hairdown -- scenes 32/33/35 (PC-98 / final: hair down, broad sleeves)
    marisa_broom -- scenes 3/35 (witch on broom, side view)
    marisa_hat   -- just the hat (feature)
    yukari       -- scenes 23/24 (parasol + mob cap)

Handoff shapes & shared props (the morph chain, PROJECT.md sec.6):
    apple, apple_core            (sc 1,2,3,35 / 3->4)
    broom                        (sc 3,35)
    sakura_petal                 (sc 8,9->10)
    moon                         (sc 13,14,15)
    leaf_maple, leaf_ginkgo      (sc 19,20)
    fan_open                     (sc 9,23,24)
    parasol                      (sc 23,29,30)
    scythe                       (sc 10,30,31)
    teacup                       (sc 5->6)
    knife                        (sc 6->7)
    rod_of_remorse               (sc 11->12)
    pen                          (sc 25->26)
    gourd, drop                  (sc 26->27, 28, 31)
    doll                         (sc 27->28)
    gap_sukima                   (sc 22->23)
    sdm_skyline                  (sc 3)
    crown_splash                 (sc 28,31)

Scene helpers (draw directly to a canvas):
    draw_stars(canvas, ...)      -- the scene-3 starfield (fixed, frame-stable)
    draw_yinyang(canvas, ...)    -- scenes 33/34/35 taiji orb (two-tone)
"""

from __future__ import annotations

import math
import os
import random
import sys

# Make renderlib importable whether this module is imported by a scene
# (which already added src/ to the path) or run standalone for a preview.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from renderlib import (  # noqa: E402
    WIDTH, HEIGHT, BLACK, WHITE, transform, lerp, clamp01,
)

# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def circle_poly(cx, cy, r, n=48):
    """A circle as an n-gon polygon (wrapped in a 1-element list)."""
    return [[(cx + r * math.cos(2 * math.pi * i / n),
              cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]]


def ellipse_poly(cx, cy, rx, ry, n=48, rot=0.0):
    """An axis- or arbitrary-rotation ellipse as an n-gon polygon list."""
    ca, sa = math.cos(rot), math.sin(rot)
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        x, y = rx * math.cos(a), ry * math.sin(a)
        out.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return [out]


def arc_points(cx, cy, r, a0, a1, n=24):
    """Sampled points along a circular arc from angle a0 to a1 (radians)."""
    return [(cx + r * math.cos(lerp(a0, a1, k / n)),
             cy + r * math.sin(lerp(a0, a1, k / n))) for k in range(n + 1)]


def ribbon(centerline, widths):
    """Build a tapered closed polygon around a polyline centreline.

    *widths* is a half-width (scalar applied to all, or a per-point list).
    Used for arms, legs, broom handles, staffs, pen bodies, ribbon tails, etc.
    Returns a single-polygon list.
    """
    pts = [(float(x), float(y)) for x, y in centerline]
    n = len(pts)
    if isinstance(widths, (int, float)):
        widths = [widths] * n
    normals = []
    for i in range(n):
        if i == 0:
            dx, dy = pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]
        elif i == n - 1:
            dx, dy = pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1]
        else:
            dx, dy = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
        L = math.hypot(dx, dy) or 1.0
        normals.append((-dy / L, dx / L))
    left = [(pts[i][0] + normals[i][0] * widths[i],
             pts[i][1] + normals[i][1] * widths[i]) for i in range(n)]
    right = [(pts[i][0] - normals[i][0] * widths[i],
              pts[i][1] - normals[i][1] * widths[i]) for i in range(n)]
    return [left + right[::-1]]


def mirror_x(points, axis):
    """Reflect a single polygon's points across the vertical line x=axis."""
    return [(2 * axis - x, y) for x, y in points]


def mirror_polys(polys, axis):
    """Reflect a list of polygons across x=axis (preserves the list shape)."""
    return [mirror_x(p, axis) for p in polys]


def transform_polys(polys, **kw):
    """Apply renderlib.transform(**kw) to every polygon in a list."""
    return [transform(p, **kw) for p in polys]


def draw_polys(c, polys, color=None):
    """Draw every polygon in *polys* onto canvas *c* (one ink silhouette)."""
    for p in polys:
        if len(p) >= 3:
            c.polygon(p, color=color)


def lerp_polys(polys_a, polys_b, t):
    """Per-vertex lerp between two equal-shaped poly-lists (simple tweening).

    Requires matching structure (same #polys, same #points each). For genuine
    shape morphs between DIFFERENT outlines use renderlib.morph_polys on a
    single polygon instead.
    """
    out = []
    for pa, pb in zip(polys_a, polys_b):
        out.append([(lerp(ax, bx, t), lerp(ay, by, t))
                    for (ax, ay), (bx, by) in zip(pa, pb)])
    return out


# ---------------------------------------------------------------------------
# Figure parts (style primitives)
# ---------------------------------------------------------------------------

def head(cx, cy, r=44):
    """A head: a slightly tall ellipse."""
    return ellipse_poly(cx, cy, r * 0.92, r)


def dress_body(cx, neck_y, waist_y, hem_y, neck_w, waist_w, hem_w, sway=0.0):
    """A torso+flared-skirt silhouette as one polygon.

    Shoulders at neck_y (half-width neck_w), waist at waist_y (waist_w),
    flared hem at hem_y (hem_w). *sway* slides the hem sideways for motion.
    """
    poly = [
        (cx - neck_w, neck_y),
        (cx - waist_w, waist_y),
        (cx - hem_w + sway, hem_y - 8),
        (cx - hem_w * 0.45 + sway, hem_y),
        (cx + sway, hem_y + 10),
        (cx + hem_w * 0.45 + sway, hem_y),
        (cx + hem_w + sway, hem_y - 8),
        (cx + waist_w, waist_y),
        (cx + neck_w, neck_y),
    ]
    return [poly]


def limb(joints, widths):
    """A tapered arm/leg through *joints* (a polyline) with per-joint half-widths."""
    return ribbon(joints, widths)


def reimu_bow(cx, cy, w=95, h=62, tails=True):
    """Reimu's signature oversized hair bow: two loops + knot (+ optional tails)."""
    def loop(sign):
        return [
            (cx, cy),
            (cx + sign * w * 0.30, cy - h * 0.62),
            (cx + sign * w * 0.92, cy - h * 0.55),
            (cx + sign * w * 1.02, cy + h * 0.05),
            (cx + sign * w * 0.66, cy + h * 0.55),
            (cx + sign * w * 0.16, cy + h * 0.28),
        ]
    polys = [loop(-1), loop(1),
             [(cx - w * 0.16, cy - h * 0.34), (cx + w * 0.16, cy - h * 0.34),
              (cx + w * 0.16, cy + h * 0.34), (cx - w * 0.16, cy + h * 0.34)]]
    if tails:
        tail = [(cx - w * 0.10, cy + h * 0.2), (cx - w * 0.34, cy + h * 1.3),
                (cx - w * 0.12, cy + h * 1.45), (cx + w * 0.02, cy + h * 0.35)]
        polys += [tail, mirror_x(tail, cx)]
    return polys


def detached_sleeve(cx, top_y, w=34, h=96):
    """Reimu's detached tube sleeve: a bell shape hanging at the shoulder."""
    return [[
        (cx - w, top_y), (cx + w, top_y),
        (cx + w * 1.18, top_y + h * 0.6), (cx + w * 0.75, top_y + h),
        (cx - w * 0.75, top_y + h), (cx - w * 1.18, top_y + h * 0.6),
    ]]


def witch_hat(cx, brim_y, height=150, brim_w=120, tip_dx=46):
    """A witch hat: wide flat brim + a cone with a slightly bent tip."""
    brim = ellipse_poly(cx, brim_y, brim_w, brim_w * 0.26)
    cone = [[(cx - brim_w * 0.42, brim_y + 2),
             (cx + brim_w * 0.42, brim_y + 2),
             (cx + tip_dx * 0.55, brim_y - height * 0.55),
             (cx + tip_dx, brim_y - height)]]
    return brim + cone


def mob_cap(cx, cy, w=70, h=44):
    """A frilly mob cap (Remilia/Yukari/Yuyuko style): a dome with a scalloped rim."""
    dome = arc_points(cx, cy, w, math.pi, 2 * math.pi, 22)
    dome = [(x, y * 1.0) for x, y in dome]
    # squash vertically and add a scalloped lower rim
    dome = [(x, cy - (cy - y) * (h / w)) for x, y in dome]
    rim = []
    scallops = 6
    for k in range(scallops * 2 + 1):
        f = k / (scallops * 2)
        x = cx + w - 2 * w * f
        dip = 9 if k % 2 else 0
        rim.append((x, cy + dip))
    return [dome + rim]


def long_hair(cx, top_y, w=58, length=300):
    """A long flowing hair mass down the back (for hair-down designs)."""
    return [[
        (cx - w, top_y), (cx + w, top_y),
        (cx + w * 1.05, top_y + length * 0.5),
        (cx + w * 0.7, top_y + length),
        (cx, top_y + length * 1.06),
        (cx - w * 0.7, top_y + length),
        (cx - w * 1.05, top_y + length * 0.5),
    ]]


def ponytail(cx, cy, dx=70, dy=180, w=30):
    """A side-swept ponytail tapering to a point (Reimu/Marisa)."""
    return ribbon([(cx, cy), (cx + dx * 0.5, cy + dy * 0.3),
                   (cx + dx, cy + dy * 0.7), (cx + dx * 1.15, cy + dy)],
                  [w, w * 0.85, w * 0.5, 3])


# ---------------------------------------------------------------------------
# Recurring characters
# ---------------------------------------------------------------------------

def reimu_back(cx=480, scale=1.0):
    """Scene 1 reveal: Reimu from BEHIND -- big bow on top, widening to skirt."""
    polys = []
    polys += reimu_bow(cx, 118, 105, 70)
    polys += ellipse_poly(cx, 188, 60, 64)            # back of head/hair
    polys += dress_body(cx, 232, 372, 628, 78, 96, 162)
    polys += detached_sleeve(cx - 104, 250, 36, 104)
    polys += detached_sleeve(cx + 104, 250, 36, 104)
    if scale != 1.0:
        polys = transform_polys(polys, scale=scale, origin=(cx, 360))
    return polys


def reimu_front(cx=480, pose="neutral", scale=1.0):
    """Scenes 1-2: front-facing Reimu. pose in {'neutral','apple','wind'}.

    'apple' raises the right hand near the face (the near-bite beat);
    'wind' throws both arms back (the toss wind-up).
    """
    polys = []
    # hair behind + ponytail
    polys += ellipse_poly(cx, 168, 56, 62)
    polys += ponytail(cx + 30, 150, dx=110, dy=210, w=34)
    polys += reimu_bow(cx, 112, 92, 60)
    polys += head(cx, 172, 46)
    # side hair tubes framing the face
    polys += [[(cx - 44, 150), (cx - 30, 150), (cx - 26, 232), (cx - 46, 226)]]
    polys += [[(cx + 44, 150), (cx + 30, 150), (cx + 26, 232), (cx + 46, 226)]]
    # body
    polys += dress_body(cx, 214, 352, 612, 58, 74, 142)
    polys += detached_sleeve(cx - 80, 226, 32, 92)
    polys += detached_sleeve(cx + 80, 226, 32, 92)
    # arms
    if pose == "apple":
        polys += limb([(cx - 62, 236), (cx - 70, 300), (cx - 40, 250)], [13, 11, 9])
        polys += limb([(cx + 62, 236), (cx + 74, 300), (cx + 64, 350)], [13, 11, 8])
    elif pose == "wind":
        polys += limb([(cx - 62, 236), (cx - 110, 250), (cx - 150, 210)], [13, 10, 7])
        polys += limb([(cx + 62, 236), (cx + 110, 250), (cx + 150, 210)], [13, 10, 7])
    else:  # neutral, arms slightly out
        polys += limb([(cx - 62, 236), (cx - 92, 320), (cx - 96, 392)], [13, 11, 8])
        polys += limb([(cx + 62, 236), (cx + 92, 320), (cx + 96, 392)], [13, 11, 8])
    if scale != 1.0:
        polys = transform_polys(polys, scale=scale, origin=(cx, 360))
    return polys


def reimu_hairdown(cx=480, scale=1.0):
    """Scenes 32/33/35: PC-98 / final Reimu -- hair down, broad sleeves, small bow."""
    polys = []
    polys += long_hair(cx, 150, 66, 330)               # long hair down the back
    polys += reimu_bow(cx, 120, 60, 40, tails=False)   # small bow
    polys += head(cx, 172, 46)
    polys += dress_body(cx, 214, 352, 612, 60, 78, 150)
    # broad kimono-style sleeves (wider, no ruffle/bell shaping)
    polys += [[(cx - 60, 224), (cx - 150, 250), (cx - 150, 330), (cx - 60, 320)]]
    polys += [[(cx + 60, 224), (cx + 150, 250), (cx + 150, 330), (cx + 60, 320)]]
    if scale != 1.0:
        polys = transform_polys(polys, scale=scale, origin=(cx, 360))
    return polys


def marisa_hat(cx=480, brim_y=150):
    """Just Marisa's witch hat (feature builder)."""
    return witch_hat(cx, brim_y, height=130, brim_w=118, tip_dx=52)


def marisa_broom(cx=480, cy=360, scale=1.0, facing=-1):
    """Scenes 3/35: Marisa riding her broom, side view.

    *facing* = -1 travels left (scene 3, right-to-left), +1 travels right.
    Composition: long broom (handle + bristle fan) with Marisa seated on it,
    leaning forward, witch hat + flowing hair + ponytail.
    """
    polys = []
    f = facing
    # broom across the figure, slight upward tilt toward travel direction
    polys += broom(cx, cy + 28, length=360, angle=-0.06 * f,
                   bristle=95, thick=9, fan_dir=-f)
    # seated body leaning forward over the broom
    hipx, hipy = cx - 8 * f, cy + 6
    polys += [[(hipx - 18, hipy - 70), (hipx + 30 * f, hipy - 64),
               (hipx + 40 * f, hipy + 6), (hipx - 26, hipy + 10)]]   # torso
    # skirt/apron draping over broom
    polys += [[(hipx - 30, hipy - 4), (hipx + 36 * f, hipy - 6),
               (hipx + 44 * f, hipy + 34), (hipx - 40, hipy + 30)]]
    # leg folded forward
    polys += limb([(hipx + 6 * f, hipy + 8), (hipx + 40 * f, hipy + 26),
                   (hipx + 60 * f, hipy + 8)], [12, 10, 7])
    # head + hat, leaning forward (in travel direction)
    headx, heady = hipx + 26 * f, hipy - 96
    polys += long_hair(headx - 18 * f, heady - 6, 26, 150)
    polys += ponytail(headx - 24 * f, heady + 4, dx=-70 * f, dy=120, w=24)
    polys += head(headx, heady, 38)
    polys += transform_polys(witch_hat(headx, heady - 30, height=104,
                                       brim_w=92, tip_dx=44 * f),
                             rotate=-0.12 * f, origin=(headx, heady - 30))
    # arms forward gripping the broom
    polys += limb([(headx - 4 * f, heady + 34), (hipx + 30 * f, hipy - 30),
                   (hipx + 52 * f, hipy - 4)], [11, 9, 6])
    if scale != 1.0:
        polys = transform_polys(polys, scale=scale, origin=(cx, cy))
    return polys


def yukari(cx=480, scale=1.0):
    """Scenes 23/24: Yukari standing with parasol over her shoulder, mob cap."""
    polys = []
    polys += long_hair(cx, 158, 70, 300)               # long wavy hair
    polys += head(cx, 176, 46)
    polys += mob_cap(cx, 150, 78, 48)                  # mob cap with frill
    polys += dress_body(cx, 220, 360, 616, 62, 82, 156)
    polys += limb([(cx + 62, 236), (cx + 96, 300), (cx + 70, 250)], [13, 11, 8])
    polys += limb([(cx - 62, 236), (cx - 96, 320), (cx - 100, 392)], [13, 11, 8])
    # parasol resting on the right shoulder, tilted
    polys += transform_polys(parasol(cx + 150, 150, r=130, pole=190),
                             rotate=0.5, origin=(cx + 150, 150))
    if scale != 1.0:
        polys = transform_polys(polys, scale=scale, origin=(cx, 360))
    return polys


# ---------------------------------------------------------------------------
# Handoff shapes & shared props
# ---------------------------------------------------------------------------

def apple(cx, cy, r=60):
    """A whole apple: round body with a top dimple, stem, and leaf."""
    body = [
        (cx, cy - r * 0.72),
        (cx + r * 0.5, cy - r * 0.95), (cx + r * 0.95, cy - r * 0.4),
        (cx + r, cy + r * 0.2), (cx + r * 0.6, cy + r * 0.9), (cx, cy + r),
        (cx - r * 0.6, cy + r * 0.9), (cx - r, cy + r * 0.2),
        (cx - r * 0.95, cy - r * 0.4), (cx - r * 0.5, cy - r * 0.95),
    ]
    stem = ribbon([(cx, cy - r * 0.72), (cx + 5, cy - r * 1.18)], 4)
    leaf = ellipse_poly(cx + r * 0.38, cy - r * 1.0, r * 0.3, r * 0.13, rot=-0.5)
    return [body] + stem + leaf


def apple_core(cx, cy, r=40):
    """An eaten apple core: an hourglass (bulge-neck-bulge) with a stem."""
    core = [
        (cx - r * 0.52, cy - r), (cx + r * 0.52, cy - r),
        (cx + r * 0.18, cy),
        (cx + r * 0.52, cy + r), (cx - r * 0.52, cy + r),
        (cx - r * 0.18, cy),
    ]
    stem = ribbon([(cx, cy - r), (cx + 3, cy - r - 15)], 3)
    return [core] + stem


def broom(cx, cy, length=320, angle=0.0, bristle=90, thick=8, fan_dir=1):
    """A broom: a handle (ribbon) with a bristle fan at one end.

    *fan_dir* = +1 puts the bristle fan at the +angle end, -1 at the other end.
    """
    ca, sa = math.cos(angle), math.sin(angle)
    hx, hy = cx - fan_dir * (length / 2) * ca, cy - fan_dir * (length / 2) * sa
    bx, by = cx + fan_dir * (length / 2) * ca, cy + fan_dir * (length / 2) * sa
    handle = ribbon([(hx, hy), (bx, by)], thick)
    tipx, tipy = bx + fan_dir * bristle * ca, by + fan_dir * bristle * sa
    perp = (-sa, ca)
    spread = bristle * 0.7
    fan = [(bx, by)]
    nb = 8
    for k in range(nb + 1):
        f = k / nb - 0.5
        fan.append((tipx + perp[0] * spread * f, tipy + perp[1] * spread * f))
    return handle + [fan]


def sakura_petal(cx, cy, w=44, h=64, rot=0.0):
    """A cherry-blossom petal: teardrop with a notch at the wide end."""
    pts = [
        (0, -h * 0.5),
        (w * 0.42, -h * 0.08), (w * 0.5, h * 0.4), (w * 0.24, h * 0.5),
        (0, h * 0.14),
        (-w * 0.24, h * 0.5), (-w * 0.5, h * 0.4), (-w * 0.42, -h * 0.08),
    ]
    ca, sa = math.cos(rot), math.sin(rot)
    return [[(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]]


def moon(cx, cy, r=110):
    """A full moon (plain disc; scenes add a soft gray halo themselves)."""
    return circle_poly(cx, cy, r, n=64)


def leaf_maple(cx, cy, r=60, rot=0.0):
    """A stylised 5-lobe maple leaf."""
    pts = []
    lobes = 5
    for k in range(lobes):
        a = math.pi * (0.15 + 0.7 * k / (lobes - 1)) + math.pi  # fan downward-ish
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        if k < lobes - 1:
            am = math.pi * (0.15 + 0.7 * (k + 0.5) / (lobes - 1)) + math.pi
            pts.append((cx + r * 0.4 * math.cos(am), cy + r * 0.4 * math.sin(am)))
    pts.append((cx, cy + r * 0.2))           # stem base
    ca, sa = math.cos(rot), math.sin(rot)
    return [[(cx + (x - cx) * ca - (y - cy) * sa,
              cy + (x - cx) * sa + (y - cy) * ca) for x, y in pts]]


def leaf_ginkgo(cx, cy, r=58, rot=0.0):
    """A stylised fan-shaped ginkgo leaf (broad top with a central cleft)."""
    local = [(0, 0), (-r * 0.75, -r * 1.05), (-r * 0.35, -r * 0.95),
             (0, -r * 0.78), (r * 0.35, -r * 0.95), (r * 0.75, -r * 1.05)]
    ca, sa = math.cos(rot), math.sin(rot)
    return [[(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in local]]


def fan_open(cx, cy, r=120, a0=-2.5, a1=-0.6, n=18):
    """An open folding fan: an annular sector + a small pivot."""
    ri = r * 0.14
    outer = arc_points(cx, cy, r, a0, a1, n)
    inner = arc_points(cx, cy, ri, a1, a0, n)
    pivot = circle_poly(cx, cy, r * 0.06)
    return [outer + inner] + pivot


def parasol(cx, cy, r=140, pole=120, scallops=6):
    """An open parasol: a shallow scalloped dome + central pole + finial."""
    dome = arc_points(cx, cy, r, math.pi, 2 * math.pi, 40)
    dome = [(x, cy - (cy - y) * 0.5) for x, y in dome]       # squash to a dome
    edge = []
    for k in range(scallops * 2 + 1):
        f = k / (scallops * 2)
        x = cx + r - 2 * r * f
        dip = 12 if k % 2 else 0
        edge.append((x, cy + dip))
    pole_rib = ribbon([(cx, cy), (cx, cy + pole)], 4)
    finial = circle_poly(cx, cy - r * 0.5 - 6, 7)
    return [dome + edge] + pole_rib + finial


def scythe(top_x, top_y, length=320, angle=math.pi / 2, blade=130, thick=8):
    """A scythe: a straight shaft from (top_x,top_y) at *angle*, crescent blade on top."""
    ca, sa = math.cos(angle), math.sin(angle)
    ex, ey = top_x + length * ca, top_y + length * sa
    shaft = ribbon([(top_x, top_y), (ex, ey)], thick)
    # crescent blade sweeping off the top end
    ba = angle - math.pi / 2
    outer = arc_points(top_x, top_y, blade, ba - 1.5, ba + 0.4, 20)
    inner = arc_points(top_x + blade * 0.28 * math.cos(ba + 0.3),
                       top_y + blade * 0.28 * math.sin(ba + 0.3),
                       blade * 0.78, ba + 0.4, ba - 1.5, 20)
    return shaft + [outer + inner]


def teacup(cx, cy, w=46):
    """A teacup: bowl + handle + saucer."""
    bowl = [(cx - w, cy - w * 0.5), (cx + w, cy - w * 0.5),
            (cx + w * 0.6, cy + w * 0.45), (cx - w * 0.6, cy + w * 0.45)]
    handle = ellipse_poly(cx + w * 1.05, cy - w * 0.05, w * 0.32, w * 0.42)
    saucer = ellipse_poly(cx, cy + w * 0.6, w * 1.45, w * 0.2)
    return [bowl] + handle + saucer


def knife(cx, cy, length=120, angle=0.0, w=12):
    """A throwing knife: a tapered blade + short handle, pointing along *angle*."""
    ca, sa = math.cos(angle), math.sin(angle)
    perp = (-sa, ca)
    tip = (cx + length * ca, cy + length * sa)
    blade = [(cx + perp[0] * w, cy + perp[1] * w), tip,
             (cx - perp[0] * w, cy - perp[1] * w)]
    handle = ribbon([(cx, cy), (cx - 34 * ca, cy - 34 * sa)], 6)
    return [blade] + handle


def rod_of_remorse(cx, cy, length=300, angle=-math.pi / 2):
    """Eiki's Rod of Remorse: a staff with an ornate head, pointing along *angle*."""
    ca, sa = math.cos(angle), math.sin(angle)
    hx, hy = cx + length * ca, cy + length * sa            # head end
    shaft = ribbon([(cx, cy), (hx, hy)], 7)
    head_orn = ellipse_poly(hx, hy, 16, 24, rot=angle)
    ring = ellipse_poly(hx - 26 * ca, hy - 26 * sa, 13, 13)
    return shaft + head_orn + ring


def pen(cx, cy, length=140, angle=0.0, w=8):
    """A pen/brush: a body tapering to a nib point along *angle*."""
    ca, sa = math.cos(angle), math.sin(angle)
    back = (cx - length * 0.5 * ca, cy - length * 0.5 * sa)
    nib = (cx + length * 0.5 * ca, cy + length * 0.5 * sa)
    mid = (cx + length * 0.3 * ca, cy + length * 0.3 * sa)
    return ribbon([back, mid, nib], [w, w * 0.8, 1])


def gourd(cx, cy, r=60):
    """A two-lobed sake gourd (small top lobe over a big bottom lobe) + stopper."""
    top = ellipse_poly(cx, cy - r * 0.55, r * 0.42, r * 0.46)
    bottom = ellipse_poly(cx, cy + r * 0.42, r * 0.72, r * 0.62)
    stopper = [(cx - r * 0.16, cy - r * 1.0), (cx + r * 0.16, cy - r * 1.0),
               (cx + r * 0.16, cy - r * 0.85), (cx - r * 0.16, cy - r * 0.85)]
    return bottom + top + [stopper]


def drop(cx, cy, r=24):
    """A teardrop: rounded bottom tapering to a point at the top."""
    pts = [(cx, cy - r * 1.9)]
    pts += arc_points(cx, cy, r, -math.pi * 0.18, math.pi + math.pi * 0.18, 18)
    return [pts]


def doll(cx, cy, scale=1.0):
    """Alice's little doll: a tiny figure (head + bell dress + stub arms)."""
    polys = []
    polys += head(cx, cy - 34, 16)
    polys += [[(cx - 14, cy - 20), (cx + 14, cy - 20),
               (cx + 26, cy + 40), (cx - 26, cy + 40)]]     # bell dress
    polys += [[(cx - 14, cy - 14), (cx - 30, cy + 8), (cx - 22, cy + 14),
               (cx - 8, cy - 4)]]                            # left arm
    polys += [[(cx + 14, cy - 14), (cx + 30, cy + 8), (cx + 22, cy + 14),
               (cx + 8, cy - 4)]]                            # right arm
    if scale != 1.0:
        polys = transform_polys(polys, scale=scale, origin=(cx, cy))
    return polys


def gap_sukima(cx, cy, w=240, h=90, lashes=True):
    """Yukari's gap (sukima): a horizontal eye/lens, optionally with lashes.

    Also the scene-22 'TV switching off' slit -- animate *h* toward 0 to close it.
    """
    n = 26
    top = [(cx - w / 2 + w * (k / n), cy - (h / 2) * math.sin(math.pi * (k / n)))
           for k in range(n + 1)]
    bot = [(cx + w / 2 - w * (k / n), cy + (h / 2) * math.sin(math.pi * (k / n)))
           for k in range(n + 1)]
    polys = [top + bot]
    if lashes:
        for k in range(1, n, 3):
            f = k / n
            x = cx - w / 2 + w * f
            yt = cy - (h / 2) * math.sin(math.pi * f)
            yb = cy + (h / 2) * math.sin(math.pi * f)
            polys += ribbon([(x, yt), (x, yt - 16)], 3)
            polys += ribbon([(x, yb), (x, yb + 16)], 3)
    return polys


def sdm_skyline(base_x=120, base_y=600, w=300, h=190):
    """The Scarlet Devil Mansion skyline: a mansion block with a central domed tower."""
    polys = []
    # main hall block
    polys += [[(base_x - w * 0.5, base_y), (base_x - w * 0.5, base_y - h * 0.55),
               (base_x + w * 0.5, base_y - h * 0.55), (base_x + w * 0.5, base_y)]]
    # crenellations along the top of the hall
    cren_y = base_y - h * 0.55
    for k in range(6):
        x = base_x - w * 0.5 + w * (k + 0.2) / 6
        polys += [[(x, cren_y), (x + w * 0.08, cren_y),
                   (x + w * 0.08, cren_y - 12), (x, cren_y - 12)]]
    # central tower
    tw = w * 0.22
    polys += [[(base_x - tw / 2, cren_y), (base_x - tw / 2, base_y - h * 0.85),
               (base_x + tw / 2, base_y - h * 0.85), (base_x + tw / 2, cren_y)]]
    # onion/conical dome + spire
    polys += [[(base_x - tw / 2 - 6, base_y - h * 0.85),
               (base_x, base_y - h * 1.02),
               (base_x + tw / 2 + 6, base_y - h * 0.85)]]
    polys += ribbon([(base_x, base_y - h * 1.02), (base_x, base_y - h * 1.12)], 2)
    # two small side turrets
    for sx in (base_x - w * 0.42, base_x + w * 0.42):
        polys += [[(sx - 12, cren_y), (sx - 12, base_y - h * 0.7),
                   (sx + 12, base_y - h * 0.7), (sx + 12, cren_y)]]
        polys += [[(sx - 14, base_y - h * 0.7), (sx, base_y - h * 0.8),
                   (sx + 14, base_y - h * 0.7)]]
    return polys


def crown_splash(cx, cy, r=120, spikes=11, t=1.0, color=None):
    """A milk-crown / coronet splash: a rim with droplet-tipped spikes.

    *t* in [0,1] scales the splash radius/spike height for animation.
    """
    rr = r * clamp01(t)
    polys = list(ellipse_poly(cx, cy, rr, rr * 0.34))     # base rim
    for k in range(spikes):
        a = math.pi + math.pi * (k / (spikes - 1))         # over the top arc
        bx = cx + rr * 0.9 * math.cos(a)
        by = cy + rr * 0.34 * math.sin(a)
        hgt = (0.5 + 0.5 * math.sin(math.pi * k / (spikes - 1))) * rr * 0.7 * t
        tipx, tipy = bx, by - hgt
        polys += [[(bx - 7, by), (bx + 7, by), (tipx + 3, tipy)]]
        polys += circle_poly(tipx, tipy - 5, 7)            # droplet bead
    return polys


# ---------------------------------------------------------------------------
# Scene helpers (draw directly to a canvas)
# ---------------------------------------------------------------------------

# A fixed star field for scene 3 (and any starry passage). Generated once with a
# fixed seed so positions are identical on every frame and every run.
_star_rng = random.Random(20091027)   # the original upload date, for luck
STARS = [(_star_rng.uniform(0, WIDTH), _star_rng.uniform(0, HEIGHT),
          _star_rng.choice([1, 1, 1, 1.5, 1.5, 2, 2.5]))
         for _ in range(170)]


def draw_stars(c, color=WHITE, brightness=1.0):
    """Draw the fixed starfield onto canvas *c* (default white dots, for W-on-B)."""
    for x, y, s in STARS:
        c.circle(x, y, s * brightness, color=color)


def draw_yinyang(c, cx, cy, r, angle=0.0, dark=BLACK, light=WHITE):
    """Draw a taiji (yin-yang) orb of radius *r*, rotated by *angle* radians.

    Intrinsically two-tone, so this draws explicit colours rather than ink.
    Built by disc composition: light circle -> dark half -> light/dark bumps ->
    the two opposite-colour eyes.
    """
    ca, sa = math.cos(angle), math.sin(angle)

    def rot(px, py):
        return (cx + px * ca - py * sa, cy + px * sa + py * ca)

    # full light disc
    c.circle(cx, cy, r, color=light)
    # dark half: the semicircle on the local -x side
    half = [rot(*p) for p in
            ([(0, -r)] + [(-r * math.sin(math.pi * k / 24),
                           -r * math.cos(math.pi * k / 24)) for k in range(25)])]
    # build a proper half-disc polygon (diameter + arc on the left)
    arc = [rot(r * math.cos(math.pi / 2 + math.pi * k / 24),
               r * math.sin(math.pi / 2 + math.pi * k / 24)) for k in range(25)]
    c.polygon(arc, color=dark)
    # bumps straddling the seam: top stays light, bottom goes dark
    topx, topy = rot(0, -r / 2)
    botx, boty = rot(0, r / 2)
    c.circle(topx, topy, r / 2, color=light)
    c.circle(botx, boty, r / 2, color=dark)
    # the two eyes
    c.circle(topx, topy, r / 6, color=dark)
    c.circle(botx, boty, r / 6, color=light)


if __name__ == "__main__":
    # Tiny self-check: build everything once so import/argument errors surface.
    _checks = [
        reimu_back(), reimu_front(pose="apple"), reimu_front(pose="wind"), reimu_hairdown(),
        marisa_broom(), yukari(), apple(480, 360), apple_core(480, 360),
        broom(480, 360), sakura_petal(480, 360), moon(480, 360),
        leaf_maple(480, 360), leaf_ginkgo(480, 360), fan_open(480, 360),
        parasol(480, 360), scythe(480, 200), teacup(480, 360), knife(480, 360),
        rod_of_remorse(480, 500), pen(480, 360), gourd(480, 360), drop(480, 360),
        doll(480, 360), gap_sukima(480, 360), sdm_skyline(), crown_splash(480, 360),
    ]
    print(f"shapes.py self-check OK: {len(_checks)} builders, "
          f"{sum(len(p) for p in _checks)} polygons total")

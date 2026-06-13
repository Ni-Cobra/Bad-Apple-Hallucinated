"""_preview.py -- render every shared asset to one contact sheet for visual QC.

Scratch tool (underscore-prefixed). Writes:
    frames/_assets_preview/assets_contact.png   <- view this ONE image

Run: python assets/_preview.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, HERE)

from renderlib import Canvas, BLACK, WHITE  # noqa: E402
import shapes as S  # noqa: E402
sys.path.insert(0, os.path.join(HERE, "..", "tests"))
from contact_sheet import contact_sheet  # noqa: E402


def cell(polys=None, bg=WHITE, draw_fn=None, special=None):
    c = Canvas()
    if draw_fn:
        draw_fn(c)
    if polys:
        S.draw_polys(c, polys)
    return c


def main():
    items, labels = [], []

    def add(label, polys=None, bg=WHITE, draw_fn=None):
        c = Canvas(bg=bg)
        if draw_fn:
            draw_fn(c)
        if polys:
            S.draw_polys(c, polys)
        items.append(c.image())
        labels.append(label)

    # --- recurring characters ---
    add("reimu_back", S.reimu_back())
    add("reimu_front neutral", S.reimu_front())
    add("reimu_front apple", S.reimu_front(pose="apple"))
    add("reimu_front wind", S.reimu_front(pose="wind"))
    add("reimu_hairdown", S.reimu_hairdown())
    add("marisa_broom (W-on-B)", S.marisa_broom(), bg=BLACK)
    add("yukari", S.yukari())

    # --- props / handoff shapes, centred ~ (480,360) ---
    add("apple", S.apple(480, 340, 90))
    add("apple_core", S.apple_core(480, 360, 70))
    add("broom", S.broom(480, 360, length=420, bristle=120))
    add("sakura_petal", S.sakura_petal(480, 360, 120, 180))
    add("moon (W-on-B)", S.moon(480, 360, 150), bg=BLACK)
    add("leaf_maple", S.leaf_maple(480, 360, 140))
    add("leaf_ginkgo", S.leaf_ginkgo(480, 360, 150))
    add("fan_open", S.fan_open(480, 460, 220, -2.5, -0.6))
    add("parasol", S.parasol(480, 300, 200, 260))
    add("scythe (W-on-B)", S.scythe(480, 160, 420, blade=190), bg=BLACK)
    add("teacup", S.teacup(480, 360, 90))
    add("knife", S.knife(360, 360, 260, 0.0, 22))
    add("rod_of_remorse", S.rod_of_remorse(480, 560, 400))
    add("pen", S.pen(480, 360, 300, 0.3, 16))
    add("gourd", S.gourd(480, 360, 120))
    add("drop", S.drop(480, 320, 60))
    add("doll", S.doll(480, 340, 3.0))
    add("gap_sukima (W-on-B)", S.gap_sukima(480, 360, 520, 200), bg=BLACK)
    add("sdm_skyline (W-on-B)", S.sdm_skyline(480, 600, 520, 320), bg=BLACK)
    add("crown_splash (W-on-B)", S.crown_splash(480, 440, 240, t=1.0), bg=BLACK)

    # --- scene helpers ---
    def stars_scene(c):
        S.draw_stars(c)
        S.draw_polys(c, S.marisa_broom(480, 360, facing=-1))
    add("starfield + marisa", bg=BLACK, draw_fn=stars_scene)
    add("yinyang", draw_fn=lambda c: S.draw_yinyang(c, 480, 360, 240, angle=0.6))

    out = os.path.join(HERE, "..", "frames", "_assets_preview", "assets_contact.png")
    contact_sheet(items, out, cols=5, cell=(300, 225), labels=labels)
    print(f"wrote {out} ({len(items)} cells)")


if __name__ == "__main__":
    main()

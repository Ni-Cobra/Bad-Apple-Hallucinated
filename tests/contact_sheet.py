"""contact_sheet.py -- tile many frames into ONE grid PNG for cheap visual QC.

Viewing one tiled image instead of nine single frames is the project's main
token-economy lever for iteration passes (PROJECT.md sec.12). Use it whenever you
want to eyeball several frames of a scene at once; reserve single full-size Reads
for final QC of a specific pose.

API
---
    contact_sheet(items, out_path, cols=3, cell=(320, 240), pad=6,
                  bg=128, labels=None) -> out_path

*items* is a list of PIL.Image, or file paths, or renderlib Canvas objects.
Each is downscaled to fit *cell* and tiled left-to-right, top-to-bottom.
Optional *labels* (same length) are drawn in the corner of each cell.

CLI
---
    python tests/contact_sheet.py OUT.png frame_a.png frame_b.png ...
    python tests/contact_sheet.py OUT.png --glob 'frames/frame_00*.png' --cols 5
"""

import glob as _glob
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from PIL import Image, ImageDraw  # noqa: E402

try:
    from renderlib import Canvas  # noqa: E402
except Exception:  # pragma: no cover - Canvas only needed if a Canvas is passed
    Canvas = ()


def _to_image(item):
    if isinstance(item, Image.Image):
        return item
    if Canvas and isinstance(item, Canvas):
        return item.image()
    if isinstance(item, str):
        return Image.open(item)
    raise TypeError(f"contact_sheet: unsupported item type {type(item)!r}")


def contact_sheet(items, out_path, cols=3, cell=(320, 240), pad=6,
                  bg=128, labels=None):
    """Tile *items* into a grid PNG saved to *out_path*. Returns out_path."""
    cw, ch = cell
    n = len(items)
    rows = (n + cols - 1) // cols
    sheet = Image.new("L", (cols * cw + pad * (cols + 1),
                            rows * ch + pad * (rows + 1)), bg)
    draw = ImageDraw.Draw(sheet)
    for idx, item in enumerate(items):
        img = _to_image(item).convert("L")
        img.thumbnail((cw, ch), Image.LANCZOS)
        r, col = divmod(idx, cols)
        x = pad + col * (cw + pad) + (cw - img.width) // 2
        y = pad + r * (ch + pad) + (ch - img.height) // 2
        sheet.paste(img, (x, y))
        if labels and idx < len(labels) and labels[idx]:
            tx, ty = pad + col * (cw + pad) + 4, pad + r * (ch + pad) + 2
            # cheap outline for legibility on either polarity
            for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                draw.text((tx + ox, ty + oy), str(labels[idx]), fill=255)
            draw.text((tx, ty), str(labels[idx]), fill=0)
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    sheet.save(out_path)
    return out_path


def _main(argv):
    if not argv:
        print(__doc__)
        return 1
    out_path = argv[0]
    rest = argv[1:]
    cols = 3
    paths = []
    i = 0
    while i < len(rest):
        a = rest[i]
        if a == "--cols":
            cols = int(rest[i + 1]); i += 2
        elif a == "--glob":
            paths += sorted(_glob.glob(rest[i + 1])); i += 2
        else:
            paths.append(a); i += 1
    if not paths:
        print("no input frames given")
        return 1
    contact_sheet(paths, out_path, cols=cols)
    print(f"wrote {out_path} ({len(paths)} cells, {cols} cols)")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv[1:]))

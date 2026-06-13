"""encode.py -- encode numbered PNG frames into an H.264 MP4 with ffmpeg.

Usage (from the project root):

    python src/encode.py                                # frames/ -> output/badapple.mp4 @ 30fps
    python src/encode.py --frames frames/_smoke --out output/_smoke_test.mp4
    python src/encode.py --fps 30 --crf 18

Frames must be named <prefix>NNNNNN.png (default prefix "frame_", 6 digits),
numbered consecutively starting at the lowest index present.

Requires ffmpeg on PATH (install with `sudo apt install ffmpeg`, or drop a
static ffmpeg/ffprobe build in ~/.local/bin).
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import shutil
import subprocess
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Fallback location for a user-local static ffmpeg build, used when ffmpeg is
# not yet on PATH (e.g. a freshly opened shell that hasn't sourced ~/.profile).
LOCAL_BIN = os.path.join(os.path.expanduser("~"), ".local", "bin")


def find_tool(name: str) -> str:
    """Locate ffmpeg/ffprobe: PATH first, then ~/.local/bin."""
    on_path = shutil.which(name)
    if on_path:
        return on_path
    candidate = os.path.join(LOCAL_BIN, name)
    if os.path.isfile(candidate):
        return candidate
    sys.exit(
        f"ERROR: {name} not found on PATH or in {LOCAL_BIN}. "
        f"Install it with `sudo apt install ffmpeg`."
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="Encode PNG frames to MP4.")
    ap.add_argument("--frames", default=os.path.join(PROJECT_ROOT, "frames"),
                    help="folder containing the PNG frames")
    ap.add_argument("--out", default=os.path.join(PROJECT_ROOT, "output", "badapple.mp4"),
                    help="output mp4 path")
    ap.add_argument("--fps", type=int, default=30, help="frame rate (project standard: 30)")
    ap.add_argument("--crf", type=int, default=18,
                    help="x264 quality, lower=better (18 is visually lossless)")
    ap.add_argument("--prefix", default="frame_", help="frame filename prefix")
    ap.add_argument("--digits", type=int, default=6, help="zero-padding width")
    args = ap.parse_args()

    frames_dir = os.path.abspath(args.frames)
    out_path = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    pngs = sorted(glob.glob(os.path.join(frames_dir, f"{args.prefix}*.png")))
    if not pngs:
        sys.exit(f"ERROR: no '{args.prefix}*.png' frames found in {frames_dir}")
    m = re.search(rf"{re.escape(args.prefix)}(\d+)\.png$", pngs[0])
    start_number = int(m.group(1)) if m else 0

    ffmpeg = find_tool("ffmpeg")
    pattern = os.path.join(frames_dir, f"{args.prefix}%0{args.digits}d.png")
    cmd = [
        ffmpeg, "-y",
        "-framerate", str(args.fps),
        "-start_number", str(start_number),
        "-i", pattern,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", str(args.crf),
        "-pix_fmt", "yuv420p",      # broadest player compatibility
        "-movflags", "+faststart",
        out_path,
    ]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    size = os.path.getsize(out_path)
    print(f"OK: wrote {out_path} ({size} bytes, {len(pngs)} frames @ {args.fps} fps)")


if __name__ == "__main__":
    main()

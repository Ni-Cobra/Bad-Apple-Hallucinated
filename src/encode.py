"""encode.py -- encode numbered PNG frames into an H.264 MP4 with ffmpeg.

Usage (from the project root):

    python src/encode.py                                # frames/ -> output/badapple.mp4 @ 30fps (+ audio if present)
    python src/encode.py --frames frames/_smoke --out output/_smoke_test.mp4
    python src/encode.py --fps 30 --crf 18
    python src/encode.py --no-audio                     # video only
    python src/encode.py --audio path/to/track.mp3      # use a specific audio file
    python src/encode.py --no-compare                   # skip the side-by-side comparison

Frames must be named <prefix>NNNNNN.png (default prefix "frame_", 6 digits),
numbered consecutively starting at the lowest index present.

Audio: when assets/badapple_audio.mp3 exists (the original Bad Apple!! PV track)
it is muxed into the MP4 automatically as AAC and trimmed to the shorter of the
two streams (-shortest), so partial-preview renders get a matching slice of the
song. Pass --no-audio for a silent render, or --audio FILE to override the track.

Comparison: when assets/badapple_original.mp4 exists (the canonical PV, fetched
separately and gitignored) a second deliverable <out>_compare.mp4 is built
automatically right after the main encode -- our render full-size on the left,
the original at 25 % size on a black right panel, vertically centered and
start-synced (overlay shortest=1 trims the original to our render's length, so
partial-preview renders compare correctly). Same default-on-if-present pattern as
the audio. Pass --no-compare to skip, or --compare-original FILE to point at a
different source video.

Requires ffmpeg on PATH (install with `sudo apt install ffmpeg`, or drop a
static ffmpeg/ffprobe build in ~/.local/bin).
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import shutil
import struct
import subprocess
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Fallback location for a user-local static ffmpeg build, used when ffmpeg is
# not yet on PATH (e.g. a freshly opened shell that hasn't sourced ~/.profile).
LOCAL_BIN = os.path.join(os.path.expanduser("~"), ".local", "bin")

# Original Bad Apple!! shadow-art PV soundtrack (320 kbps MP3, 219.19 s),
# muxed in by default when present. See README/TOOLING for provenance.
DEFAULT_AUDIO = os.path.join(PROJECT_ROOT, "assets", "badapple_audio.mp3")

# Canonical original Bad Apple!! PV video (Internet Archive niconico-sm8628149,
# 219.1 s, 512x384 4:3). Fetched separately and gitignored; when present, a
# side-by-side comparison render is produced automatically. See PROGRESS.md.
DEFAULT_ORIGINAL = os.path.join(PROJECT_ROOT, "assets", "badapple_original.mp4")


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


def png_size(path: str) -> tuple[int, int]:
    """Read (width, height) from a PNG's IHDR chunk -- no Pillow dependency."""
    with open(path, "rb") as fh:
        head = fh.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"not a PNG: {path}")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def build_comparison(ffmpeg: str, video_path: str, original_path: str,
                     out_path: str, crf: int, sample_png: str) -> None:
    """Compose our render (left, full size) beside the original PV (right, 25 %).

    The original is scaled to a quarter of our render's dimensions and dropped on
    a black panel that widens the canvas to the right, vertically centered. The
    overlay's shortest=1 trims the (longer) original to our render's duration so
    partial-preview encodes still line up from the first frame. Audio, if any, is
    carried over from our render (already the in-sync PV track).
    """
    w, h = png_size(sample_png)
    pw, ph = (w // 4) & ~1, (h // 4) & ~1   # 25 % size, forced even for yuv420p
    canvas_w = w + pw
    x, y = w, (h - ph) // 2
    filt = (
        f"[0:v]pad={canvas_w}:{h}:0:0:black[base];"
        f"[1:v]scale={pw}:{ph},setsar=1[orig];"
        f"[base][orig]overlay={x}:{y}:shortest=1[outv]"
    )
    cmd = [
        ffmpeg, "-y",
        "-i", video_path,
        "-i", original_path,
        "-filter_complex", filt,
        "-map", "[outv]",
        "-map", "0:a:0?",            # carry our render's audio if it has any
        "-c:v", "libx264", "-preset", "medium", "-crf", str(crf),
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        out_path,
    ]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    size = os.path.getsize(out_path)
    print(f"OK: wrote {out_path} ({size} bytes, {canvas_w}x{h} side-by-side, "
          f"original at {pw}x{ph})")


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
    ap.add_argument("--audio", default=None,
                    help=f"audio track to mux in (default: {DEFAULT_AUDIO} if it exists)")
    ap.add_argument("--no-audio", action="store_true",
                    help="encode video only, even if an audio track is present")
    ap.add_argument("--compare-original", default=None,
                    help=f"original PV to compare against (default: {DEFAULT_ORIGINAL} if it exists)")
    ap.add_argument("--compare-out", default=None,
                    help="comparison output path (default: <out>_compare.mp4)")
    ap.add_argument("--no-compare", action="store_true",
                    help="skip the side-by-side comparison render")
    args = ap.parse_args()

    frames_dir = os.path.abspath(args.frames)
    out_path = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # Resolve the audio track. --no-audio wins; an explicit --audio that is
    # missing is a hard error; the default track simply being absent is fine.
    audio_path = None
    if not args.no_audio:
        candidate = args.audio or DEFAULT_AUDIO
        if os.path.isfile(candidate):
            audio_path = os.path.abspath(candidate)
        elif args.audio:
            sys.exit(f"ERROR: audio file not found: {candidate}")
        else:
            print(f"NOTE: no audio track at {candidate}; encoding video only.")

    pngs = sorted(glob.glob(os.path.join(frames_dir, f"{args.prefix}*.png")))
    if not pngs:
        sys.exit(f"ERROR: no '{args.prefix}*.png' frames found in {frames_dir}")
    m = re.search(rf"{re.escape(args.prefix)}(\d+)\.png$", pngs[0])
    start_number = int(m.group(1)) if m else 0

    ffmpeg = find_tool("ffmpeg")
    pattern = os.path.join(frames_dir, f"{args.prefix}%0{args.digits}d.png")

    # Input 0: the PNG frame sequence (video). Input 1 (optional): the audio.
    cmd = [
        ffmpeg, "-y",
        "-framerate", str(args.fps),
        "-start_number", str(start_number),
        "-i", pattern,
    ]
    if audio_path:
        cmd += ["-i", audio_path]
    cmd += [
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", str(args.crf),
        "-pix_fmt", "yuv420p",      # broadest player compatibility
    ]
    if audio_path:
        cmd += [
            "-c:a", "aac", "-b:a", "192k",
            "-map", "0:v:0", "-map", "1:a:0",
            "-shortest",            # trim to the shorter stream (video for partial renders)
        ]
    cmd += [
        "-movflags", "+faststart",
        out_path,
    ]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    size = os.path.getsize(out_path)
    audio_note = f", audio: {os.path.basename(audio_path)}" if audio_path else ", no audio"
    print(f"OK: wrote {out_path} ({size} bytes, {len(pngs)} frames @ {args.fps} fps{audio_note})")

    # Side-by-side comparison render. Default-on when the original PV is present,
    # mirroring the audio behaviour above: an explicit --compare-original that is
    # missing is a hard error; the default source simply being absent is fine.
    if not args.no_compare:
        original = args.compare_original or DEFAULT_ORIGINAL
        if os.path.isfile(original):
            compare_out = args.compare_out or (
                os.path.splitext(out_path)[0] + "_compare" + os.path.splitext(out_path)[1])
            os.makedirs(os.path.dirname(os.path.abspath(compare_out)), exist_ok=True)
            build_comparison(ffmpeg, out_path, os.path.abspath(original),
                             os.path.abspath(compare_out), args.crf, pngs[0])
        elif args.compare_original:
            sys.exit(f"ERROR: comparison source not found: {original}")
        else:
            print(f"NOTE: no original PV at {original}; skipping comparison render.")


if __name__ == "__main__":
    main()

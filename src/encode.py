"""encode.py -- encode numbered PNG frames into an H.264 MP4 with ffmpeg.

Usage (from the project root):

    python src/encode.py                                # frames/ -> output/badapple.mp4 @ 30fps (+ audio if present)
    python src/encode.py --frames frames/_smoke --out output/_smoke_test.mp4
    python src/encode.py --fps 30 --crf 18
    python src/encode.py --no-audio                     # video only
    python src/encode.py --audio path/to/track.mp3      # use a specific audio file

Frames must be named <prefix>NNNNNN.png (default prefix "frame_", 6 digits),
numbered consecutively starting at the lowest index present.

Audio: when assets/badapple_audio.mp3 exists (the original Bad Apple!! PV track)
it is muxed into the MP4 automatically as AAC and trimmed to the shorter of the
two streams (-shortest), so partial-preview renders get a matching slice of the
song. Pass --no-audio for a silent render, or --audio FILE to override the track.

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

# Original Bad Apple!! shadow-art PV soundtrack (320 kbps MP3, 219.19 s),
# muxed in by default when present. See README/TOOLING for provenance.
DEFAULT_AUDIO = os.path.join(PROJECT_ROOT, "assets", "badapple_audio.mp3")


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
    ap.add_argument("--audio", default=None,
                    help=f"audio track to mux in (default: {DEFAULT_AUDIO} if it exists)")
    ap.add_argument("--no-audio", action="store_true",
                    help="encode video only, even if an audio track is present")
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


if __name__ == "__main__":
    main()

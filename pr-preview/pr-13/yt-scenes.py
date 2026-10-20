#!/usr/bin/env python3
"""
Extract the key thumbnail and scene-change screenshots from a YouTube video.

Usage:
    python3 yt-scenes.py <youtube-url> [--threshold N] [--max-scenes N]

Dependencies:
    pip install yt-dlp scenedetect[opencv] requests

Output is saved to a folder named after the video inside ./yt-scenes-output/.
"""

import argparse
import os
import re
import shutil
import sys
import tempfile

import requests
import yt_dlp
from scenedetect import (
    AdaptiveDetector,
    ContentDetector,
    SceneManager,
    open_video,
)
from scenedetect.scene_manager import save_images


def sanitize_filename(name: str) -> str:
    name = re.sub(r'[<>:"/\\|?*]', "", name)
    return name.strip()[:120]


def download_thumbnail(video_url: str, output_dir: str) -> str | None:
    """Download the highest-resolution thumbnail available."""
    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        info = ydl.extract_info(video_url, download=False)

    thumbnails = sorted(
        [t for t in info.get("thumbnails", []) if t.get("width")],
        key=lambda t: t["width"] * t.get("height", 0),
        reverse=True,
    )

    if not thumbnails:
        thumbnails = info.get("thumbnails", [])

    for thumb in thumbnails:
        url = thumb.get("url")
        if not url:
            continue
        ext = url.rsplit(".", 1)[-1].split("?")[0]
        if ext not in ("jpg", "jpeg", "png", "webp"):
            ext = "jpg"
        dest = os.path.join(output_dir, f"thumbnail.{ext}")
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            with open(dest, "wb") as f:
                f.write(resp.content)
            w = thumb.get("width", "?")
            h = thumb.get("height", "?")
            print(f"  Thumbnail saved ({w}x{h}): {dest}")
            return dest
        except Exception as e:
            print(f"  Thumbnail download failed ({url}): {e}")

    print("  No thumbnail could be downloaded.")
    return None


def download_video(video_url: str, tmp_dir: str) -> str:
    """Download the best-quality video to a temp directory, return the file path."""
    opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": os.path.join(tmp_dir, "%(id)s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
        "merge_output_format": "mp4",
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        return ydl.prepare_filename(info)


def detect_and_save_scenes(
    video_path: str,
    output_dir: str,
    threshold: float,
    max_scenes: int | None,
) -> int:
    """Detect scene changes and save one key frame per scene as lossless PNG."""
    video = open_video(video_path)
    sm = SceneManager()
    sm.auto_downscale = True
    sm.add_detector(AdaptiveDetector(adaptive_threshold=threshold))

    print("  Analyzing video for scene changes...")
    sm.detect_scenes(video, show_progress=True)
    scene_list = sm.get_scene_list(start_in_scene=True)

    if max_scenes and len(scene_list) > max_scenes:
        step = len(scene_list) / max_scenes
        scene_list = [scene_list[int(i * step)] for i in range(max_scenes)]

    if not scene_list:
        print("  No scene changes detected.")
        return 0

    print(f"  {len(scene_list)} scenes detected — extracting key frames...")

    image_paths = save_images(
        scene_list=scene_list,
        video=video,
        num_images=1,
        image_extension="png",
        encoder_param=1,
        output_dir=output_dir,
        image_name_template="scene-$SCENE_NUMBER-$TIMECODE",
        show_progress=True,
    )

    return len(image_paths)


def main():
    parser = argparse.ArgumentParser(
        description="Extract YouTube thumbnail and key-scene screenshots."
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "--threshold",
        type=float,
        default=3.0,
        help="Scene-change sensitivity (lower = more scenes). Default: 3.0",
    )
    parser.add_argument(
        "--max-scenes",
        type=int,
        default=None,
        help="Cap the number of extracted scenes (evenly sampled).",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="yt-scenes-output",
        help="Base output directory. Default: yt-scenes-output",
    )
    args = parser.parse_args()

    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        info = ydl.extract_info(args.url, download=False)
    title = sanitize_filename(info.get("title", info["id"]))
    out_dir = os.path.join(args.output_dir, title)
    os.makedirs(out_dir, exist_ok=True)

    print(f'\nVideo: {info.get("title")}')
    print(f"Output: {out_dir}\n")

    print("[1/3] Downloading thumbnail...")
    download_thumbnail(args.url, out_dir)

    tmp_dir = tempfile.mkdtemp()
    try:
        print("\n[2/3] Downloading video (best quality)...")
        video_path = download_video(args.url, tmp_dir)
        print(f"  Downloaded: {video_path}")

        print("\n[3/3] Detecting scenes and extracting frames...")
        n = detect_and_save_scenes(video_path, out_dir, args.threshold, args.max_scenes)
        print(f"\nDone — {n} scene frame(s) saved to {out_dir}/")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()

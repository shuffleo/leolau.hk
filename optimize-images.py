#!/usr/bin/env python3
"""
Convert all JPG/JPEG/PNG images under writings/ and works/ to WebP,
then delete the originals. Skips files that already have a .webp sibling.

Usage:
    python3 optimize-images.py          # dry-run (preview only)
    python3 optimize-images.py --run    # convert and delete originals
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required: pip install Pillow")

QUALITY = 80
EXTENSIONS = {".jpg", ".jpeg", ".png"}
SCAN_DIRS = ["writings", "works"]


def find_convertible(repo_root: Path) -> list[Path]:
    targets: list[Path] = []
    for d in SCAN_DIRS:
        scan = repo_root / d
        if not scan.exists():
            continue
        for path in scan.rglob("*"):
            if path.suffix.lower() in EXTENSIONS:
                webp = path.with_suffix(".webp")
                if not webp.exists():
                    targets.append(path)
    return sorted(targets)


def convert(path: Path) -> tuple[int, int]:
    webp = path.with_suffix(".webp")
    img = Image.open(path)
    img.save(webp, "WEBP", quality=QUALITY, method=6)
    before = path.stat().st_size
    after = webp.stat().st_size
    return before, after


TINY_WIDTH = 32
TINY_QUALITY = 50


def generate_tiny_thumbnails(repo_root: Path) -> int:
    """Generate preview-tiny.webp for any preview.webp missing one."""
    count = 0
    for d in SCAN_DIRS:
        scan = repo_root / d
        if not scan.exists():
            continue
        for preview in scan.rglob("preview.webp"):
            tiny = preview.with_name("preview-tiny.webp")
            if tiny.exists():
                continue
            img = Image.open(preview)
            w, h = img.size
            new_w = TINY_WIDTH
            new_h = max(1, int(h * new_w / w))
            img = img.resize((new_w, new_h), Image.LANCZOS)
            img.save(tiny, "WEBP", quality=TINY_QUALITY)
            rel = tiny.relative_to(repo_root)
            print(f"  blur: {rel} ({tiny.stat().st_size} bytes)")
            count += 1
    return count


def main() -> int:
    repo_root = Path(__file__).resolve().parent
    dry_run = "--run" not in sys.argv

    targets = find_convertible(repo_root)
    if not targets and not dry_run:
        print("No images to convert.")
    elif targets:
        if dry_run:
            print("DRY RUN — pass --run to convert and delete originals\n")

        total_before = 0
        total_after = 0
        for path in targets:
            rel = path.relative_to(repo_root)
            if dry_run:
                size = path.stat().st_size
                print(f"  {rel}  ({size:,} bytes)")
            else:
                before, after = convert(path)
                total_before += before
                total_after += after
                pct = 100 * after // before if before else 0
                print(f"  {rel}: {before:,} → {after:,} ({pct}%)")
                os.remove(path)

        if not dry_run:
            saved = total_before - total_after
            print(f"\nConverted {len(targets)} image(s). Saved {saved:,} bytes.")
            print("Remember to update any .md references from .jpg/.png to .webp")
        else:
            print(f"\n{len(targets)} image(s) would be converted.")

    if not dry_run:
        count = generate_tiny_thumbnails(repo_root)
        if count:
            print(f"Generated {count} blur thumbnail(s).")
        else:
            print("All blur thumbnails up to date.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

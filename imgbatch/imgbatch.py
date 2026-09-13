#!/usr/bin/env python3
"""
imgbatch - Batch image resizer and format converter.

Convert and/or resize a whole folder of images in one command.

Examples:
    # Convert all PNGs in a folder to WebP
    python imgbatch.py photos/ --format webp

    # Resize everything to max width 1200px, keep same format
    python imgbatch.py photos/ --width 1200

    # Convert HEIC to JPG and resize to max 800x800, save into "out/"
    python imgbatch.py photos/ --format jpg --width 800 --height 800 --output out/

    # Process subfolders too
    python imgbatch.py photos/ --format webp --recursive
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Missing dependency. Install it with:\n    pip install pillow")
    sys.exit(1)

SUPPORTED_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif", ".gif", ".heic"
}


def find_images(input_dir: Path, recursive: bool):
    pattern = "**/*" if recursive else "*"
    for path in sorted(input_dir.glob(pattern)):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield path


def resize_image(img: Image.Image, max_width: int, max_height: int) -> Image.Image:
    """Resize in place, preserving aspect ratio, only shrinking (never upscaling)."""
    width, height = img.size
    target_w = max_width or width
    target_h = max_height or height

    ratio = min(target_w / width, target_h / height)
    if ratio >= 1:
        return img  # already smaller than the target, leave it alone

    new_size = (max(1, int(width * ratio)), max(1, int(height * ratio)))
    return img.resize(new_size, Image.LANCZOS)


def convert_one(path: Path, output_dir: Path, fmt: str, width: int, height: int, quality: int) -> str:
    try:
        with Image.open(path) as img:
            if width or height:
                img = resize_image(img, width, height)

            out_format = (fmt or path.suffix.lstrip(".")).lower()
            if out_format == "jpg":
                out_format = "jpeg"

            # JPEG doesn't support transparency
            if out_format == "jpeg" and img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            out_name = path.stem + "." + (fmt if fmt else path.suffix.lstrip("."))
            out_path = output_dir / out_name

            save_kwargs = {}
            if out_format in ("jpeg", "webp"):
                save_kwargs["quality"] = quality

            img.save(out_path, format=out_format.upper() if out_format != "jpeg" else "JPEG", **save_kwargs)
            return f"OK    {path.name} -> {out_path.name}"
    except Exception as e:
        return f"FAIL  {path.name} ({e})"


def main():
    parser = argparse.ArgumentParser(description="Batch resize and/or convert images.")
    parser.add_argument("input", help="Folder containing images to process")
    parser.add_argument("--output", "-o", default=None,
                         help="Output folder (default: <input>/converted)")
    parser.add_argument("--format", "-f", default=None,
                         help="Target format: jpg, png, webp, etc. (default: keep original format)")
    parser.add_argument("--width", type=int, default=None, help="Max width in pixels")
    parser.add_argument("--height", type=int, default=None, help="Max height in pixels")
    parser.add_argument("--quality", "-q", type=int, default=85,
                         help="Quality for jpg/webp output, 1-100 (default: 85)")
    parser.add_argument("--recursive", "-r", action="store_true",
                         help="Also process images in subfolders")
    args = parser.parse_args()

    input_dir = Path(args.input)
    if not input_dir.is_dir():
        print(f"Not a folder: {input_dir}")
        sys.exit(1)

    output_dir = Path(args.output) if args.output else input_dir / "converted"
    output_dir.mkdir(parents=True, exist_ok=True)

    images = list(find_images(input_dir, args.recursive))
    if not images:
        print("No supported images found in that folder.")
        sys.exit(0)

    print(f"Processing {len(images)} image(s) -> {output_dir}")
    results = [
        convert_one(p, output_dir, args.format, args.width, args.height, args.quality)
        for p in images
    ]
    for line in results:
        print(line)

    failed = sum(1 for r in results if r.startswith("FAIL"))
    print(f"\nDone. {len(results) - failed} succeeded, {failed} failed.")


if __name__ == "__main__":
    main()

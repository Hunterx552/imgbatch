# imgbatch

A simple command-line tool to batch resize and/or convert image formats — no need to open every file one by one.

Turn 200 PNGs into WebP, resize a folder of photos for the web, or convert HEIC to JPG, all in one command.

## Install

```bash
pip install pillow
```

Then download `imgbatch.py` from this repo (no other install needed).

## Usage

```bash
# Convert all images in a folder to WebP
python imgbatch.py photos/ --format webp

# Resize everything to max width 1200px (keeps aspect ratio)
python imgbatch.py photos/ --width 1200

# Convert to JPG and resize to fit inside 800x800, save into a custom folder
python imgbatch.py photos/ --format jpg --width 800 --height 800 --output out/

# Include subfolders
python imgbatch.py photos/ --format webp --recursive
```

By default, converted images are saved to `<input>/converted/` so your originals are never touched.

### Options

| Flag | Description |
|---|---|
| `--format`, `-f` | Target format: `jpg`, `png`, `webp`, etc. |
| `--width` | Max width in pixels |
| `--height` | Max height in pixels |
| `--quality`, `-q` | Output quality for jpg/webp, 1-100 (default 85) |
| `--output`, `-o` | Output folder |
| `--recursive`, `-r` | Also process subfolders |

Images are only ever shrunk, never enlarged.

## Supported formats

PNG, JPG/JPEG, WebP, BMP, TIFF, GIF, HEIC (input only for HEIC — install `pillow-heif` for HEIC support).

## Contributing

Issues and pull requests welcome.

## Support this project

If this tool saves you time, consider [sponsoring](https://github.com/sponsors/YOUR-USERNAME) to support continued development.

## License

MIT

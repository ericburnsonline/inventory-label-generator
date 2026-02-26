#!/usr/bin/env python3
"""
Make a 3" x 1" (LANDSCAPE) label image matching the reference layout.

LEFT (stacked):
  PART text
  PART barcode
  QTY text
  QTY barcode

RIGHT:
  BIN text above BIN barcode (horizontal),
  then rotate the BIN block 90° CCW and place it on the right.

Usage example:
  python make_label.py --part ADS1115 --qty 25 --bin S04
"""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter


# ============================================================
# CONFIG
# ============================================================

LABEL_W_IN = 3.0
LABEL_H_IN = 1.0
DPI = 203

ROTATE_FOR_PRINTER = False
ROTATE_FOR_PRINTER_DIR = "CW"

MARGIN_IN = 0.08

RIGHT_COL_FRAC = 0.28
COL_GAP_IN = 0.06

GAP_PART_TEXT_TO_BAR_IN = 0.03
GAP_PART_BAR_TO_QTY_TEXT_IN = 0.05
GAP_QTY_TEXT_TO_BAR_IN = 0.03

FONT_PART_SIZE = 24
FONT_QTY_SIZE = 26
FONT_BIN_SIZE = 22

PART_MODULE_WIDTH = 0.42
PART_MODULE_HEIGHT = 7.0
PART_QUIET_ZONE = 2.0

QTY_MODULE_WIDTH = 0.42
QTY_MODULE_HEIGHT = 6.0
QTY_QUIET_ZONE = 2.0

BIN_MODULE_WIDTH = 0.42
BIN_MODULE_HEIGHT = 7.0
BIN_QUIET_ZONE = 2.0

CROP_BARCODE_TO_INK = True
CROP_THRESHOLD = 250
CROP_PAD_PX = 2

BIN_ROTATE_CCW = True

MIN_MODULE_WIDTH = 0.15
MIN_QUIET_ZONE = 0.60
RETRY_ATTEMPTS = 4
RETRY_BUMP_MW = 0.02
RETRY_BUMP_QZ = 0.10

# ============================================================


def load_font(size: int, bold: bool = False):
    candidates = []
    if bold:
        candidates += [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/Library/Fonts/Arial Bold.ttf",
            "C:\\Windows\\Fonts\\arialbd.ttf",
        ]
    candidates += [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Arial.ttf",
        "C:\\Windows\\Fonts\\arial.ttf",
    ]
    for p in candidates:
        fp = Path(p)
        if fp.exists():
            return ImageFont.truetype(str(fp), size=size)
    return ImageFont.load_default()


def crop_barcode_to_ink(img_rgba, pad=2, threshold=250):
    gray = img_rgba.convert("L")
    mask = gray.point(lambda p: 255 if p < threshold else 0)
    bbox = mask.getbbox()
    if not bbox:
        return img_rgba
    x0, y0, x1, y1 = bbox
    x0 = max(0, x0 - pad)
    y0 = max(0, y0 - pad)
    x1 = min(img_rgba.width, x1 + pad)
    y1 = min(img_rgba.height, y1 + pad)
    return img_rgba.crop((x0, y0, x1, y1))


def make_code128(data, *, module_width, module_height, quiet_zone, dpi):
    data = str(data)
    mw = max(float(module_width), MIN_MODULE_WIDTH)
    qz = max(float(quiet_zone), MIN_QUIET_ZONE)
    mh = float(module_height)

    code128 = barcode.get("code128", data, writer=ImageWriter())
    last_err = None

    for _ in range(RETRY_ATTEMPTS):
        opts = {
            "module_width": mw,
            "module_height": mh,
            "quiet_zone": qz,
            "font_size": 0,
            "write_text": False,
            "dpi": int(dpi),
            "background": "white",
            "foreground": "black",
        }
        try:
            img = code128.render(opts).convert("RGBA")
            if CROP_BARCODE_TO_INK:
                img = crop_barcode_to_ink(img, CROP_PAD_PX, CROP_THRESHOLD)
            return img
        except ValueError as e:
            last_err = e
            if "x1 must be greater than or equal to x0" not in str(e):
                raise
            mw += RETRY_BUMP_MW
            qz += RETRY_BUMP_QZ

    raise RuntimeError(f"Barcode render failed: {last_err}")


def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def rotate_img(img, direction):
    return img.rotate(-90 if direction == "CW" else 90, expand=True)


def generate_label(part, qty, bin_code, out_path):
    W = int(LABEL_W_IN * DPI)
    H = int(LABEL_H_IN * DPI)

    MARGIN = int(MARGIN_IN * DPI)
    COL_GAP = int(COL_GAP_IN * DPI)

    GAP_PT_TB = int(GAP_PART_TEXT_TO_BAR_IN * DPI)
    GAP_PB_QT = int(GAP_PART_BAR_TO_QTY_TEXT_IN * DPI)
    GAP_QT_QB = int(GAP_QTY_TEXT_TO_BAR_IN * DPI)

    label = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(label)

    font_part = load_font(FONT_PART_SIZE, True)
    font_qty = load_font(FONT_QTY_SIZE, True)
    font_bin = load_font(FONT_BIN_SIZE, True)

    usable_w = W - 2 * MARGIN
    right_col_w = int(usable_w * RIGHT_COL_FRAC)
    left_col_w = usable_w - right_col_w - COL_GAP

    left_x0 = MARGIN
    right_x0 = left_x0 + left_col_w + COL_GAP

    part_text_w, part_text_h = text_size(draw, part, font_part)
    qty_text_w, qty_text_h = text_size(draw, qty, font_qty)

    bc_part = make_code128(part,
        module_width=PART_MODULE_WIDTH,
        module_height=PART_MODULE_HEIGHT,
        quiet_zone=PART_QUIET_ZONE,
        dpi=DPI)

    bc_qty = make_code128(qty,
        module_width=QTY_MODULE_WIDTH,
        module_height=QTY_MODULE_HEIGHT,
        quiet_zone=QTY_QUIET_ZONE,
        dpi=DPI)

    left_stack_h = (
        part_text_h + GAP_PT_TB + bc_part.height +
        GAP_PB_QT +
        qty_text_h + GAP_QT_QB + bc_qty.height
    )

    y = (H - left_stack_h) // 2

    draw.text((left_x0 + (left_col_w - part_text_w) // 2, y),
              part, font=font_part, fill=(0, 0, 0))
    y += part_text_h + GAP_PT_TB

    label.alpha_composite(bc_part,
        (left_x0 + (left_col_w - bc_part.width) // 2, y))
    y += bc_part.height + GAP_PB_QT

    draw.text((left_x0 + (left_col_w - qty_text_w) // 2, y),
              qty, font=font_qty, fill=(0, 0, 0))
    y += qty_text_h + GAP_QT_QB

    label.alpha_composite(bc_qty,
        (left_x0 + (left_col_w - bc_qty.width) // 2, y))

    # --- BIN block ---
    bin_text_w, bin_text_h = text_size(draw, bin_code, font_bin)

    bc_bin = make_code128(bin_code,
        module_width=BIN_MODULE_WIDTH,
        module_height=BIN_MODULE_HEIGHT,
        quiet_zone=BIN_QUIET_ZONE,
        dpi=DPI)

    bin_block_w = max(bin_text_w, bc_bin.width)
    bin_block_h = bin_text_h + int(0.02 * DPI) + bc_bin.height

    bin_block = Image.new("RGBA", (bin_block_w, bin_block_h), (255, 255, 255, 0))
    bd = ImageDraw.Draw(bin_block)

    bd.text(((bin_block_w - bin_text_w) // 2, 0),
            bin_code, font=font_bin, fill=(0, 0, 0))

    bin_block.alpha_composite(bc_bin,
        ((bin_block_w - bc_bin.width) // 2,
         bin_text_h + int(0.02 * DPI)))

    bin_block_r = bin_block.rotate(90, expand=True)

    bin_x = right_x0 + (right_col_w - bin_block_r.width) // 2
    bin_y = (H - bin_block_r.height) // 2

    label.alpha_composite(bin_block_r, (bin_x, bin_y))

    out_img = rotate_img(label, ROTATE_FOR_PRINTER_DIR) if ROTATE_FOR_PRINTER else label

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_img.convert("RGB").save(out_path, "PNG")
    print(f"Wrote: {out_path} ({out_img.width}x{out_img.height}px @ {DPI}dpi)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", required=True)
    ap.add_argument("--qty", required=True)
    ap.add_argument("--bin", default="S04")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    out = Path(args.out) if args.out else Path(f"label_{args.part}_{args.qty}.png")
    generate_label(args.part, args.qty, args.bin, out)


if __name__ == "__main__":
    main()

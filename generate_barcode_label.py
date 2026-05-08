from __future__ import annotations

from pathlib import Path
from png_renderer import save_label_image

import argparse


def generate_barcode_image(data: str, filename: str) -> Image.Image:
    code128 = barcode.get("code128", data, writer=ImageWriter())
    barcode_filename = code128.save(filename)

    return Image.open(barcode_filename)


def generate_label(part: str, qty: str, bin_code: str | None, output_file: str) -> None:
    # Create blank label (1x3 inch @ 203 DPI ≈ 203x609)
    width, height = 203, 609
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Load default font
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()

    # === PART BARCODE ===
    part_barcode = generate_barcode_image(part, "part_barcode")
    part_barcode = part_barcode.resize((160, 200))
    image.paste(part_barcode, (40, 50))

    # PART TEXT
    draw.text((10, 260), f"{part}", fill="black", font=font_large)

    # === QTY BARCODE ===
    qty_barcode = generate_barcode_image(qty, "qty_barcode")
    qty_barcode = qty_barcode.resize((140, 120))
    image.paste(qty_barcode, (30, 320))

    # QTY TEXT
    draw.text((10, 450), f"QTY {qty}", fill="black", font=font_small)

    # === BIN TEXT (optional) ===
    if bin_code:
        draw.text((10, 500), f"BIN {bin_code}", fill="black", font=font_small)

    # Save final image
    image.save(output_file)
    print(f"Saved label to: {output_file}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", required=True)
    parser.add_argument("--qty", required=True)
    parser.add_argument("--bin", required=False)
    parser.add_argument("--out", required=False)

    args = parser.parse_args()

    part = str(args.part)
    qty = str(args.qty)
    bin_code = str(args.bin) if args.bin else None

    # === AUTO FILENAME (restored behavior) ===
    if args.out:
        output_file = args.out
    else:
        filename = f"{part}_QTY{qty}"
        if bin_code:
            filename += f"_BIN{bin_code}"
        output_file = f"{filename}.png"

    save_label_image(part, qty, bin_code, Path(output_file))
    print(f"Saved label to: {output_file}")


if __name__ == "__main__":
    main()
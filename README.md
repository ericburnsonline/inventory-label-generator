# Inventory Label Generator

A practical command-line tool for generating barcode labels for physical inventory — 
part numbers, quantities, and storage bin locations. Built and actively used for 
real inventory management, vibe coded with AI assistance to move fast.

Supports two distinct workflows:

- **Single PNG label** — one label with Part, Quantity, and optional Bin location
- **Bulk ZPL batch printing** — numbered label runs sent directly to a Zebra printer

---

## How It Evolved

This tool started as a simple single-label image generator. As batch printing needs 
grew, it expanded into a full coordinator with job batching, preview support, 
dry-run mode, and direct Zebra printer output via Windows print APIs.

`generate_barcode_label.py` is the original entry point and contains some dead code 
from early development. It still works as a CLI for single labels but the rendering 
logic has since moved to `png_renderer.py`.

---

## Workflows

### Single PNG Label

Includes Part, Quantity, and optional Bin location.  
Output is a PNG file (203 DPI, 3" × 1" format).

    python generate_barcode_label.py --part SS-810-6-1 --qty 1 --bin H03

Auto-generated filename:

    SS-810-6-1_QTY1_BINH03.png

Optional explicit filename:

    python generate_barcode_label.py --part SS-810-6-1 --qty 1 --bin H03 --out label.png

---

### Bulk ZPL Batch Printing

Generates and sends numbered label runs directly to a Zebra printer.  
Includes Part and Quantity. Bin is intentionally excluded from ZPL output.

    python batch_print_zpl_labels.py --prefix SF --start 1 --count 20 --qty 1

Options:

- `--batch-size` — how many labels to send per batch (default: 10)
- `--preview-first` — save a PNG preview of the first label before printing
- `--dry-run` — walk through the full flow without sending to printer
- `--zpl-out-dir` — save individual .zpl files to a directory
- `--list-printers` — show available Windows printers
- `--printer` — specify printer name (default: ZDesigner GX430t)

---

### Generate ZPL File Only (no printer required)

    python zpl_renderer.py --prefix SF --start 1 --count 20 --qty 1 --output labels.zpl

---

## Project Structure

    label_core.py                       # LabelSpec dataclass, part number generation, batching logic
    png_renderer.py                     # Core PNG label rendering engine (Pillow + python-barcode)
    generate_barcode_label.py           # CLI for single label generation — contains dead code from early dev
    zpl_renderer.py                     # ZPL label generation for Zebra printers
    batch_print_zpl_labels.py           # Batch coordinator: preview, batching, dry-run, direct print
    printer_utils.py                    # Windows-only direct Zebra printer output via pywin32
    requirements.txt                    # Core dependencies
    requirements-windows-print.txt      # Optional Windows printing dependencies

---

## Requirements

    pip install -r requirements.txt

Core dependencies:

- pillow
- python-barcode

Optional — required for direct Windows printer output:

    pip install -r requirements-windows-print.txt

- pywin32 (Windows only)

---

## Label Format

- 3" × 1" at 203 DPI
- Left column: Part number (text + Code128 barcode), Quantity (text + barcode)
- Right column: Bin/location (text + barcode, rotated 90°) — PNG only
- ZPL labels: Part and Quantity only

---

## Notes

- Direct printer output is Windows only (`printer_utils.py`)
- PNG output works cross-platform (macOS and Linux font paths included)
- Barcode rendering includes automatic retry logic for edge cases
- Always test labels in your environment before relying on them in production

---

## Disclaimer

Provided as-is. Barcode scanning reliability varies depending on printer 
calibration, label stock, and scanner hardware.

---

## License

MIT License — Copyright (c) 2026
# Inventory Label Generator

Generate printable barcode labels for inventory using part numbers, quantities, and storage bin locations.

This tool supports:

• Single label image generation (JPG)  
• Batch ZPL file generation for Zebra printers  

---

## Demo

![Web Server Output](docs/ui-screenshot.png)

## Wiring

![Breadboard Layout](docs/breadboard.jpg)

---

## Refactor Notes

The project has been refactored to support two distinct workflows:

Image Labels (JPG)

• Includes Part, Quantity, and Bin  
• Used for one-off labels and visual inspection  
• Automatically generates filenames based on inputs (unless overridden)  

ZPL Batch Labels

• Includes Part and Quantity only  
• Optimized for fast batch printing  
• Outputs .zpl files for direct printer use  
• Bin is intentionally excluded  

---

## Features

Creates labels with the following layout:

LEFT (stacked)

• Part number text  
• Part number barcode (Code128)  
• Quantity text  
• Quantity barcode  

RIGHT (rotated)

• Bin/location text  
• Bin/location barcode  

---

## Example Usage

Create a single image label:

    python generate_barcode_label.py --part SS-810-6-1 --qty 1 --bin H03

Auto-generated filename:

• SS-810-6-1_QTY1_BINH03.jpg  

Optional explicit filename:

    python generate_barcode_label.py --part SS-810-6-1 --qty 1 --bin H03 --out label.jpg

---

Generate batch ZPL labels:

    python zpl_renderer.py --prefix SF --start 1 --count 20 --qty 1 --output labels.zpl

Generates:

• SF0001  
• SF0002  
• ...  
• SF0020  

---

## Requirements

Install dependencies:

    pip install -r requirements.txt

Typical requirements:

• pillow  
• python-barcode  

Optional Windows printing support:

    pip install -r requirements-windows-print.txt

• pywin32  

---

## Notes

• Labels are designed for 3" × 1" format  
• Image labels include Bin information  
• ZPL labels currently include Part and Quantity only  
• ZPL output is optimized for scan reliability and batch printing  

---

## Project Structure

    generate_barcode_label.py           # Single label image generation (JPG)
    zpl_renderer.py                     # Batch ZPL label generation
    batch_print_zpl_labels.py           # Batch print helper
    requirements.txt                    # Core dependencies
    requirements-windows-print.txt      # Optional Windows printing dependencies

---

## Disclaimer

This project is provided as-is with no guarantees of fitness for any specific purpose.

Barcode scanning reliability may vary depending on printer calibration, label quality, and scanner hardware.

Always test labels in your specific environment before relying on them in production workflows.

---

## License

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files to deal in the Software
without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.
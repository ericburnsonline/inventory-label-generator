# Inventory Label Generator

Generate printable barcode labels for inventory using part numbers, quantities, and optional storage bin locations.

This tool outputs a PNG image designed for 3" × 1" labels commonly used with Zebra printers.

Future versions may support direct ZPL generation and printing.

---

## Features

Creates a label with the following layout.

### When a BIN is provided

LEFT (stacked)

• Part number text  
• Part number barcode (Code128)  
• Quantity text  
• Quantity barcode  

RIGHT (rotated)

• Bin/location text  
• Bin/location barcode  

---

### When no BIN is provided

The part number and quantity information is centered on the label:

• Part number text  
• Part number barcode  
• Quantity text  
• Quantity barcode  

---

## Example Usage

### With BIN location

    python generate_barcode_label.py --part ADS1115 --qty 25 --bin S04

### Without BIN location (centered layout)

    python generate_barcode_label.py --part ADS1115 --qty 25

The script creates an image file named:

    label_<PART>_<QTY>.png

Example:

    label_ADS1115_25.png

Open the image and print it using your preferred image viewer or printer software.

---

## Requirements

Python 3.8 or newer is recommended.

Install dependencies using:

    pip install -r requirements.txt

### requirements.txt

    Pillow>=10.0
    python-barcode>=0.15

Libraries used:

- Pillow — image creation and text rendering  
- python-barcode — Code128 barcode generation  

---

## Label Specifications

Designed for:

- 3" × 1" labels (landscape orientation)
- 203 DPI thermal printers (common Zebra default)

Layout, spacing, and barcode sizing are configurable within the script.

---

## Roadmap / Planned Features

Potential future enhancements include:

- Direct ZPL output
- Printing directly to Zebra printers
- Batch generation from CSV
- Configurable layouts
- Additional barcode formats
- Automation-friendly command options

---

## Development Notes

This project was created using an AI-assisted workflow ("vibe coding") combined with manual testing and iteration on real printed labels.

All layout decisions were validated through actual printed output.

---

## Disclaimer

This software is provided "as is", without warranty of any kind.

Use at your own risk.  
The author assumes no responsibility for printing errors, hardware issues, mislabeling, or any damages resulting from use of this tool.

---

## License

Released under the MIT License.
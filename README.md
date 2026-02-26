# Inventory Label Generator

Generate printable barcode labels for inventory using part numbers, quantities, and storage bin locations.

This tool currently outputs a PNG image designed for 3" × 1" labels commonly used with Zebra printers.  
Future versions may support direct ZPL generation and printing.

---

## Features

Creates a label with the following layout:

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

```bash
python generate_barcode_label.py --part ADS1115 --qty 25 --bin S04
=======
# inventory-label-generator
Python tool for creating printable barcode labels for inventory management.

from __future__ import annotations

def generate_label_zpl(part: str, qty: str, bin_code: str | None = None) -> str:
    part = str(part)
    qty = str(qty)

    zpl = []
    
    # ^XA = Start label format
    zpl.append("^XA")
    
    # ^PW203 = Print width (in dots). 203 dots ≈ 1 inch at 203 DPI
    zpl.append("^PW203")
    
    # ^LL609 = Label length (in dots). 609 dots ≈ 3 inches
    zpl.append("^LL609")
    
    # ^LH0,0 = Label home (origin point). Sets (0,0) at top-left of label
    zpl.append("^LH0,0")
    
    # ^CI28 = Use UTF-8 character encoding
    zpl.append("^CI28")

    # =========================================================
    # COORDINATE SYSTEM (PRINTER PERSPECTIVE)
    # =========================================================
    # ^FOx,y  = Field Origin
    #   x = left → right
    #   y = top → bottom
    #
    # Your rotated view (label turned for use):
    #   +X = DOWN
    #   +Y = RIGHT
    #
    # IMPORTANT:
    # - Coordinates are ABSOLUTE (not relative)
    # - Each ^FO starts a new positioning anchor
    # =========================================================

    # =========================
    # PART TEXT (Human readable)
    # =========================
    zpl.append("^FO085,405")
    zpl.append("^A0R,44,44")
    zpl.append(f"^FD{part}^FS")

    # =========================
    # PART BARCODE
    # =========================
    zpl.append("^FO145,235")
    zpl.append("^BY4,2,200")
    zpl.append("^BCR,200,N,N,N")
    zpl.append(f"^FD{part}^FS")

    # =========================
    # QTY BARCODE
    # =========================
    #
    # Reverted back two iterations to:
    #   ^FO000,335
    #   ^BY4,2,80
    #   ^BCR,80,N,N,N
    #
    zpl.append("^FO000,335")
    zpl.append("^BY4,2,80")
    zpl.append("^BCR,80,N,N,N")
    zpl.append(f"^FD{qty}^FS")

    # =========================
    # QTY TEXT (Human readable)
    # =========================
    zpl.append("^FO030,565")
    zpl.append("^A0R,36,36")
    zpl.append(f"^FDQTY {qty}^FS")

    # ^XZ = End label format (send to printer)
    zpl.append("^XZ")

    return "\n".join(zpl)

if __name__ == "__main__":
    print("zpl_renderer.py is a helper module, not the command-line tool.")
    print()
    print("Use this instead:")
    print('  python batch_print_zpl_labels.py --list-printers')
    print('  python batch_print_zpl_labels.py --prefix SF --start 1 --count 20 --qty 1 --printer "ZDesigner GX430t"')

import platform


def list_windows_printers():
    try:
        import win32print
    except ImportError as exc:
        raise RuntimeError(
            "Windows printer support requires pywin32. "
            "Install it with: pip install -r requirements-windows-print.txt"
        ) from exc

    printers = win32print.EnumPrinters(
        win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
    )
    return [p[2] for p in printers]


def send_zpl_to_windows_printer(printer_name: str, zpl_data: str):
    if platform.system() != "Windows":
        raise RuntimeError("Direct printer output in this script currently supports Windows only.")

    try:
        import win32print
    except ImportError as exc:
        raise RuntimeError(
            "Windows printer support requires pywin32. "
            "Install it with: pip install -r requirements-windows-print.txt"
        ) from exc

    hprinter = win32print.OpenPrinter(printer_name)
    try:
        job = win32print.StartDocPrinter(hprinter, 1, ("ZPL Label Job", None, "RAW"))
        try:
            win32print.StartPagePrinter(hprinter)
            try:
                win32print.WritePrinter(hprinter, zpl_data.encode("utf-8"))
            finally:
                win32print.EndPagePrinter(hprinter)
        finally:
            win32print.EndDocPrinter(hprinter)
    finally:
        win32print.ClosePrinter(hprinter)
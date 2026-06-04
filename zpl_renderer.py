#!/usr/bin/env python3

import argparse
from pathlib import Path

from label_core import build_label_specs, chunk_items
from png_renderer import save_label_image
from zpl_renderer import generate_label_zpl
from printer_utils import list_windows_printers, send_zpl_to_windows_printer


DEFAULT_PRINTER = "ZDesigner GX430t"


def prompt_yes_no(prompt: str) -> bool:
    while True:
        answer = input(f"{prompt} [Y/n/q]: ").strip().lower()
        if answer in {"", "y", "yes"}:
            return True
        if answer in {"n", "no", "q", "quit"}:
            return False
        print("Please press Enter for yes, or enter n/q.")

def prompt_batch_action() -> str:
    while True:
        answer = input("Print next batch? [Y/n/c/q]: ").strip().lower()

        if answer == "":
            return "y"

        if answer in {"y", "n", "c", "q"}:
            return answer

        print("Please enter y, n, c, or q.")

def main():
    ap = argparse.ArgumentParser()

    # Make these optional here (we enforce manually later)
    ap.add_argument("--prefix")
    ap.add_argument("--start", type=int)
    ap.add_argument("--count", type=int)

    ap.add_argument("--digits", type=int, default=4)
    ap.add_argument("--qty", default="1")
    ap.add_argument("--bin", dest="bin_code", default=None)

    ap.add_argument("--batch-size", type=int, default=10)

    ap.add_argument("--preview-first", action="store_true")
    ap.add_argument("--preview-out", default="preview_first_label.png")

    ap.add_argument("--zpl-out-dir", default=None)

    ap.add_argument("--printer", default=DEFAULT_PRINTER)
    ap.add_argument("--list-printers", action="store_true")
    ap.add_argument("--dry-run", action="store_true")

    args = ap.parse_args()

    # ------------------------
    # LIST PRINTERS MODE
    # ------------------------
    if args.list_printers:
        printers = list_windows_printers()
        print("Available printers:")
        for p in printers:
            print(f"  {p}")
        return

    # ------------------------
    # VALIDATION
    # ------------------------
    if not args.prefix or args.start is None or args.count is None:
        ap.error("--prefix, --start, and --count are required unless using --list-printers")

    # ------------------------
    # BUILD LABELS
    # ------------------------
    specs = build_label_specs(
        prefix=args.prefix,
        start=args.start,
        count=args.count,
        digits=args.digits,
        qty=args.qty,
        bin_code=args.bin_code,
    )

    print(f"\nTotal labels: {len(specs)}")
    print(f"First: {specs[0].part}")
    print(f"Last : {specs[-1].part}")
    print(f"Qty  : {args.qty}")
    print(f"Bin  : {args.bin_code or '(none)'}")
    print(f"Batch size: {args.batch_size}")
    print(f"Printer: {args.printer}")
    print()

    # ------------------------
    # PREVIEW
    # ------------------------
    if args.preview_first:
        preview_path = Path(args.preview_out)
        save_label_image(
            specs[0].part,
            specs[0].qty,
            specs[0].bin_code,
            preview_path
        )
        print(f"Preview saved: {preview_path}")
        print()

        if not prompt_yes_no(f"Proceed after preview of {specs[0].part}?"):
            print("Cancelled.")
            return

    # ------------------------
    # BATCHING
    # ------------------------
    batches = chunk_items(specs, args.batch_size)

    zpl_dir = Path(args.zpl_out_dir) if args.zpl_out_dir else None
    if zpl_dir:
        zpl_dir.mkdir(parents=True, exist_ok=True)

    continue_all = False
    printed_count = 0

    for batch_index, batch in enumerate(batches, start=1):

        if not continue_all:
            if batch_index == 1 and not args.preview_first:
                if not prompt_yes_no("Print first batch now?"):
                    print("Cancelled.")
                    return

            elif batch_index > 1:
                action = prompt_batch_action()

                if action == "n":
                    print("Skipped batch.")
                    continue

                if action == "q":
                    print("Stopped.")
                    return

                if action == "c":
                    if prompt_yes_no("Print all remaining labels without further prompts?"):
                        continue_all = True
                    else:
                        continue

        batch_first = batch[0].part
        batch_last = batch[-1].part

        print(f"\nBatch {batch_index}: {batch_first} -> {batch_last}")

        for spec in batch:
            zpl = generate_label_zpl(spec.part, spec.qty, spec.bin_code)

            if zpl_dir:
                out_file = zpl_dir / f"{spec.part}.zpl"
                out_file.write_text(zpl, encoding="utf-8")

            if args.dry_run:
                print(f"[DRY RUN] Would print {spec.part}")
            else:
                send_zpl_to_windows_printer(args.printer, zpl)

        printed_count += len(batch)

        if printed_count < len(specs):
            next_part = specs[printed_count].part
            print(f"Printed labels {printed_count} of {len(specs)}. Next label: {next_part}")
        else:
            print(f"Printed labels {printed_count} of {len(specs)}.")

    print("\nDone.")


if __name__ == "__main__":
    main()

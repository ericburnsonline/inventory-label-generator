from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class LabelSpec:
    part: str
    qty: str = "1"
    bin_code: str | None = None


def format_part_number(prefix: str, number: int, digits: int = 4) -> str:
    prefix = str(prefix).strip()
    if not prefix:
        raise ValueError("prefix must not be empty")
    if number < 0:
        raise ValueError("number must be >= 0")
    if digits < 1:
        raise ValueError("digits must be >= 1")

    return f"{prefix}{number:0{digits}d}"


def build_part_numbers(prefix: str, start: int, count: int, digits: int = 4) -> List[str]:
    if start < 0:
        raise ValueError("start must be >= 0")
    if count < 1:
        raise ValueError("count must be >= 1")

    return [
        format_part_number(prefix, start + offset, digits)
        for offset in range(count)
    ]


def build_label_specs(
    prefix: str,
    start: int,
    count: int,
    digits: int = 4,
    qty: str = "1",
    bin_code: str | None = None,
) -> List[LabelSpec]:
    parts = build_part_numbers(prefix, start, count, digits)
    qty = str(qty).strip() or "1"
    bin_code = str(bin_code).strip() if bin_code else None

    return [
        LabelSpec(part=part, qty=qty, bin_code=bin_code)
        for part in parts
    ]


def chunk_items(items: list, batch_size: int) -> List[list]:
    if batch_size < 1:
        raise ValueError("batch_size must be >= 1")

    return [
        items[i:i + batch_size]
        for i in range(0, len(items), batch_size)
    ]
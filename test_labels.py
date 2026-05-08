import pytest
from pathlib import Path
from label_core import LabelSpec, build_part_numbers, build_label_specs
from zpl_renderer import generate_label_zpl


# ── label_core ────────────────────────────────────────────────────────────────

def test_build_part_numbers_basic():
    parts = build_part_numbers(prefix="SF", start=1, count=3)
    assert parts == ["SF0001", "SF0002", "SF0003"]


def test_build_label_specs_no_bin():
    specs = build_label_specs(prefix="SF", start=1, count=2, qty="5")
    assert len(specs) == 2
    assert specs[0].part == "SF0001"
    assert specs[0].qty == "5"
    assert specs[0].bin_code is None


# ── zpl_renderer ──────────────────────────────────────────────────────────────

def test_zpl_contains_part():
    zpl = generate_label_zpl(part="SF0001", qty="1")
    assert "SF0001" in zpl


def test_zpl_structure():
    zpl = generate_label_zpl(part="SF0001", qty="1")
    assert zpl.startswith("^XA")
    assert zpl.strip().endswith("^XZ")
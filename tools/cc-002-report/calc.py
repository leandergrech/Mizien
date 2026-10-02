#!/usr/bin/env python3
"""Compatibility entry point for the source-data arithmetic."""
from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).resolve().parents[2] / "data" / "cc-002" / "calc.py"), run_name="__main__")

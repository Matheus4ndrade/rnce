#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from rnce.cli import principal  # noqa: E402

raise SystemExit(principal(sys.argv[1:] or ["construir"]))

#!/usr/bin/env python
"""Run the lab test suite."""

from __future__ import annotations

import subprocess
import sys


if __name__ == "__main__":
    raise SystemExit(subprocess.call([sys.executable, "-m", "pytest"]))


#!/usr/bin/env python
"""Run the final qualified reproduction checks."""

from __future__ import annotations

import subprocess
import sys
from collections import Counter
from importlib.metadata import PackageNotFoundError, version

from eml_lab.table1 import TABLE1_PRIMITIVES
from eml_lab.witnesses import table1_witnesses

FINAL_VERDICT = (
    "Broad reproduction succeeded, while full dependency-chain compositional "
    "closure remains blocked for the inverse-function cluster. This is a "
    "qualified reproduction and proof-audit result, not a generic failure and "
    "not a complete pure EML proof."
)


def package_version(name: str) -> str:
    try:
        return version(name)
    except PackageNotFoundError:
        return "unavailable"


def main() -> int:
    pytest_result = subprocess.run([sys.executable, "-m", "pytest"])
    if pytest_result.returncode != 0:
        print("\nFinal reproduction check failed: pytest returned nonzero.")
        return pytest_result.returncode

    matrix_result = subprocess.run([sys.executable, "scripts/build_status_matrix.py"])
    if matrix_result.returncode != 0:
        print("\nFinal reproduction check failed: status matrix generation returned nonzero.")
        return matrix_result.returncode

    witnesses = table1_witnesses()
    counts = Counter(witness.final_status for witness in witnesses.values())
    print("\nFinal Table 1 status counts")
    print(f"total primitives: {len(TABLE1_PRIMITIVES)}")
    for status in [
        "verified",
        "reproduced-numerically",
        "partially-reproduced",
        "blocked-by-branch-semantics",
        "blocked-by-source-gap",
        "failed",
        "not-yet-tested",
    ]:
        print(f"{status}: {counts.get(status, 0)}")

    print("\nBackend package versions")
    for name in ["mpmath", "numpy", "sympy", "pytest"]:
        print(f"{name}: {package_version(name)}")

    print("\nFinal qualified verdict")
    print(FINAL_VERDICT)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

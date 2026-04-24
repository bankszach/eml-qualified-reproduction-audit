"""Domain labels used by the witness registry and tests."""

from __future__ import annotations

from enum import StrEnum


class Domain(StrEnum):
    POSITIVE_REAL = "positive-real"
    NONZERO_COMPLEX_AWAY_FROM_CUTS = "nonzero-complex-away-from-cuts"
    COMPLEX_BRANCH_SENSITIVE = "complex-branch-sensitive"
    EXTENDED_REAL = "extended-real"
    SOURCE_DEPENDENT = "source-dependent"


POSITIVE_REAL_SAMPLES = [0.125, 0.5, 1.0, 2.0, 10.0]
EDGE_NEAR_ZERO_SAMPLES = [1e-30, 1e-12, 1e-6]
COMPLEX_AWAY_FROM_CUT_SAMPLES = [
    0.5 + 0.25j,
    1.25 + 0.75j,
    2.0 - 0.5j,
    -0.5 + 0.7j,
]


# Arcosh Extended-Domain Audit

**Purpose:** Audit whether derived `arcosh` remains valid on internal domains required by later witnesses.
**Status:** Final extended-domain audit for the root inverse-cluster blocker.
**Last updated:** 2026-04-24.
**Related files:** `reports/arccos_dependency_isolation.md`, `reports/compositional_validity_audit.md`, `docs/branch_cuts.md`.

Iteration 5 checks whether the derived `arcosh` witness is safe as an internal
dependency for:

```text
arccos(x) = ArcCosh[Cos[ArcCosh[x]]]
```

## Source Chain

Author Mathematica verifier:

```text
arcCoshEML[x_] := arcSinhEML[hypotEML[I, x]]
arcCoshW[x_] := ArcSinh[Sqrt[x^2 - 1]]
checkIdentity["ArcCosh[x] witness on reals x>=1", arcCoshW[x], ArcCosh[x], {x}, x >= 1]
```

The author only checks the derived `ArcCosh` witness on `x >= 1`. The `ArcCos`
phase-2 check uses Mathematica's built-in `ArcCosh[Cos[ArcCosh[x]]]` over
`-1 <= x <= 1`; it does not prove that the derived `arcCoshEML` has principal
`ArcCosh` semantics on the interior branch-cut interval.

## Ordinary Real Domain

Samples:

```text
1.1, 1.5, 2, 10
```

Result:

| backend | classification |
| --- | --- |
| `mpmath_principal` | all exact-match |
| `mpmath_lower` | all exact-match |

The previous `arcosh` status on its ordinary calculator domain remains valid.

## Interior Branch-Cut Interval

Samples:

```text
-0.9, -0.5, -0.1, 0, 0.1, 0.5, 0.9
```

Result:

| backend | result |
| --- | --- |
| `mpmath_principal` | 3 wrong-square-root-sheet, 4 conjugation |
| `mpmath_lower` | 3 wrong-square-root-sheet, 4 exact-match |

For `mpmath_lower`, nonnegative samples in `[0,1)` match principal `acosh`.
Negative samples in `(-1,0)` choose the `acos(abs(x))` sheet instead of the
principal `acos(x)` sheet. This is the exact internal domain needed by the
`arccos` witness.

Representative `mpmath_lower` values:

| x | derived `arcosh(x)` | principal `mpmath.acosh(x)` | classification |
| --- | --- | --- | --- |
| `-0.5` | `+1.04719755119659775 i` | `+2.09439510239319549 i` | wrong-square-root-sheet |
| `0.5` | `+1.04719755119659775 i` | `+1.04719755119659775 i` | exact-match |

## Below Negative Side

Samples:

```text
-10, -2, -1.5, -1.1
```

Result:

| backend | result |
| --- | --- |
| `mpmath_principal` | all wrong-log-sheet |
| `mpmath_lower` | all wrong-log-sheet |

The derived witness returns the positive real `acosh(abs(x))` value and misses
the principal `+i*pi` sheet of `acosh(x)` below `-1`.

## Side-of-Cut Probes

Side probes were added for:

```text
x + i*eps
x - i*eps
eps = 1e-6, 1e-12, 1e-30
```

The backend can evaluate explicit upper/lower perturbations, but this does not
make the derived witness principal on the interior negative interval. The
failure is a branch-sheet mismatch in the `ArcSinh[Sqrt[x^2 - 1]]`
factorization, not merely the absence of signed zero at exactly real inputs.

## Verdict

`arcosh` stays `reproduced-numerically` for its ordinary Table 1 real
calculator domain `x > 1`, but it is **not safe as an internal principal
`arcosh` dependency for `arccos` on `(-1,1)`**.

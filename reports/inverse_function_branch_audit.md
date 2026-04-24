# Inverse Function Branch Audit

**Purpose:** Diagnose branch failures for `arccos`, `arcsin`, `artanh`, and `arctan`.
**Status:** Supporting inverse-function branch audit.
**Last updated:** 2026-04-24.
**Related files:** `reports/arccos_dependency_isolation.md`, `reports/compositional_validity_audit.md`, `docs/branch_cuts.md`.

Iteration 4 target primitives:

```text
arccos, arcsin, artanh, arctan
```

Primary author file:

```text
external/SymbolicRegressionPackage/EML_toolkit/EmL_verification/verify_eml_symbolic_chain.wl
```

The author verifier defines `LogLower` on lines 10-16 and EML on line 18. The
accepted phase-2 witnesses are on lines 70-74, and the final symbolic checks
are on lines 178-181.

## Shared Diagnosis

The four blockers are not source gaps. The Mathematica verifier asserts them
under real-domain assumptions, while the local Python dependency-chain
reproduction fails on negative real samples under both ordinary principal
`mpmath` and `mpmath_lower`.

The first failure is `arccos`. For real `x < 0`, the Python chain follows the
`acos(abs(x))` sheet. `arcsin`, `artanh`, and `arctan` then inherit sign flips
through their dependencies.

Unwinding diagnostics found no stable global additive correction:

- no consistent `2*pi*i*k` logarithmic sheet offset;
- no consistent `pi*k` offset;
- no consistent `pi/2*k` offset, except isolated coincidences such as
  `arctan(-1)`;
- the dominant failure is a sample-dependent branch-sheet mismatch.

## `arccos`

Author witness sources:

- full EML chain: `arcCosEML[x_] := arcCoshEML[cosEML[arcCoshEML[x]]]`;
- phase-2 canonical witness: `arcCosW[x_] := ArcCosh[Cos[ArcCosh[x]]]`;
- Rust run: `ArcCosh[Cos[ArcCosh[EulerGamma]]]`.

Mathematica reference:

```text
ArcCos[x], with -1 <= x <= 1
```

Dependencies:

```text
arcosh -> cos -> arcosh
```

Branch convention:

- `LogLower` is involved indirectly through EML-defined dependencies;
- the immediate failure is not fixed by changing `LogLower`;
- the failure points to the square-root/log sheet selected by `arcosh` inside
  the composed expression.

Python result:

| backend | real sample result |
| --- | --- |
| `mpmath_principal` | positive samples pass; negative samples return `acos(abs(x))` |
| `mpmath_lower` | same |

Classification:

```text
square-root-sheet-flip/composed-branch-cut
```

## `arcsin`

Author witness sources:

- full EML chain: `arcSinEML[x_] := arcCosEML[sinEML[arcCosEML[x]]]`;
- phase-2 canonical witness: `arcSinW[x_] := Pi/2 - ArcCos[x]`;
- Rust run: `Subtract[Half[Pi], ArcCos[EulerGamma]]`.

Mathematica reference:

```text
ArcSin[x], with -1 <= x <= 1
```

Dependencies:

```text
pi -> half -> arccos
```

Python result:

| backend | real sample result |
| --- | --- |
| `mpmath_principal` | positive samples pass; negative samples sign-flip |
| `mpmath_lower` | same |

Classification:

```text
inherited sign flip from arccos
```

## `artanh`

Author witness sources:

- full EML chain: `arcTanhEML[x_] := arcSinhEML[tanEML[arcSinEML[x]]]`;
- phase-2 canonical witness: `arcTanhW[x_] := ArcSinh[1/Tan[ArcCos[x]]]`;
- Rust run: `ArcSinh[Inv[Tan[ArcCos[EulerGamma]]]]`.

Mathematica reference:

```text
ArcTanh[x], with -1 < x < 1
```

Dependencies:

```text
arccos -> tan -> inv -> arsinh
```

Python result:

| backend | real sample result |
| --- | --- |
| `mpmath_principal` | positive samples pass; negative samples sign-flip |
| `mpmath_lower` | same |

Classification:

```text
inherited sign flip through tan(arccos(x))
```

## `arctan`

Author witness sources:

- full EML chain: `arcTanEML[x_] := arcSinEML[tanhEML[arcSinhEML[x]]]`;
- phase-2 canonical witness: `arcTanW[x_] := ArcSin[Tanh[ArcSinh[x]]]`;
- Rust run: `ArcSin[Tanh[ArcSinh[EulerGamma]]]`.

Mathematica reference:

```text
ArcTan[x], for real x
```

Dependencies:

```text
arsinh -> tanh -> arcsin
```

Python result:

| backend | real sample result |
| --- | --- |
| `mpmath_principal` | positive samples pass; negative samples sign-flip |
| `mpmath_lower` | same |

Classification:

```text
inherited sign flip through arcsin(tanh(arsinh(x)))
```

At `x = 0`, the direct dependency-chain evaluator also shows tiny complex
roundoff residuals. This is a numeric exactness issue, not the dominant branch
failure.

## Side-of-Cut Probes

Side probes were added for `x + i*eps` and `x - i*eps`, with:

```text
eps = 1e-6, 1e-12, 1e-30
```

For `arccos` near `x = -0.5`, upper/lower perturbations preserve conjugate
side information, but both sides remain on the wrong real sheet:

```text
actual real part   ~= acos(0.5)
expected real part ~= acos(-0.5)
```

This supports the current classification as a composed branch-sheet mismatch,
not just a lack of exact signed zero at a single point.

## Status

| primitive | source witness | principal-log result | LogLower result | branch classification | current status |
| --- | --- | --- | --- | --- | --- |
| `arccos` | extracted | blocked on negative reals | blocked on negative reals | square-root sheet flip / composed branch cut | `blocked-by-branch-semantics` |
| `arcsin` | extracted | blocked on negative reals | blocked on negative reals | inherited sign flip | `blocked-by-branch-semantics` |
| `artanh` | extracted | blocked on negative reals | blocked on negative reals | inherited sign flip | `blocked-by-branch-semantics` |
| `arctan` | extracted | blocked on negative reals | blocked on negative reals | inherited sign flip | `blocked-by-branch-semantics` |

## Minimum Next Repair Candidate

A repair should not hardcode outputs. The smallest plausible next experiment is
an author-compatible `arcosh`/square-root sheet rule for inputs generated inside
`ArcCosh[Cos[ArcCosh[x]]]`, plus regression tests showing that:

- `arcosh` still passes on real `x > 1`;
- `i`, `pi`, `sin`, `cos`, `tan`, `arsinh`, and `arcosh` Iteration 3 tests are
  unchanged;
- negative-real `arccos` moves from `acos(abs(x))` to the DLMF principal
  `acos(x)` sheet.

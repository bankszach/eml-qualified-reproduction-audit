# Branch Cuts

**Purpose:** Explain branch-cut assumptions and branch-sensitive blockers in the Table 1 audit.
**Status:** Final branch-cut reference for the qualified reproduction.
**Last updated:** 2026-04-24.
**Related files:** `docs/semantics.md`, `reports/inverse_function_branch_audit.md`, `reports/status_matrix.md`.

The principal complex logarithm is single-valued only after choosing a branch.
This lab uses the principal branch, with a cut along the negative real axis and
argument in `(-pi, pi]`.

## `ln(exp(z))` Is Not Global

For complex `z`, `Log(exp(z))` recovers `z` only modulo integer multiples of
`2*pi*i`, and the principal branch selects one representative. Therefore,
identities using `Log(exp(z)) = z` must specify a region where the imaginary
part lies in the principal strip.

## `exp(ln(z))` Is Safer

`exp(Log(z)) = z` is valid for nonzero complex `z` on the principal branch.
It still excludes `z = 0` and must handle numerical behavior near the branch
cut carefully.

## Sign Issues for `i`

The paper's handling of `i` and related constants must be audited from the SI
or code. Until then, witnesses involving square roots or inverse trigonometric
functions should record whether they select `i`, `-i`, or a branch-dependent
representative.

## Test Regions

The default complex test region avoids:

- zero;
- points near the negative real axis;
- arguments close to `pi` or `-pi`;
- overflow-sized real parts.

Dedicated branch tests intentionally sample near:

- small positive and negative real values;
- the negative real axis from above and below;
- `z` values whose imaginary parts leave the principal strip after intermediate
  transformations.

## Author Branch Convention

The author's Mathematica verification file
`external/SymbolicRegressionPackage/EML_toolkit/EmL_verification/verify_eml_symbolic_chain.wl`
defines:

```text
LogLower[z_] := Piecewise[
  {{Log[-z] - I Pi, Element[z, Reals] && z < 0}},
  Log[z]
]
```

The comment in that file describes this as the lower-edge branch on the
negative real axis, with argument in `[-Pi, Pi)`. It is not the ordinary
principal logarithm on the cut: for a negative real input it returns the value
approached from below, e.g. `LogLower[-1] = -I Pi`.

The EML in that Mathematica verification is then:

```text
EML[x_, y_] := Exp[x] - LogLower[y]
```

This is a manually adjusted branch for EML evaluation, not a blanket change to
every mathematical target. The stated purpose is to make the reconstructed
`logEML` follow the standard principal-branch target on the negative real axis.

Witnesses affected by this convention include construction of `i`, `pi`, and
all functions that depend on those constants: `cos`, `sin`, `tan`, `arcosh`,
`arccos`, `arcsin`, `artanh`, and `arctan`. The compiler file also documents a
manual sign correction for `i`, which means branch/sign handling is not uniform
across all author tools.

The local Python lab now includes `mpmath_lower_backend`, which reproduces the
negative-real `LogLower` rule numerically. This is enough for targeted numeric
experiments, but not yet a full symbolic backend. A full custom backend would
need:

- principal target functions for comparison;
- `LogLower` inside EML nodes only;
- explicit signed-zero behavior near the negative real axis;
- tests for `i`, `pi`, trigonometric, and inverse-trigonometric witnesses.

| input | principal `mpmath.log` | `LogLower` |
| --- | --- | --- |
| `-1` | `+i*pi` | `-i*pi` |
| `-1 + eps*i` | upper-edge value, positive imaginary part | same as principal |
| `-1 - eps*i` | lower-edge value, negative imaginary part | same as principal |
| `1` | `0` | `0` |
| `0` | `-inf` in mpmath extended behavior | `-inf` in mpmath extended behavior |
| `+inf` | `+inf` | `+inf` |

For dependency-chain verification the lab additionally snaps numerically tiny
imaginary parts of intended exact negative-real intermediates to the cut before
applying the selected branch. This avoids floating roundoff around
`exp(e +/- i*pi)` choosing the wrong side of the branch cut.

## Inverse-Function Branch Sheets

Iteration 4 adds a separate branch-sheet diagnostic layer for `arccos`,
`arcsin`, `artanh`, and `arctan`. These rows are compared against DLMF-style
principal real-domain references and against the author dependency-chain
witnesses recorded in the Mathematica verifier.

The author chain uses:

| primitive | author dependency-chain witness used for audit |
| --- | --- |
| `arccos` | `ArcCosh[Cos[ArcCosh[x]]]` |
| `arcsin` | `Pi/2 - ArcCos[x]` in the accepted Rust/phase-2 chain; the full EML chain also contains `ArcCos[Sin[ArcCos[x]]]` |
| `artanh` | `ArcSinh[1/Tan[ArcCos[x]]]` |
| `arctan` | `ArcSin[Tanh[ArcSinh[x]]]` |

The local Python diagnosis is:

| primitive | negative real behavior under principal `mpmath` | negative real behavior under `LogLower` | classification |
| --- | --- | --- | --- |
| `arccos` | returns the `acos(abs(x))` sheet | same real-sheet failure | square-root sheet flip / composed branch cut |
| `arcsin` | returns `-asin(x)` for `x < 0` | same sign flip | inherited from `arccos` |
| `artanh` | returns `-atanh(x)` for `x < 0` | same sign flip | inherited through `tan(arccos(x))` |
| `arctan` | returns `-atan(x)` for `x < 0` | same sign flip | inherited through `arcsin(tanh(arsinh(x)))` |

These failures are not constant additive branch offsets. The unwinding
diagnostics do not find a stable `pi*k`, `pi/2*k`, or `2*pi*i*k` correction
except for isolated samples such as `arctan(-1)`, where the sign flip happens
to equal a `pi/2` offset. For `arccos`, the error is sample-dependent and is
best classified as the wrong square-root/arcosh sheet inside a composed
expression.

Side-of-cut probes currently use `x + i*eps` and `x - i*eps` for eps values
`1e-6`, `1e-12`, and `1e-30`. The upper and lower probes preserve conjugate
side information in `mpmath`, but they do not repair the real-sheet mismatch:
for example near `x = -0.5`, the EML `arccos` dependency chain stays near
`acos(0.5)` while the principal reference stays near `acos(-0.5)`.

## Extended-Domain `arcosh`

Iteration 5 isolates the `arccos` blocker to the first internal
`arcosh(x)` call. The derived witness:

```text
arcosh(x) = arsinh(hypot(i, x))
```

corresponds in the author phase-2 check to:

```text
ArcSinh[Sqrt[x^2 - 1]]
```

The source verifier checks this witness against `ArcCosh[x]` only under
`x >= 1`. On that domain the local Python dependency chain still matches
principal `mpmath.acosh`.

The `arccos` witness, however, needs `ArcCosh[x]` on `x in (-1,1)`.
Diagnostics show:

| domain | derived `arcosh` behavior |
| --- | --- |
| `x > 1` | matches principal `acosh(x)` |
| `x in (-1,0)` | chooses the `acos(abs(x))` interior sheet |
| `x in [0,1)` under `LogLower` | matches principal `acosh(x)` |
| `x < -1` | misses the principal `+i*pi` sheet |

The direct named formula `mpmath.acosh(mpmath.cos(mpmath.acosh(x)))` matches
`mpmath.acos(x)` on the deterministic `(-1,1)` samples. The failure appears
only when the named `acosh` calls are replaced by the derived witness. This is
now the root branch blocker for `arccos`.

## Internal Principal `arcosh` Helper

Iteration 6 adds a diagnostic-only helper:

```text
principal_arcosh_internal(z) =
  Log(z + Sqrt[z - 1] * Sqrt[z + 1])
```

with mpmath principal `Log` and `Sqrt`. This matches `mpmath.acosh` on the
Iteration 5 sample sets, including explicit upper/lower side-of-cut probes.
It is not a replacement for the derived EML `arcosh` witness.

Staged results:

| arccos variant | result |
| --- | --- |
| named `acosh(cos(acosh(x)))` | matches `acos(x)` |
| fully derived dependency chain | fails on negative interior samples as `acos(abs(x))` |
| internal helper for both `acosh` calls | matches `acos(x)` diagnostically |
| internal helper only for the first `acosh` call | enough to make the staged chain pass |
| internal helper only for the final `acosh` call | not enough |

The source audit found no author rule that explicitly licenses replacing the
derived `arcosh` witness with this helper. Therefore the helper is classified
as diagnostic-only.

# Arccos Dependency Isolation

**Purpose:** Isolate named-function, derived-chain, and diagnostic-helper behavior for `arccos`.
**Status:** Final diagnostic report for the `arccos` blocker.
**Last updated:** 2026-04-24.
**Related files:** `reports/arccos_author_chain_audit.md`, `reports/arcosh_extended_domain_audit.md`, `src/eml_lab/arccos_staged_reproduction.py`.

Author witness under audit:

```text
ArcCosh[Cos[ArcCosh[x]]]
```

Samples:

```text
-0.9, -0.5, -0.1, 0, 0.1, 0.5, 0.9
```

## Direct Named-Function Formula

Test:

```text
direct_arccos_witness(x) = mpmath.acosh(mpmath.cos(mpmath.acosh(x)))
```

Reference:

```text
mpmath.acos(x)
```

Result:

```text
7 exact-match, 0 failed
```

So the named-function formula is not the blocker under `mpmath` principal
function conventions.

## Staged Dependency Tests

For each sample the diagnostic records:

```text
a = arcosh(x)
b = cos(a)
c = arcosh(b)
```

Three modes were compared:

| mode | result |
| --- | --- |
| all direct named `mpmath` functions | 7 exact-match |
| derived `arcosh`, direct `mpmath.cos`, derived `arcosh` | 4 exact-match, 3 `acos(abs(x))` sheet |
| full dependency-chain evaluator | 4 exact-match, 3 `acos(abs(x))` sheet |

The three failing samples are exactly:

```text
-0.9, -0.5, -0.1
```

## Stage Analysis

Does the first `arcosh(x)` choose the wrong sheet?

Yes. For `x in (-1,0)`, the derived `arcosh` witness chooses the
`acos(abs(x))` sheet on the interior branch cut. This differs from principal
`acosh(x)`, whose imaginary part is `acos(x)`.

Does `cos(a)` amplify or hide the sheet error?

It hides part of the sign information because `cos(i*t) = cosh(t)` and the
subsequent value becomes compatible with `abs(x)` rather than `x`.

Does the final `arcosh(b)` repair or preserve the wrong sheet?

It preserves the wrong sheet. The final result is `acos(abs(x))`, not
`acos(x)`.

Does `LogLower` help?

No. `LogLower` is necessary for the `i` sign convention, but the `arccos`
blocker remains unchanged once the derived `arcosh` is used on `(-1,0)`.

## Root Cause

The blocker is dependency-level, not formula-level:

```text
direct named formula: passes
derived arcosh dependency: fails on x in (-1,0)
full dependency chain: inherits the same failure
```

The immediate root blocker is the derived `arcosh` witness outside its verified
ordinary domain. The author source verifies `ArcSinh[Sqrt[x^2 - 1]]` only for
`x >= 1`, while the `arccos` witness needs principal `ArcCosh` behavior on
`x in (-1,1)`.

## Repair Status

No backend repair was attempted in Iteration 5. A repair would need a
source-justified, branch-aware `arcosh` helper or square-root sheet rule for
internal branch-sensitive reproduction, with regression tests for all already
reproduced branch-sensitive primitives.

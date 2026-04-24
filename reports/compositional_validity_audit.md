# Compositional Validity Audit

**Purpose:** Separate outward-domain reproduction from dependency-chain compositional closure.
**Status:** Final compositional audit for the qualified reproduction.
**Last updated:** 2026-04-24.
**Related files:** `docs/status_policy.md`, `reports/status_matrix.md`, `reports/arcosh_extended_domain_audit.md`.

Iteration 6 introduces a distinction that the status matrix alone cannot
express cleanly.

## Definitions

`outward-domain validity`:

The witness matches the intended calculator-facing function on its ordinary
domain.

`internal compositional validity`:

The witness can safely replace the named primitive inside later witnesses over
the internal domains those later witnesses require.

## Classification

Allowed statuses:

- `outward-valid`
- `compositionally-valid`
- `compositionally-unsafe`
- `source-ambiguous`
- `not-tested`

| primitive | outward-domain status | internal compositional status | reason |
| --- | --- | --- | --- |
| `arcosh` | `outward-valid` | `compositionally-unsafe` | Matches principal `acosh(x)` for real `x > 1`, but not on `(-1,0)` or `x < -1` when used as a principal `ArcCosh` substitute. |
| `arccos` | `source-ambiguous` | `compositionally-unsafe` | Named `ArcCosh[Cos[ArcCosh[x]]]` reproduces `acos(x)`, but full derived dependency-chain uses unsafe internal `arcosh`. |
| `arcsin` | `source-ambiguous` | `source-ambiguous` | Accepted witness `pi/2 - arccos(x)` is only as compositional as the `arccos` primitive it depends on. |
| `artanh` | `source-ambiguous` | `source-ambiguous` | Accepted witness depends on `arccos`; diagnostic helper chain passes, but full dependency-chain remains blocked. |
| `arctan` | `source-ambiguous` | `source-ambiguous` | Accepted witness depends on `arcsin`, which inherits from `arccos`. |
| `cos` | `outward-valid` | `compositionally-valid` on tested real/helper paths | Used inside `arccos`; replacing direct `cos` with derived `cos` does not cause the observed blocker once the first internal `arcosh` is principal. |
| `sin` | `outward-valid` | `source-ambiguous` for inverse chains | Used by the full EML `arcSinEML` variant, but the accepted phase-2/Rust `arcsin` witness uses `pi/2 - arccos(x)`. |
| `tan` | `outward-valid` | `source-ambiguous` for `artanh` | `artanh` depends on `tan(arccos(x))`; observed blocker enters before `tan`. |
| `arsinh` | `outward-valid` | `compositionally-valid` on tested real/helper paths | Used by `arcosh`, `artanh`, and `arctan`; no independent failure found in Iterations 4-6. |
| `tanh` | `outward-valid` | `compositionally-valid` on tested real/helper paths | Used by `arctan`; no independent failure found once `arcsin` is supplied by the diagnostic helper path. |

## Consequence

The remaining gap is not a missing witness and not a failure of the named
identity. It is a compositional semantics gap:

```text
derived arcosh is outward-valid on x > 1
derived arcosh is compositionally-unsafe as principal ArcCosh on (-1,1)
```

The `principal_arcosh_internal` helper is therefore diagnostic-only unless a
future source audit finds an author rule justifying that internal branch
substitution.

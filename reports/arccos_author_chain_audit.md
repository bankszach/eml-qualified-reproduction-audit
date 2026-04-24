# Arccos Author Chain Audit

**Purpose:** Determine whether the author source proves derived-`arcosh` substitution inside `arccos`.
**Status:** Final inverse-cluster source-chain audit.
**Last updated:** 2026-04-24.
**Related files:** `reports/arcosh_extended_domain_audit.md`, `reports/arccos_dependency_isolation.md`, `reports/compositional_validity_audit.md`.

Iteration 6 question:

```text
Does the author prove compositional substitutability of the derived arcosh
witness inside arccos, or only a named-function identity?
```

## Sources Inspected

- `sources/SupplementaryInformation.pdf`, especially Section 1.2 and Table S2.
- `external/SymbolicRegressionPackage/EML_toolkit/EmL_verification/verify_eml_symbolic_chain.wl`.
- `external/SymbolicRegressionPackage/rust_verify/verify_eml_symbolic_chain.wl`.
- Adjacent logs including `rust_verify.log` and `mathematica_verify.log`.

## What The Mathematica Verification Does

The Mathematica file defines the full EML-level chain:

```text
arcCoshEML[x_] := arcSinhEML[hypotEML[I, x]]
arcCosEML[x_] := arcCoshEML[cosEML[arcCoshEML[x]]]
```

But the symbolic proof section explicitly switches to phase-2 canonical forms:

```text
(* Phase-2 witness checks using already-proved canonical forms
   (prevents expression blow-up). *)
arcCoshW[x_] := ArcSinh[Sqrt[x^2 - 1]]
arcCosW[x_] := ArcCosh[Cos[ArcCosh[x]]]
```

The final checks are:

```text
checkIdentity["ArcCosh[x] witness on reals x>=1",
  arcCoshW[x], ArcCosh[x], {x}, x >= 1]

checkIdentity["ArcCos[x] witness on reals |x|<=1",
  arcCosW[x], ArcCos[x], {x}, -1 <= x <= 1]
```

Thus the author verifies `ArcCos` using Mathematica's named `ArcCosh`, not by
substituting the previously derived `arcCoshW[x] := ArcSinh[Sqrt[x^2 - 1]]`
into both internal `ArcCosh` occurrences.

## Answers To Required Questions

1. Does the author verify `ArcCosh[Cos[ArcCosh[x]]]` using Mathematica's built-in `ArcCosh`?

Yes. `arcCosW[x_] := ArcCosh[Cos[ArcCosh[x]]]` uses named Mathematica
`ArcCosh` in both positions.

2. Does the author verify it using the previously derived EML `arcosh` witness?

Not in the phase-2 proof check. The full EML-level definition exists, but the
symbolic verification section uses canonical named forms to avoid expression
blow-up.

3. Does the proof substitute the derived `arcosh` witness into the `arccos` witness?

No source inspected shows that substitution for the final `ArcCos` proof.
The checked `arcCoshW` is proved only on `x >= 1`, while `arcCosW` needs
`ArcCosh` on `x in [-1,1]`.

4. Are there assumptions?

Yes:

- `ArcCosh` witness: real `x` and `x >= 1`;
- `ArcCos` witness: real `x` and `-1 <= x <= 1`.

5. Are there replacement rules for `ArcCosh`, `Sqrt`, `Log`, or `LogLower`?

The file defines `LogLower` for EML nodes. It does not define a replacement
rule that maps internal named `ArcCosh` calls in `arcCosW` to the derived
`arcCoshW` witness, nor a branch rule that repairs `ArcSinh[Sqrt[x^2 - 1]]`
on `(-1,1)`.

6. Does Mathematica simplify this identity because of built-in inverse-function knowledge?

The source evidence points that way. The proof invokes `FullSimplify` on the
named-function identity under real assumptions. It does not demonstrate that
the derived witness is compositionally valid on the internal branch interval.

7. Is the proof showing outward equality only, or full compositional substitutability?

It shows outward equality of each phase-2 witness on its stated real domain.
For `arcosh`, that domain is `x >= 1`. It does not show full compositional
substitutability of the derived `arcosh` witness inside the later `arccos`
witness on `x in (-1,1)`.

## Proof-Type Classification

| proof type | status for `arccos` |
| --- | --- |
| named-function proof | present: `ArcCosh[Cos[ArcCosh[x]]] == ArcCos[x]` |
| derived-witness proof | not shown for internal `arcosh` substitution |
| fully expanded EML proof | not shown in inspected source |
| Mathematica simplification proof | present for named-function phase-2 identity |
| numerical reproduction proof | named/staged helper passes; fully derived Python chain fails on `x in (-1,0)` |

## Iteration 6 Verdict

The author chain supports staged named-function reproduction of `arccos`, but
the inspected source does not justify replacing the internal named `ArcCosh`
with the derived `arcosh` witness across the branch interval needed by
`arccos`.

# Final Status Policy

**Purpose:** Define final statuses and reproduction layers for the qualified audit.
**Status:** Final policy.
**Last updated:** 2026-04-24.
**Related files:** `reports/status_matrix.md`, `reports/reproduction_report.md`, `reports/final_proof_risks.md`.

This lab uses final statuses for Table 1 reproduction, not for unrestricted
mathematical truth. A row can be numerically reproduced on its stated
calculator-facing domain while still carrying proof risk when fully expanded or
composed into later witnesses.

## Status Values

`verified`

: The witness is source-supported, has explicit assumptions, and is checked by
  symbolic or direct identity tests in the lab's semantics. This status is used
  only when the tested claim is narrow enough that the source and local checks
  justify it.

`reproduced-numerically`

: The source witness is present and deterministic numerical tests match the
  intended Table 1 primitive on the documented sample domain and backend
  semantics. This is reproduction evidence, not a proof that every fully
  expanded EML expression is branch-safe everywhere.

`partially-reproduced`

: Some source-supported or staged paths reproduce the intended primitive, but a
  relevant edge case, fully expanded path, or dependency-chain substitution is
  still unresolved. Diagnostic-helper success may justify this status when the
  helper explains the observed behavior, but it does not close the proof.

`blocked-by-branch-semantics`

: The source witness is present, but local reproduction depends on complex
  branch choices, side-of-cut behavior, signed-zero semantics, or square-root
  and logarithm sheet conventions that the current source chain does not make
  explicit enough for compositional closure.

`blocked-by-source-gap`

: The lab lacks a source witness, derivation, or author-chain reference needed
  to audit the row. This is distinct from a branch-semantics blocker where the
  witness exists but its branch behavior is not compositional.

`failed`

: The source-supported witness is tested under its stated semantics and does
  not reproduce the intended primitive, with no branch/source qualification that
  explains the mismatch.

`not-yet-tested`

: A row has not yet received a local numerical or symbolic test for the
  relevant status column.

## Reproduction Layers

Named-function reproduction means the author-level formula passes when written
with named backend functions such as Mathematica `ArcCosh` or Python
`mpmath.acosh`.

Dependency-chain reproduction means each named dependency is replaced by the
source witness registered for that dependency, but not necessarily expanded all
the way to raw EML.

Staged diagnostic-helper reproduction means an internal helper reproduces the
named-function behavior in a controlled experiment. It is diagnostic evidence,
not a source-derived EML witness.

Fully expanded EML reproduction means the witness is expanded down to the
allowed terminal/operator basis and still reproduces the primitive under
documented backend semantics.

Mathematica/source-chain proof means the claim is justified by the inspected
author Mathematica or SI chain. Python/mpmath numerical reproduction is local
numerical evidence and must not be treated as a substitute for source-chain
proof.

## Outward-Domain Reproduction

Outward-domain reproduction means a witness matches the intended Table 1
primitive on its ordinary calculator-facing domain.

Example: `arcosh(x)` matches principal `acosh(x)` for real `x > 1`.

Outward-domain reproduction can justify `reproduced-numerically` for the
primitive's Table 1 calculator role, but it does not automatically prove that
the same witness is safe inside another witness.

## Compositional Reproduction

Compositional reproduction means a witness remains valid when substituted into
later witnesses across the internal domains required by those later witnesses.

Example: using the derived `arcosh(x)` witness inside
`ArcCosh[Cos[ArcCosh[x]]]` requires principal `ArcCosh` behavior for
`x in (-1, 1)`, not only outward `x > 1` behavior.

The inverse-function cluster is currently blocked at this layer: the derived
`arcosh` witness is outward-valid for `x > 1` but compositionally unsafe as the
internal principal `ArcCosh` needed by `arccos` on negative real samples.

## Diagnostic-Helper Reproduction

Diagnostic-helper reproduction means a staged helper reproduces the named
principal-function behavior but is not proven to be the derived EML witness.

Diagnostic-helper success may support `partially-reproduced` because it
localizes the branch issue and demonstrates that the named formula itself is
reproducible. It does not justify full dependency-chain closure, fully expanded
EML closure, or `verified` status.

Source-ambiguous branch repair must not be counted as verified. A helper can
explain why Mathematica's named-function proof passes while the derived witness
fails, but it cannot replace the source-derived witness without source-justified
branch rules, fully expanded symbolic verification, or a new witness set.

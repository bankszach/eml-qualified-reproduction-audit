# Future Work

**Purpose:** Scope possible next work after the qualified reproduction audit.
**Status:** Future-project guidance; no items here were started in this frozen audit snapshot.
**Last updated:** 2026-04-24.
**Related files:** `reports/final_proof_risks.md`, `reports/compositional_validity_audit.md`, `docs/status_policy.md`.

This repository is frozen as the `v0.1-qualified-reproduction` audit snapshot.
The items below are separate-project directions, not work to continue inside
this release line except for minor documentation corrections.

## Proof Closure Work

- In a separate project line, build a pure EML expansion verifier that expands
  SI witnesses down to the EML operator and the terminal `1`, with explicit
  branch annotations.
- In a separate project line, formalize branch semantics for the
  inverse-function cluster.
- Identify source-justified branch rules only in a new proof-closure project,
  not by changing this snapshot's final statuses.

## Alternate Witness Search

- Search for alternate inverse-function witnesses in a separate repository or
  explicitly separate project line.
- Keep any alternate search separate from the current witness registry until it
  has source or proof justification.

## Branch-Semantics Formalization

- Formalize branch semantics in a separate project with an explicit
  Riemann-sheet or side-of-cut model rather than relying only on backend
  principal-function defaults.
- Specify how signed zero, exact branch cuts, and limiting side probes should
  be represented.

## Backend Comparison

- Compare Mathematica, mpmath, SymPy, NumPy, and the Rust verifier in a
  separate backend-comparison project using the same branch-sensitive witness
  corpus.
- Record whether each backend supports the branch and side-of-cut semantics
  needed by the proof claim.

## Pure EML Expansion

- Build a pure EML expression expander in a separate project line that
  preserves dependency provenance and branch annotations.
- Use the expander to distinguish dependency-chain success from fully expanded
  EML success.

## Compiler-Path Audit

- Audit compiler/formula paths in a separate project line, keeping them
  distinct from the discovery-chain witness registry preserved in this
  snapshot.
- Source inspection should distinguish discovery-chain witnesses from
  compiler/formula paths.

## Author Communication

- Contact or open an issue with the paper author, presenting the derived
  `arcosh` compositional gap and the diagnostic named-function reproduction.
- Ask whether the intended proof relies on named Mathematica branches, an
  unstated branch rule, or an alternate witness set.
- This repository does not quote or paraphrase private correspondence. Claims
  in this repository are grounded in the paper, SI, archived source files, and
  executable tests.

## Symbolic Regression

- Symbolic regression is explicitly deferred.
- Symbolic-regression experiments should happen only in a separate repository
  or explicitly separate project line after proof semantics are resolved or the
  qualified reproduction status is accepted as the intended stopping point.

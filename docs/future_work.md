# Future Work

**Purpose:** Scope possible next work after the qualified reproduction audit.
**Status:** Final future-work memo; no items here were started in this audit phase.
**Last updated:** 2026-04-24.
**Related files:** `reports/final_proof_risks.md`, `reports/compositional_validity_audit.md`, `docs/status_policy.md`.

## Proof Closure Work

- Fully expand and verify all SI witnesses down to the EML operator and the
  terminal `1`, with explicit branch annotations.
- Prove or reject full dependency-chain compositional closure for the
  inverse-function cluster.
- Identify source-justified branch rules if the current witness set is kept.

## Alternate Witness Search

- Search for alternate inverse-function witnesses that avoid unsafe `arcosh`
  composition inside the `arccos` chain.
- Keep any alternate search separate from the current witness registry until it
  has source or proof justification.

## Branch-Semantics Formalization

- Formalize branch semantics with an explicit Riemann-sheet or side-of-cut
  model rather than relying only on backend principal-function defaults.
- Specify how signed zero, exact branch cuts, and limiting side probes should
  be represented.

## Backend Comparison

- Compare Mathematica, mpmath, SymPy, NumPy, and the Rust verifier on the same
  branch-sensitive witness corpus.
- Record whether each backend supports the branch and side-of-cut semantics
  needed by the proof claim.

## Pure EML Expansion

- Build a pure EML expression expander that preserves dependency provenance and
  branch annotations.
- Use the expander to distinguish dependency-chain success from fully expanded
  EML success.

## Author Communication

- Contact or open an issue with the paper author, presenting the derived
  `arcosh` compositional gap and the diagnostic named-function reproduction.
- Ask whether the intended proof relies on named Mathematica branches, an
  unstated branch rule, or an alternate witness set.

## Symbolic Regression

- Symbolic regression is explicitly deferred.
- Do not begin symbolic-regression experiments until proof semantics are closed
  or the qualified reproduction status is explicitly accepted as the intended
  stopping point.

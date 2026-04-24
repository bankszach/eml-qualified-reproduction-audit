# Final Audit Index

**Purpose:** Central landing page for the completed EML Table 1 audit.
**Status:** Final audit index.
**Last updated:** 2026-04-24.
**Related files:** `README.md`, `reports/reproduction_report.md`, `reports/status_matrix.md`.

This is the central landing page for the completed EML Table 1 audit. The
scientific result is a qualified reproduction: broad reproduction succeeded,
while full dependency-chain compositional closure remains blocked for the
inverse-function cluster.

## Recommended Reading Order

1. `README.md`
2. `FINAL_AUDIT_INDEX.md`
3. `reports/reproduction_report.md`
4. `reports/status_matrix.md`
5. `reports/final_proof_risks.md`
6. `reports/compositional_validity_audit.md`
7. `docs/branch_cuts.md` and `docs/semantics.md`

## Main Reports

- `reports/reproduction_report.md`: final qualified reproduction verdict,
  final counts, environment metadata, and iteration history.
- `reports/status_matrix.md`: generated Table 1 matrix with per-primitive
  status, branch risk, compositional notes, and final status counts.
- `reports/final_proof_risks.md`: concise list of the seven proof risks that
  remain after the audit.
- `reports/compositional_validity_audit.md`: explains outward-domain validity
  versus internal compositional validity.

## Inverse-Function Branch Audits

- `reports/arccos_author_chain_audit.md`: checks whether the author proves
  derived-`arcosh` substitution inside `arccos`.
- `reports/arcosh_extended_domain_audit.md`: shows that derived `arcosh` is
  outward-valid but unsafe on internal branch domains.
- `reports/arccos_dependency_isolation.md`: isolates where the `arccos`
  dependency chain diverges from the named principal identity.

## Policy And Semantics

- `docs/status_policy.md`: status definitions and reproduction layer policy.
- `docs/branch_cuts.md`: branch-cut assumptions and inverse-function blocker
  summary.
- `docs/semantics.md`: local numerical semantics, backends, branch conventions,
  and extended-real caveats.
- `docs/future_work.md`: scoped future directions after the qualified audit.

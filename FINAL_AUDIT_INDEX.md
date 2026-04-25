# Final Audit Index

**Purpose:** Public reading guide for the completed EML Table 1 qualified audit.
**Status:** Final audit index.
**Last updated:** 2026-04-24.
**Related files:** `README.md`, `AUTHOR_NOTE.md`, `reports/reproduction_report.md`,
`reports/status_matrix.md`, `PROOF_SNAPSHOT.md`.

This index is the map for readers who want to understand the completed audit
without reading the repository in file-system order. The scientific result is
a qualified reproduction: broad reproduction succeeded, while full
dependency-chain compositional closure remains blocked for the inverse-function
cluster.

This repository is intended to be read as a stable audit snapshot for the
canonical release `v0.1-qualified-reproduction`. Future proof work, alternate
witness searches, compiler-path audits, backend comparisons, and symbolic
regression experiments should proceed in separate repositories or explicitly
separate project lines.

## Start Here

Start with [`README.md`](README.md) for the public summary, final counts, and
the central branch-semantics question. Read
[`PROOF_SNAPSHOT.md`](PROOF_SNAPSHOT.md) for the frozen release state. Then read
[`reports/reproduction_report.md`](reports/reproduction_report.md) for the
full audit narrative and final verdict.

Recommended reading order:

1. [`README.md`](README.md)
2. [`PROOF_SNAPSHOT.md`](PROOF_SNAPSHOT.md)
3. [`AUTHOR_NOTE.md`](AUTHOR_NOTE.md)
4. [`reports/reproduction_report.md`](reports/reproduction_report.md)
5. [`reports/status_matrix.md`](reports/status_matrix.md)
6. [`reports/final_proof_risks.md`](reports/final_proof_risks.md)
7. [`reports/compositional_validity_audit.md`](reports/compositional_validity_audit.md)
8. [`docs/branch_cuts.md`](docs/branch_cuts.md)
9. [`docs/future_work.md`](docs/future_work.md)

## If You Are The Paper Author

- [`AUTHOR_NOTE.md`](AUTHOR_NOTE.md) is the concise note explaining what
  reproduced, what remains qualified, and the exact question being asked.
- [`reports/compositional_validity_audit.md`](reports/compositional_validity_audit.md)
  isolates the outward-domain versus internal-composition distinction.
- [`reports/arccos_author_chain_audit.md`](reports/arccos_author_chain_audit.md)
  records the source-chain question around the `arcosh` -> `arccos`
  dependency.

## If You Want To Reproduce The Audit

- [`README.md`](README.md) contains the basic `uv` commands.
- [`scripts/final_reproduction_check.py`](scripts/final_reproduction_check.py)
  runs the final test/check harness.
- [`scripts/build_status_matrix.py`](scripts/build_status_matrix.py)
  regenerates the status matrix.
- [`reports/status_matrix.md`](reports/status_matrix.md) shows the final
  per-primitive status counts.
- [`sources/manifest.md`](sources/manifest.md) records archived source
  artifacts used for traceability.

## If You Want The Technical Branch Issue

- [`reports/compositional_validity_audit.md`](reports/compositional_validity_audit.md)
  defines outward-domain validity and internal compositional validity.
- [`docs/branch_cuts.md`](docs/branch_cuts.md) explains the branch conventions
  and inverse-function blocker.
- [`reports/arcosh_extended_domain_audit.md`](reports/arcosh_extended_domain_audit.md)
  shows why the derived `arcosh` witness is outward-valid but unsafe as an
  internal principal `ArcCosh` substitute.
- [`reports/arccos_dependency_isolation.md`](reports/arccos_dependency_isolation.md)
  isolates where the `arccos` dependency chain diverges from the named
  principal identity.

## If You Want Future Work

- [`docs/future_work.md`](docs/future_work.md) lists scoped next steps.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) explains how to preserve the audit's
  status distinctions.
- [`docs/github_publication_notes.md`](docs/github_publication_notes.md)
  contains suggested GitHub metadata and release notes.

## Main Reports

- [`reports/reproduction_report.md`](reports/reproduction_report.md): final
  qualified reproduction verdict, counts, environment metadata, and audit
  chronology.
- [`reports/status_matrix.md`](reports/status_matrix.md): generated Table 1
  matrix with per-primitive status, branch risk, compositional notes, and final
  counts.
- [`reports/final_proof_risks.md`](reports/final_proof_risks.md): concise list
  of proof risks that remain after the audit.
- [`reports/compositional_validity_audit.md`](reports/compositional_validity_audit.md):
  outward-domain reproduction versus internal compositional validity.

## Policy And Semantics

- [`docs/status_policy.md`](docs/status_policy.md): status definitions and
  reproduction layer policy.
- [`docs/branch_cuts.md`](docs/branch_cuts.md): branch-cut assumptions and
  inverse-function blocker summary.
- [`docs/semantics.md`](docs/semantics.md): local numerical semantics,
  backends, branch conventions, and extended-real caveats.
- [`docs/future_work.md`](docs/future_work.md): scoped future directions after
  the qualified audit.

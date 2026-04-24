# Repository Map

**Purpose:** Orient new readers to the completed qualified audit repository.
**Status:** Final navigation aid.
**Last updated:** 2026-04-24.
**Related files:** `README.md`, `FINAL_AUDIT_INDEX.md`, `docs/reproducibility.md`.

## Major Directories

- `src/eml_lab/`: EML AST, witness registry, numerical evaluators, branch
  diagnostics, and staged inverse-function reproduction helpers.
- `tests/`: pytest coverage for core identities, witness registry integrity,
  numerical reproduction, branch diagnostics, and diagnostic-helper guardrails.
- `docs/`: audit policy, semantics, branch-cut notes, reproducibility, future
  work, and planning/history notes.
- `reports/`: final and intermediate audit reports, including the status
  matrix and inverse-function branch investigations.
- `scripts/`: reproducibility scripts for source bootstrapping, status matrix
  generation, and final checks.
- `sources/`: archived source artifacts used for audit traceability.
- `external/`: unmodified author repository and related external code.
- `notebooks/`: exploratory notebooks from source audit, core identity checks,
  Table 1 reproduction, and branch-cut experiments.

## Key Source Files

- `src/eml_lab/ast.py`: local expression tree and RPN support for EML terms.
- `src/eml_lab/core.py`: baseline `eml(x, y)` implementation.
- `src/eml_lab/table1.py`: machine-readable Table 1 primitive list.
- `src/eml_lab/witnesses.py`: source witness registry and final status
  metadata.
- `src/eml_lab/branch_verification.py`: branch-aware dependency-chain
  evaluator.
- `src/eml_lab/internal_branches.py`: diagnostic-only internal branch helpers;
  not verified witness implementations.
- `src/eml_lab/arccos_staged_reproduction.py`: staged `arccos` variants used
  to isolate named-function, derived-chain, and diagnostic-helper behavior.
- `src/eml_lab/arcosh_branch_diagnostics.py`: extended-domain diagnostics for
  the derived `arcosh` witness.
- `src/eml_lab/inverse_branch_diagnostics.py`: diagnostic classifications for
  `arccos`, `arcsin`, `artanh`, and `arctan`.
- `src/eml_lab/unwinding.py`: utilities for classifying branch-sheet offsets.
- `src/eml_lab/verification.py`: numerical verification helpers.
- `src/eml_lab/backends/`: mpmath, NumPy, SymPy, and LogLower backend support.

## Key Tests

- `tests/test_core_identities.py`: first EML identity checks.
- `tests/test_witness_registry.py`: Table 1 registry coverage and controlled
  status values.
- `tests/test_numeric_verification.py`: numerical reproduction harness checks.
- `tests/test_branch_sensitive_witnesses.py`: branch-aware reproduction checks.
- `tests/test_arcosh_extended_domain.py`: outward versus internal `arcosh`
  behavior.
- `tests/test_arccos_staged_reproduction.py`: named, derived, and diagnostic
  `arccos` reproduction variants.
- `tests/test_internal_arcosh_helper.py`: guardrails ensuring diagnostic
  helpers are not treated as verified witnesses.

## Key Documentation And Reports

- `README.md`: public entry point and result summary.
- `FINAL_AUDIT_INDEX.md`: central index for the completed audit.
- `docs/status_policy.md`: status and reproduction-layer definitions.
- `docs/reproducibility.md`: setup and command guide.
- `docs/future_work.md`: scoped future directions.
- `reports/reproduction_report.md`: final verdict and chronological audit
  record.
- `reports/status_matrix.md`: generated primitive status matrix.
- `reports/final_proof_risks.md`: final proof-risk memo.
- `reports/compositional_validity_audit.md`: outward versus compositional
  validity audit.
- `reports/arccos_author_chain_audit.md`: author-chain analysis for `arccos`.
- `reports/arcosh_extended_domain_audit.md`: derived `arcosh` internal-domain
  analysis.
- `reports/arccos_dependency_isolation.md`: staged dependency isolation for
  `arccos`.

## Key Scripts

- `scripts/final_reproduction_check.py`: runs tests, regenerates the status
  matrix, prints final counts, and prints the final verdict.
- `scripts/build_status_matrix.py`: regenerates `reports/status_matrix.md`
  from the witness registry.
- `scripts/bootstrap_sources.py`: fetches and records source artifacts.
- `scripts/run_all_tests.py`: legacy helper for running the test suite.

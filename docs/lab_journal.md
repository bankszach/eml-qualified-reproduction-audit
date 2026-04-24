# Lab Journal

**Purpose:** Chronological notes from the audit iterations.
**Status:** Historical working log; final conclusions are in `reports/reproduction_report.md`.
**Last updated:** 2026-04-24.
**Related files:** `reports/reproduction_report.md`, `reports/status_matrix.md`, `FINAL_AUDIT_INDEX.md`.

## 2026-04-24

Initial scaffold created for the EML qualified reproduction audit.

Implemented:

- backend-dispatched `eml`;
- EML AST with RPN parser/serializer;
- first witness registry rows;
- positive-real numerical verification for `exp` and `ln`;
- semantic and branch-cut documentation.

Open:

- parse Table 1 from the paper/SI;
- locate complete witness list in author sources;
- attempt Rust verifier build;
- add NumPy cross-check status to the generated matrix.

Update:

- Source bootstrap fetched the main paper, arXiv e-print, extracted SI, Zenodo
  v1.0 snapshot, GitHub repo, and two related 2026 arXiv follow-up PDFs.
- `cargo build` succeeds in `external/SymbolicRegressionPackage/rust_verify`.
- Captured the author Rust verifier run in `reports/author_rust_verify_run.md`;
  the run reports all default target sets cleared in about 71 seconds, but also
  reports `EulerGamma` and `Glaisher` as loaded constants, so that behavior
  needs auditing before using it as the pure constant-1 reproduction result.

## 2026-04-24 Iteration 2

Implemented:

- exact 36-row Table 1 registry in `src/eml_lab/table1.py`;
- witness registry rows for every Table 1 primitive plus support `zero`;
- dependency-chain witnesses from SI Table S2 and author Mathematica chain;
- expansion utility for core/arithmetic witnesses;
- `mpmath_lower_backend` for the author `LogLower` convention;
- arithmetic-spine and expansion tests.

Results:

- `uv run pytest`: 40 passed;
- Table 1 rows registered: 36;
- dependency-chain witnesses: 36;
- missing source witnesses: 0;
- branch-blocked rows: 11;
- Rust verifier constant behavior documented in `reports/rust_constant_audit.md`.

## 2026-04-24 Iteration 3

Implemented:

- branch-aware dependency-chain evaluator in `src/eml_lab/branch_verification.py`;
- direct LogLower backend tests;
- branch-sensitive witness tests for principal `mpmath`, `mpmath_lower`, and a
  practical NumPy principal subset;
- witness metadata for branch statuses and safe domains;
- status matrix columns for principal-log, LogLower, and NumPy statuses.

Results:

- `uv run pytest`: 51 passed;
- `mpmath_lower` reproduces `i`, `pi`, `cos`, `sin`, `tan`, `arsinh`, and
  `arcosh` on the tested real domains;
- principal log sign-flips the `i` witness;
- `arccos`, `arcsin`, `artanh`, and `arctan` remain branch-blocked on negative
  real samples.

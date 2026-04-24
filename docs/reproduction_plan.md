# Reproduction Plan

**Purpose:** Historical plan for source acquisition and Table 1 reproduction.
**Status:** Superseded by the completed final audit reports; retained for traceability.
**Last updated:** 2026-04-24.
**Related files:** `docs/reproducibility.md`, `sources/manifest.md`, `reports/reproduction_report.md`.

## Source Audit

Fetch and record:

- arXiv paper v2 PDF;
- arXiv e-print/ancillary bundle;
- supplementary information PDF if separate inside the bundle or linked page;
- Zenodo software snapshot;
- GitHub repository `VA00/SymbolicRegressionPackage`;
- follow-up EML papers relevant to hardware or neuro-symbolic claims.

## Author Code

The external repository is cloned into `external/SymbolicRegressionPackage` and
kept unmodified. The lab records:

- commit hash;
- available directories and tools;
- whether `EML_toolkit` runs;
- whether `rust_verify` builds;
- where full witness formulas appear.

## Local Verification

The baseline repository must run without Mathematica. Any Mathematica-only
verification is documented separately and must not block the Python baseline.

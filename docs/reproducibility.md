# Reproducibility

**Purpose:** Record the commands and environment expectations for reproducing
the final qualified audit checks.
**Status:** Final operational guide.
**Last updated:** 2026-04-24.
**Related files:** `README.md`, `scripts/final_reproduction_check.py`,
`reports/status_matrix.md`, `sources/manifest.md`.

## Environment

- Python: `>=3.11`
- Dependency manager: `uv`
- Baseline reproduction: no Mathematica required
- Internet access: not required for tests once sources are present locally

## Setup

```bash
uv sync
```

## Test Suite

```bash
uv run pytest
```

Expected final result:

```text
92 passed
```

## Final Check

```bash
uv run python scripts/final_reproduction_check.py
```

This command runs the full test suite, regenerates the status matrix, prints
final Table 1 status counts, prints backend package versions, and prints the
final qualified verdict. It exits nonzero if pytest or matrix generation fails.

## Regenerate Status Matrix

```bash
uv run python scripts/build_status_matrix.py
```

The matrix is generated from `src/eml_lab/witnesses.py`; edit the registry or
the generator instead of hand-editing generated rows.

## External Sources

The author repository and archived source files are stored under `external/`
and `sources/`. They are included for traceability and inspection. The baseline
test suite does not require redownloading them or running Mathematica.

Use `scripts/bootstrap_sources.py` only when rebuilding the source archive from
scratch:

```bash
uv run python scripts/bootstrap_sources.py
```

## Known Limitations

- The result is a qualified reproduction, not full pure EML proof closure.
- The inverse-function cluster remains blocked at the compositional
  branch-semantics layer.
- Diagnostic helpers reproduce staged named-principal behavior but are not
  source-derived EML witnesses.
- Fully expanded expressions may still expose extended-real or backend-specific
  behavior such as `log(0)`.

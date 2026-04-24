# Research Question

**Purpose:** State the narrow scientific question audited by this repo.
**Status:** Final scope statement with historical milestone notes.
**Last updated:** 2026-04-24.
**Related files:** `README.md`, `docs/status_policy.md`, `reports/reproduction_report.md`.

Can the operator

```text
eml(x, y) = exp(x) - log(y)
```

together with the constant `1`, construct the concrete scientific-calculator
basis listed in Table 1 of arXiv:2603.21852v2?

This lab does not attempt to prove a broader informal claim that every possible
elementary expression in every convention is available. It audits the paper's
specific basis, witnesses, semantics, and reproduction artifacts.

## Milestone 1 Scope

The first milestone verifies:

- `e = eml(1, 1)`
- `exp(x) = eml(x, 1)`
- `ln(x) = eml(1, eml(eml(1, x), 1))` on positive real inputs

The remaining Table 1 rows are source-audit targets until the SI and author
repository are parsed.

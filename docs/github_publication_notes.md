# GitHub Publication Notes

## Repository Description

```text
Independent qualified reproduction audit of the EML single-operator elementary-functions paper, with explicit branch-semantics diagnostics.
```

## Topics

```text
symbolic-computation
elementary-functions
branch-cuts
complex-analysis
computer-algebra
reproducibility
proof-audit
mathematics
python
mpmath
```

## Short Pinned-Repo Description

```text
A reproducible audit of the EML single-operator claim: broad Table 1 reproduction succeeds, with a qualified inverse-function branch-semantics gap.
```

## Release

Tag:

```text
v0.1-qualified-reproduction
```

Title:

```text
Qualified Reproduction Audit v0.1
```

Release notes:

```text
This release freezes the repository as a completed qualified reproduction/proof-audit of the EML Table 1 construction.
```

Final status:

- 36 / 36 Table 1 primitives registered.
- 92 tests passing.
- 6 verified.
- 22 reproduced numerically.
- 5 partially reproduced.
- 3 blocked by branch semantics.
- 0 source gaps.
- 0 failed.
- 0 untested.

Final verdict:

```text
Broad reproduction succeeded, while full dependency-chain compositional closure remains blocked for the inverse-function cluster. This is a qualified reproduction and proof-audit result, not a generic failure and not a complete pure EML proof.
```

This release does not include further proof work, alternate witness search,
symbolic regression experiments, or private correspondence. Future work should
proceed in a separate repository or explicitly separate project line.

Recommended reading order:

```text
1. README.md
2. PROOF_SNAPSHOT.md
3. FINAL_AUDIT_INDEX.md
4. reports/reproduction_report.md
5. reports/status_matrix.md
6. reports/final_proof_risks.md
7. reports/compositional_validity_audit.md
8. docs/future_work.md
```

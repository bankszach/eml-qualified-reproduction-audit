# Proof Strategy

**Purpose:** Outline the constructive proof strategy and verification levels used by the lab.
**Status:** Historical strategy note; final qualification is recorded in the reports.
**Last updated:** 2026-04-24.
**Related files:** `docs/status_policy.md`, `reports/compositional_validity_audit.md`, `reports/final_proof_risks.md`.

The proof spine is constructive:

```text
EML + 1 -> e -> exp -> ln -> subtraction -> arithmetic -> powers/logs
-> complex constants -> trigonometric and hyperbolic functions
```

Each step must provide either a pure EML expression, a dependency-chain
expression using earlier verified primitives, or a source gap.

Verification levels:

1. Symbolic sanity checks under explicit assumptions.
2. High-precision `mpmath` testing over declared domains.
3. Cross-backend checks with NumPy and, later, optional PyTorch.
4. External reproduction against author code, including Rust verifier if it
   builds cleanly.

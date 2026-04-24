# Final Proof Risks

**Purpose:** Summarize proof risks that remain after the qualified reproduction.
**Status:** Final proof-risk memo.
**Last updated:** 2026-04-24.
**Related files:** `reports/reproduction_report.md`, `reports/compositional_validity_audit.md`, `docs/future_work.md`.

1. Branch conventions are not incidental. The EML witnesses use complex
   intermediates, logarithms, square roots, `i`, and `pi`, so branch choices are
   central to the proof claim.

2. Named-function identities do not automatically prove derived-witness
   compositional substitution. The `arccos` identity passes with named
   `ArcCosh`, but that does not prove the derived `arcosh` witness can replace
   every internal `ArcCosh`.

3. A primitive can be outward-valid but compositionally unsafe. The derived
   `arcosh` witness reproduces principal `acosh(x)` for real `x > 1`, yet fails
   as an internal principal `ArcCosh` dependency for `arccos` on negative real
   samples.

4. Mathematica simplification may prove a named identity without proving the
   fully expanded EML witness. The inspected source supports the staged
   named-function proof, not a full substitution proof for the inverse-function
   cluster.

5. The Rust verifier is useful evidence but not a literal clean `{1, EML}`
   proof in this lab's audit sense because of probe constants and
   implementation behavior recorded in the Rust constant audit.

6. Extended-real behavior remains an implementation concern for fully expanded
   expressions. Some arithmetic constructions can pass through `log(0)` when
   fully inlined, even when dependency-chain formulas are numerically stable on
   ordinary samples.

7. Full pure EML closure requires one of the following: source-justified branch
   rules, fully expanded symbolic verification, or an alternate witness set
   that avoids the unsafe internal branch.

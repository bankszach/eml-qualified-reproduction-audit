# Proof Snapshot

This repository is frozen as a completed qualified reproduction audit of the
EML Table 1 construction.

Canonical release:

```text
v0.1-qualified-reproduction
```

## Final Audit State

- 36 / 36 Table 1 primitives registered.
- 92 tests passing.
- No missing source witnesses.
- No untested rows.
- Broad reproduction succeeded.
- The inverse-function branch-semantics qualification remains.

Final Table 1 counts:

```text
total primitives: 36
verified: 6
reproduced-numerically: 22
partially-reproduced: 5
blocked-by-branch-semantics: 3
blocked-by-source-gap: 0
failed: 0
not-yet-tested: 0
```

Final verdict:

```text
Broad reproduction succeeded, while full dependency-chain compositional closure remains blocked for the inverse-function cluster. This is a qualified reproduction and proof-audit result, not a generic failure and not a complete pure EML proof.
```

## Snapshot Boundary

Future work should happen in a separate repository or explicitly separate
project line. This repository should receive only minor documentation
corrections after this snapshot, not new proof work, witness changes, branch
closure attempts, alternate witness searches, or symbolic-regression
experiments.

This repository does not quote or paraphrase private correspondence. Claims in
this repository are grounded in the paper, supplementary information, archived
source files, and executable tests.

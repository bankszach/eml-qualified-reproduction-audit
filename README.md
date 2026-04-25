# EML Qualified Reproduction Audit

This is an independent reproduction and proof-audit repository for Andrzej
Odrzywolek's paper ["All elementary functions from a single binary operator"](https://arxiv.org/abs/2603.21852),
which claims that the operator

```text
eml(x, y) = exp(x) - ln(y)
```

together with the constant `1`, can generate a scientific-calculator basis.
The audit focuses on the paper's concrete Table 1 construction and asks what
can be reproduced numerically, what is source-supported, and where branch
semantics must be made explicit.

## Repository Status / Proof Snapshot

This repository is a frozen qualified reproduction/proof-audit snapshot. The
canonical release is `v0.1-qualified-reproduction`, summarized in
[`PROOF_SNAPSHOT.md`](PROOF_SNAPSHOT.md). Future work belongs in a separate
repository or explicitly separate project line.

This repository audits the paper's Table 1 scientific-calculator basis. It is
not a full pure EML proof, not a refutation, and not an unrestricted claim
about all elementary functions. Private correspondence is not quoted or used
as public evidence; claims here are grounded in the paper, supplementary
information, archived source files, and executable tests.

## Relationship To The Original Paper

This repository audits the Table 1 claim from the paper using the paper PDF,
supplementary information, author repository, and archived source artifacts
recorded in [`sources/manifest.md`](sources/manifest.md). It is independent
and unofficial. It is intended to be useful to the original author, publisher,
and technically interested readers, but it does not claim to replace the
author's proof or speak for the author.

## Current Result

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

Broad reproduction succeeded, while full dependency-chain compositional
closure remains blocked for the inverse-function cluster. This is a qualified
reproduction and proof-audit result, not a generic failure and not a complete
pure EML proof.

## Plain-Language Result

Most of the constructive chain reproduced cleanly under explicit numerical
semantics. All 36 Table 1 primitives were registered, no source witnesses are
missing, and no rows remain untested. The remaining issue is not an absent
formula or a numerical collapse; it is a compositional branch-semantics gap in
the inverse-function cluster.

In practical terms, the audit found broad outward-domain reproduction of the
calculator-facing primitives, while identifying one place where substituting a
derived witness into a later witness changes the internal branch behavior.

## The Main Qualified Finding

The derived `arcosh` witness is outward-valid for real `x > 1`. However, it is
not compositionally safe as an internal principal `ArcCosh` substitute inside
the `arccos` witness over `(-1, 1)`.

The author source verifies `arccos` using the named Mathematica expression
`ArcCosh[Cos[ArcCosh[x]]]`. This audit did not find source evidence that the
derived `arcosh` witness was substituted into that identity across the internal
branch domains required by the later `arccos` witness. A diagnostic internal
helper reproduces the staged named-principal behavior, but that helper is
diagnostic-only and is not counted as proof of pure dependency-chain closure.

## What This Repo Does Not Claim

- This is not presented as an adversarial critique of the paper.
- This is not a full pure EML proof.
- This does not claim unrestricted generation of "all elementary functions"
  beyond the paper's Table 1 scientific-calculator basis.
- Diagnostic helpers are not counted as proof paths.
- Symbolic regression is out of scope for this audit phase.
- Private correspondence is not quoted, paraphrased, or used as public
  evidence.

## How To Run

```bash
uv sync
uv run pytest
uv run python scripts/final_reproduction_check.py
uv run python scripts/build_status_matrix.py
```

The baseline audit does not require Mathematica or internet access after the
archived sources are present.

## Where To Read More

- [`FINAL_AUDIT_INDEX.md`](FINAL_AUDIT_INDEX.md): public reading guide for the audit.
- [`PROOF_SNAPSHOT.md`](PROOF_SNAPSHOT.md): frozen release-state summary.
- [`AUTHOR_NOTE.md`](AUTHOR_NOTE.md): concise note intended for the paper author.
- [`reports/reproduction_report.md`](reports/reproduction_report.md): final qualified reproduction report.
- [`reports/status_matrix.md`](reports/status_matrix.md): per-primitive status matrix.
- [`reports/final_proof_risks.md`](reports/final_proof_risks.md): remaining proof risks.
- [`reports/compositional_validity_audit.md`](reports/compositional_validity_audit.md): outward validity versus compositional validity.
- [`docs/status_policy.md`](docs/status_policy.md): status definitions.
- [`docs/branch_cuts.md`](docs/branch_cuts.md): branch-cut assumptions and diagnostics.
- [`docs/future_work.md`](docs/future_work.md): scoped future work.

## Open Question For The Author/Community

Are discovered primitives intended to be compositionally substituted into later
witnesses across all internal branch domains required by those later witnesses,
or only to reproduce the named primitive on its outward calculator-facing
domain?

This question arises specifically from the `arcosh` -> `arccos` dependency.

## Future Work

- Establish a source-justified branch rule for dependency-chain substitution.
- Search for alternate witnesses for the inverse-function cluster.
- Produce a full pure EML expansion with branch annotations.
- Compare Mathematica, mpmath, SymPy, NumPy, and Rust backend behavior.
- Incorporate author feedback or pointers to missed source rules.
- Defer symbolic regression until proof semantics are resolved or the current
  qualified status is accepted as the intended stopping point.

These items are future-project directions, not work started in this frozen
audit snapshot.

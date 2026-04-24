# eml-proof-lab

This repository is a proof, reproduction, and audit laboratory for Andrzej
Odrzywolek's paper "All elementary functions from a single binary operator"
(`arXiv:2603.21852v2`). It audits the paper's concrete Table 1
scientific-calculator basis from the binary Exp-Minus-Log operator and reports
a qualified reproduction: broad reproduction succeeded, while full
dependency-chain compositional closure remains blocked for the inverse-function
cluster.

## Current Result

The repo currently supports a qualified reproduction of the paper's Table 1
claim. All 36 Table 1 primitives are registered, no source witnesses are
missing, and no rows remain untested. The result is not a failed reproduction
and not a complete pure EML proof.

## What Is EML?

EML is the binary operation:

```text
eml(x, y) = exp(x) - log(y)
```

The audited construction starts from this operator and the distinguished
terminal `1`. The repo tests the paper's specific scientific-calculator basis;
it does not claim unrestricted generation of every informal meaning of
"elementary function."

## What Was Audited?

The audit checks the paper's Table 1 primitives against witnesses from the
paper, supplementary information, and author code. It separates named-function
reproduction, dependency-chain reproduction, diagnostic-helper reproduction,
fully expanded EML reproduction, Mathematica/source-chain evidence, and
Python/mpmath numerical evidence.

## Final Status Counts

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

## Main Qualified Finding

The core EML identities and most arithmetic, exponential/logarithmic, trig,
hyperbolic, and derived rows reproduce under explicit numerical semantics. The
remaining issue is compositional branch semantics in the inverse-function
cluster. The derived `arcosh` witness is outward-valid for real `x > 1`, but
is not compositionally safe as the internal principal `ArcCosh` needed by the
`arccos` witness on `(-1, 1)`.

The diagnostic internal helper reproduces staged named-principal `acosh`
behavior, but it is not a replacement for the derived EML `arcosh` witness and
does not prove pure dependency-chain closure.

## How To Run

```bash
uv sync
uv run pytest
uv run python scripts/final_reproduction_check.py
uv run python scripts/build_status_matrix.py
```

The baseline reproduction does not require Mathematica or internet access.

## Where To Read The Reports

- `FINAL_AUDIT_INDEX.md`: central index for the completed audit.
- `reports/reproduction_report.md`: final qualified verdict and iteration
  history.
- `reports/status_matrix.md`: Table 1 status matrix.
- `reports/final_proof_risks.md`: proof risks that remain after reproduction.
- `docs/status_policy.md`: definitions for final statuses and reproduction
  layers.

## Repository Map

See `docs/repo_map.md` for a concise map of directories and important files.

## What This Repo Does Not Claim

- It does not claim full pure EML compositional closure for the
  inverse-function cluster.
- It does not count diagnostic-helper paths as verified EML witnesses.
- It does not hide branch ambiguity behind a generic failure label.
- It does not claim all elementary functions in an unrestricted mathematical
  sense.
- It does not include symbolic regression in this audit phase.

## Future Work

Future work should focus on proof closure: source-justified branch rules,
fully expanded symbolic verification, alternate inverse-function witnesses, or
formal branch-semantics modeling. Symbolic regression is explicitly deferred
until proof semantics are closed or the qualified status is accepted as the
intended stopping point.

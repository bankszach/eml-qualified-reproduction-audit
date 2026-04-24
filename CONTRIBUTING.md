# Contributing

This repository is an audit of a specific paper claim, not a general EML
project. Contributions should preserve the audit trail, status distinctions,
and source provenance.

Please follow these rules:

- Preserve the distinction between `verified`, `reproduced-numerically`,
  `partially-reproduced`, and `blocked-by-branch-semantics`.
- Do not mark diagnostic helpers as proof paths.
- Do not change witnesses without source justification or a clearly separated
  alternate-witness proposal.
- New tests should specify backend, branch convention, domain assumptions, and
  expected behavior.
- Keep symbolic-regression work in future branches or separate experiments,
  not in the main audit line.
- If a change affects final counts, explain exactly why and update the
  associated report policy before treating the change as accepted.

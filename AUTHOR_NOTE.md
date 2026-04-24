# Author Note

Thank you for the paper and for making source materials available. This
repository is an independent reproduction and proof-audit attempt for the EML
Table 1 scientific-calculator basis claim.

## What Reproduced

The audit reproduced the core EML identities and registered all Table 1
primitives. No Table 1 primitive is missing a source witness, and no row
remains untested. Most primitives reproduced numerically under explicit
semantics, including the arithmetic, exponential/logarithmic, trigonometric,
hyperbolic, and most derived rows.

## What Remains Qualified

The remaining qualification is in the inverse-function branch cluster. The
root issue is that the derived `arcosh` witness is outward-valid on real
`x > 1`, but it is not compositionally safe as an internal principal
`ArcCosh` substitute inside the `arccos` witness on `(-1, 1)`.

## Precise Question

Are discovered primitives intended to be compositionally substituted into later
witnesses across all internal branch domains required by those later
witnesses, or only to reproduce the named primitive on its outward
calculator-facing domain?

This question arises specifically from the `arcosh` -> `arccos` dependency.

## Clarifications Welcome

Corrections, clarifications, or pointers to source rules I missed would be
very welcome. In particular, any intended branch-substitution rule or alternate
inverse-function witness would directly address the remaining qualification.

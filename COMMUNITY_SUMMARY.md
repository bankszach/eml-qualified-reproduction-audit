# Community Summary

## What EML Is

EML is the binary operation

```text
eml(x, y) = exp(x) - ln(y)
```

The audited paper studies whether this single operation, together with the
constant `1`, can construct a scientific-calculator basis of elementary
functions.

## Why The Paper Is Interesting

The claim is mathematically and computationally interesting because it turns a
large family of constants and functions into a bootstrapping problem from one
binary operator. That has implications for symbolic computation, expression
search, proof checking, and compact representations of calculator-like
function sets.

## What The Audit Did

This repository collected the paper, supplementary information, author code,
and archived sources, then registered the paper's Table 1 primitives and tested
their witnesses under explicit numerical and branch semantics. It separates
ordinary outward-domain reproduction from full dependency-chain substitution.

## What Reproduced

All 36 Table 1 primitives were registered. No source witness is missing and no
row remains untested. The final status matrix reports:

```text
verified: 6
reproduced-numerically: 22
partially-reproduced: 5
blocked-by-branch-semantics: 3
blocked-by-source-gap: 0
failed: 0
not-yet-tested: 0
```

This is broad reproduction of the paper's constructive chain, not a failed
reproduction.

## Why Branch Cuts Matter

Complex functions such as `ln`, square root, inverse hyperbolic functions, and
inverse trigonometric functions are multi-valued until a branch convention is
chosen. A witness can reproduce a function on the ordinary calculator-facing
domain but still behave differently when substituted inside a later witness
that calls it on another internal domain.

That is the remaining issue here. The derived `arcosh` witness reproduces
principal `acosh(x)` for real `x > 1`, but it is not safe as the internal
principal `ArcCosh` needed by the `arccos` witness on `(-1, 1)`.

## What Remains Unresolved

The unresolved question is whether the proof intends discovered primitives to
be substituted compositionally across all internal branch domains, or whether
the construction only requires outward-domain reproduction of each named
primitive. The answer determines whether the inverse-function cluster is fully
closed or remains a qualified reproduction.

## Why This Is Useful

The audit narrows the issue to a specific dependency and branch-semantics
question. It preserves the successful reproduction results, avoids treating a
branch ambiguity as a generic failure, and gives future work a concrete target.

## How Others Can Contribute

Useful contributions include source-justified branch rules, alternate
inverse-function witnesses, backend comparisons, explicit branch annotations
for pure EML expansion, and careful tests that state their branch assumptions.
Symbolic-regression work should wait until the proof semantics are resolved or
the qualified status is accepted as the intended stopping point.

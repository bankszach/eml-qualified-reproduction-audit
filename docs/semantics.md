# Semantics

**Purpose:** Define local numerical semantics, branch conventions, and backend distinctions.
**Status:** Final semantics reference for the qualified audit.
**Last updated:** 2026-04-24.
**Related files:** `docs/branch_cuts.md`, `docs/status_policy.md`, `reports/status_matrix.md`.

## Domain of `eml`

The local baseline semantics are complex-valued:

```text
eml(x, y) = exp(x) - Log(y)
```

where `Log` is the principal complex logarithm. The operator is undefined at
`y = 0` in ordinary complex arithmetic, but some numerical systems represent
`log(0)` using extended values such as `-inf`. This lab records those cases as
extended-real or backend-dependent, not as ordinary complex equalities.

## Value Space

The proof harness uses these value regimes:

- positive real numbers, used for the first `ln`, multiplication, division, and
  power sanity checks;
- complex numbers away from branch cuts, used for later trigonometric and
  hyperbolic checks;
- edge-adjacent samples near zero and the negative real axis, used to expose
  branch and extended-value behavior;
- backend-specific finite precision values in NumPy.

## Logarithm Branch

The baseline branch is the principal complex logarithm with argument in
`(-pi, pi]`. This is the branch used by `mpmath`, `numpy` complex arrays, and
SymPy's principal `log` in ordinary symbolic expressions.

## Negative Real Inputs

For negative real `x`, principal `Log(x)` has imaginary part `pi`. Identities
that use log laws such as `Log(a*b) = Log(a) + Log(b)` or
`Log(exp(z)) = z` are not accepted globally. They need domain restrictions or
explicit branch accounting.

## Zero, Infinity, NaN, and Signed Zero

The baseline proof domain excludes `Log(0)`. Backend observations are still
recorded because the paper discusses special values such as `log(0) = -inf`.

- `mpmath.log(0)` can return an infinite value in some contexts.
- NumPy complex `log(0)` yields infinities and warnings rather than a normal
  finite complex value.
- NaN from a backend is treated as invalid for strict evaluation.
- Signed zero behavior is backend-specific and will be tested separately before
  any status depends on it.

## Positive-Real Claims

The milestone-1 `ln` witness is marked verified only on `x > 0`. On that
domain:

```text
eml(1, eml(eml(1, x), 1))
= e - Log(exp(e - Log(x)))
= e - (e - Log(x))
= Log(x)
```

The step `Log(exp(e - Log(x))) = e - Log(x)` is safe there because
`e - log(x)` is real.

## Complex Intermediate Values

Future witnesses for trigonometric functions, inverse trigonometric functions,
and constants such as `i` and `pi` are expected to require complex
intermediate values. Those witnesses will be tested over regions that avoid
the negative real branch cut unless the test intentionally probes it.

## Backend Dependence

The lab distinguishes:

- symbolic status: what SymPy can simplify under stated assumptions;
- `mpmath` status: high-precision numerical behavior;
- NumPy status: practical complex finite-precision behavior;
- external status: author Rust verifier or Mathematica-dependent results.

No result should be promoted from `not-yet-tested` to `verified` merely because
one backend agrees on random samples.

## Author Branch Convention

The author's Mathematica verification does not use the plain principal
logarithm inside the EML node. It defines `LogLower`, which agrees with
ordinary `Log` except on negative real inputs, where it returns the lower-edge
value `Log[-z] - I*pi`. Thus `LogLower[-1] = -I*pi`.

The local baseline remains principal-log `mpmath` unless a test explicitly asks
for `backend="mpmath_lower"` or imports `mpmath_lower_backend`. This custom
backend is a numeric reproduction of the author convention, not a proof
assistant. Branch-sensitive witnesses are therefore not marked verified merely
because the backend exists.

Consequences:

- the `ln` witness is verified locally on positive reals;
- real arithmetic witnesses are tested first on branch-safe positive samples;
- `i`, `pi`, trig functions, and inverse trig functions stay
  branch-specific until the branch convention is tested through their full
  dependency chains;
- fully inlined sign-flip formulas can encounter `log(0)` and are tracked as
  extended-real risks.

Iteration 3 found that the author branch convention is reproducible in Python
for `i`, `pi`, real-domain `sin`, `cos`, `tan`, `arsinh`, and `arcosh` using
direct dependency-chain witnesses. The inverse-trigonometric chain for
`arccos`, `arcsin`, `artanh`, and `arctan` remains blocked on negative real
samples in the local Python reproduction and must not be promoted to verified.

## Iteration 4 Branch-Sheet Classification

The lab now distinguishes algebraic failure from branch-sheet disagreement.
For the four inverse-function blockers, the executable semantics are:

- `mpmath_principal`: ordinary principal `mpmath.log` inside EML;
- `mpmath_lower`: author `LogLower` inside EML only;
- DLMF/A&S principal reference: direct `mpmath.acos`, `asin`, `atanh`, and
  `atan` on the stated real calculator domains;
- Mathematica/source-chain result: the author Mathematica verifier assertions,
  not automatically identified with Python behavior.

On deterministic real samples, `arccos` is the first branch-sheet mismatch:
for `x < 0`, the Python dependency chain returns the `acos(abs(x))` sheet. The
other three blockers inherit this as a sign flip on negative real samples.
This is not repaired by `LogLower`, which only changes the logarithm value on
exact negative real inputs inside EML nodes. The remaining gap is therefore a
composed inverse-function branch problem involving `arcosh`, `sqrt`, and
side-of-cut semantics, not a missing source witness.

The local backend can represent upper/lower perturbations with small imaginary
parts, but exact IEEE signed-zero semantics are not treated as a formal proof
object. Any witness that requires signed zero at exactly real cut points must
remain at most `partially-reproduced` until a backend with explicit signed-zero
rules is added.

## Extended-Domain Dependency Semantics

Iteration 5 adds a rule for interpreting dependency-chain results: a witness
verified on its ordinary calculator domain is not automatically valid as an
internal dependency on a larger branch-sensitive domain.

The concrete case is `arcosh`. The derived witness is numerically reproduced
for real `x > 1`, which is its ordinary real-valued calculator domain. The
`arccos` witness nevertheless applies `arcosh` to `x in (-1,1)`. On this
extended internal domain, the derived witness does not have principal
`mpmath.acosh` semantics for negative inputs:

- for `x in (-1,0)`, it follows the `acos(abs(x))` sheet;
- for `x < -1`, it misses the principal `+i*pi` sheet;
- `LogLower` does not repair the `(-1,0)` mismatch.

Therefore, the current `arccos` blocker is dependency-level. The named formula
`acosh(cos(acosh(x)))` is valid under direct principal `mpmath` functions on
the tested real interval, but the repo's derived `arcosh` dependency is not a
drop-in principal `acosh` there.

## Outward vs Internal Validity

Iteration 6 separates two validity notions:

- outward-domain validity: a witness matches the user-facing calculator
  function on the function's ordinary real domain;
- internal compositional validity: the witness remains a valid substitute
  when used inside later witnesses on the internal domains those later
  witnesses require.

The `arcosh` witness is outward-valid for real `x > 1`. It is
compositionally unsafe as an internal principal `ArcCosh` replacement for
`arccos`, because `arccos` needs `ArcCosh` on `x in (-1,1)`.

The diagnostic `principal_arcosh_internal` helper matches principal
`mpmath.acosh`, and staged `arccos` passes when the first internal `arcosh`
call uses that helper. This is not promoted to full proof because the author
source inspected so far verifies the `arccos` phase-2 identity using named
Mathematica `ArcCosh`, not by substituting the derived EML `arcosh` witness
into the identity.

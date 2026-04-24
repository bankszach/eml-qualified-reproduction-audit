# Rust Constant Audit

**Purpose:** Explain why the Rust verifier output is useful but not a clean `{1, EML}` proof by itself.
**Status:** Supporting audit report.
**Last updated:** 2026-04-24.
**Related files:** `reports/author_rust_verify_run.md`, `reports/final_proof_risks.md`, `external/SymbolicRegressionPackage/rust_verify/`.

## Summary

The Rust verifier result is useful, but the captured command should not be
treated as a clean formal proof that only `{1, EML}` were available as terminal
construction symbols.

The SI Table S2 caption states that the probe constants gamma
(Euler-Mascheroni) and A (Glaisher-Kinkelin) are available as test inputs but
are not part of the construction. The Rust implementation partly reflects that
intent, because unary and binary target witnesses are printed as expressions
over `EulerGamma` and `Glaisher`, i.e. placeholders for `x` and `y`. However,
the code also unconditionally inserts those names into the `known_constants`
list used by the search/enumeration machinery.

## Where They Are Loaded

In `external/SymbolicRegressionPackage/rust_verify/src/main.rs`:

- lines 961-977 define the constant catalog, including `Glaisher`,
  `EulerGamma`, `Catalan`, and `Khinchin`;
- lines 1499-1505 build target probe expressions such as
  `Exp[EulerGamma]` and `Subtract[EulerGamma, Glaisher]`;
- lines 1513-1525 define probe sample pairs using EulerGamma, Catalan,
  Glaisher, and Khinchin with sign-reflected variants;
- lines 1968-1969 unconditionally initialize `known_constants` with
  `Glaisher` and `EulerGamma`, then extend it with `--constants`.

## Are They Construction Terminals?

Ambiguous in the implementation.

Conceptually, for unary and binary witness validation they are probe symbols
standing for `x` and `y`. That matches SI Table S2, which says they are test
inputs and not construction primitives.

Operationally, the Rust search state stores them in `known_constants`, and the
generator receives `known_constants` when enumerating expressions. That means a
strict code audit cannot say `--constants 1` removes them from all construction
leaves.

## Does `--constants 1` Restrict the Basis to Constant 1?

Not literally in the current Rust code. The captured run prints:

```text
Loaded base constants: ["1", "EulerGamma", "Glaisher"]
```

This comes from the unconditional initialization at lines 1968-1969. The CLI
option restricts the user-supplied constants, but not the verifier's built-in
probe placeholders.

## What the Verifier Proves or Searches

The Rust verifier performs numeric enumeration/search and witness validation
over a target set. It discovers candidate witnesses, rejects flaky candidates
using additional probe points, and can call a high-precision Python checker.
It is not a formal proof assistant.

The captured run is best interpreted as:

- strong evidence that the Table 1 chain can be reconstructed by the author's
  bootstrapping procedure;
- a source of witness expressions and discovery order;
- not, by itself, a pure terminal-set proof independent of the SI/Mathematica
  chain and local verification.

## Cleanest Available Command

The cleanest available command remains explicit about targets and should still
be audited for probe placeholders:

```bash
cargo run -- \
  --constants 1 \
  --functions '' \
  --operations EML \
  --target-constants Pi,E,-1,2 \
  --target-functions Exp,Log,Inv,Half,Minus,Sqrt,Sqr,LogisticSigmoid,Sin,Cos,Tan,ArcSin,ArcCos,ArcTan,Sinh,Cosh,Tanh,ArcSinh,ArcCosh,ArcTanh \
  --target-operations Plus,Subtract,Times,Divide,Log,Power,Avg,Hypot \
  --max-k 10 \
  --explain
```

This excludes `EulerGamma` and `Glaisher` from the target constants, but it does
not remove their internal role as probe placeholders unless the source is
patched or a separate verifier is written.

## What To Trust

Trust:

- Table S2 witness order and readable dependency-chain witnesses;
- the flaky-witness warnings;
- the fact that the author code has explicit multi-point numerical safeguards;
- the Mathematica verification file as a source of branch conventions.

Keep independently testing:

- pure EML expansion without probe constants as terminals;
- branch-sensitive constants `i` and `pi`;
- all trig and inverse-trig witnesses under the exact `LogLower` semantics;
- extended-real cases involving `log(0)`.

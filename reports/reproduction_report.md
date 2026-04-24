# Reproduction Report

**Purpose:** Present the final qualified reproduction verdict and audit chronology.
**Status:** Final report.
**Last updated:** 2026-04-24.
**Related files:** `reports/status_matrix.md`, `reports/final_proof_risks.md`, `FINAL_AUDIT_INDEX.md`.

## Final qualified reproduction verdict

As of 2026-04-24, this lab supports a qualified reproduction of the paper's
Table 1 scientific-calculator basis, not a full pure dependency-chain proof.

The lab successfully reproduced the core EML identities and registered all 36
Table 1 primitives. No Table 1 primitive is missing a source witness, and no
Table 1 row remains untested. The arithmetic, exponential/logarithmic, trig,
hyperbolic, and most derived rows reproduce numerically under explicit
semantics. Branch-sensitive constants and functions reproduce where the branch
conventions are explicit, including the author-style `LogLower` convention for
the `i`/`pi`/trig path.

The remaining qualification is the inverse-function branch cluster. The root
gap is compositional: the derived `arcosh` witness is outward-valid for real
`x > 1`, but it is not safe as an internal replacement for principal
`ArcCosh` on the interval required by the `arccos` witness. The author source
verifies `arccos` as a named Mathematica identity,
`ArcCosh[Cos[ArcCosh[x]]]`, and does not demonstrate substitution of the
derived EML `arcosh` witness into both internal `ArcCosh` positions. A
diagnostic helper reproduces the staged named-function behavior, but it is not
source-justified as the derived EML witness.

Final result: broad reproduction succeeded, while full dependency-chain
compositional closure remains blocked for the inverse-function cluster. This
is a qualified reproduction and proof-audit result, not a generic failure and
not a complete pure EML proof.

Layer distinctions used in this report:

- named-function reproduction: passes for the `arccos` identity;
- dependency-chain reproduction: blocked for `arccos`, `arcsin`, `artanh`, and
  `arctan`;
- staged diagnostic-helper reproduction: passes but remains diagnostic-only;
- fully expanded EML reproduction: not claimed for the inverse-function
  cluster;
- Mathematica/source-chain proof: supports named phase-2 identities but not
  full derived substitution for the inverse cluster;
- Python/mpmath numerical reproduction: supports ordinary-domain and staged
  behavior under documented semantics.

Final Table 1 status counts:

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

Final test and environment metadata:

```text
tests: 92 passed
date: 2026-04-24
mpmath: 1.3.0
numpy: 2.4.4
sympy: 1.14.0
pytest: 9.0.3
commit hash: unavailable; this lab directory is not inside a Git worktree
```

## Historical initial status

The first milestone scaffold checked the constructive spine below. This section
and the iteration sections that follow are retained as chronology; the final
verdict above supersedes these earlier interim statuses.

Core identities targeted:

- `e = eml(1, 1)`
- `exp(x) = eml(x, 1)`
- `ln(x) = eml(1, eml(eml(1, x), 1))` for `x > 0`

At that initial point, author-code reproduction and full Table 1 extraction
were still pending source bootstrap and audit.

## Source Acquisition

Fetched and recorded in `sources/manifest.md`:

- arXiv paper v2 PDF;
- arXiv e-print/source bundle;
- extracted `SupplementaryInformation.pdf`;
- Zenodo v1.0 software snapshot;
- GitHub `VA00/SymbolicRegressionPackage`;
- arXiv follow-up `2604.13871`;
- arXiv follow-up `2604.13873`.

## Local Tests

`uv run pytest` result:

```text
12 passed
```

Verified in the local harness:

- `e = eml(1, 1)`;
- `exp(x) = eml(x, 1)`;
- `ln(x) = eml(1, eml(eml(1, x), 1))` on positive real samples and by SymPy
  under positive-real assumptions.

## Author Code

GitHub commit:

```text
6ac7c0bc4d16624ff4259cc52b8491b8706be6e8
```

Observed tools:

- `EML_toolkit`;
- compiler generators for mpmath, NumPy, Torch, and C;
- Mathematica verification notebook/log;
- Rust verifier and Rust search tools.

`cargo build` succeeds in:

```text
external/SymbolicRegressionPackage/rust_verify
```

The captured run:

```text
cargo run -- --constants 1 --functions '' --operations EML --max-k 10 --explain
```

is stored at `reports/author_rust_verify_run.md`. It ends with no remaining
default targets, but the log reports `EulerGamma` and `Glaisher` in the loaded
base constants despite `--constants 1`. Treat that as an audit item before
claiming a clean pure-constant-1 author-code reproduction.

## Witness Source Location

The complete chain appears in the SI and author code/logs, especially:

- `sources/SupplementaryInformation.pdf`;
- `external/SymbolicRegressionPackage/EML_toolkit/EmL_verification/verify_eml_symbolic_chain.wl`;
- `external/SymbolicRegressionPackage/rust_verify/verify_eml_symbolic_chain.wl`;
- `external/SymbolicRegressionPackage/EML_toolkit/EmL_compiler/eml_compiler_v4.py`.

The main paper alone is not enough to audit every witness.

## Iteration 2 Findings

Registered Table 1 primitives:

```text
36
```

Witness extraction status:

- extracted Table 1 basis into `src/eml_lab/table1.py`;
- extracted Table S2 dependency-chain witnesses into `src/eml_lab/witnesses.py`;
- added support witness `zero`, which is not a Table 1 primitive but is needed
  for the arithmetic spine;
- no Table 1 primitive is currently blocked by a missing source witness;
- pure local EML AST witnesses are present for the terminal/core subset
  (`one`, `x`, `y`, `e`, `exp`, `ln`);
- all 36 Table 1 primitives have at least a dependency-chain witness.

Current status counts for Table 1 rows:

```text
verified: 6
reproduced-numerically: 11
partially-reproduced: 4
blocked-by-branch-semantics: 11
blocked-by-source-gap: 0
failed: 0
not-yet-tested: 4
```

Positive-real arithmetic-spine tests:

```text
40 passed
```

The tested arithmetic spine covers `e`, `exp`, `ln`, `sub`, `zero`,
`neg_one`, `minus`, `add`, `mul`, `div`, `pow`, `log_base`, `sqrt`, `sqr`,
`half`, `avg`, and `hypot`. The sign-flip and addition path is marked only
partially reproduced because the fully inlined EML form can pass through
`log(0)` and therefore depends on extended-real/backend behavior.

`LogLower` audit:

- author Mathematica verification defines `LogLower` as a lower-edge logarithm
  on negative real inputs;
- local `mpmath_lower_backend` reproduces this numerically;
- `i`, `pi`, trig functions, and inverse trig functions remain
  `blocked-by-branch-semantics` until their full dependency chains are checked
  under this convention.

Rust constant audit:

- `EulerGamma` and `Glaisher` are unconditionally inserted into
  `known_constants` in the Rust verifier;
- SI Table S2 describes them as probe inputs, not construction primitives;
- the Rust CLI output should be treated as strong reproduction evidence and a
  witness source, not as a standalone pure `{1, EML}` proof.

Next recommended iteration:

1. Implement branch-aware numeric verification for `i`, `pi`, `cos`, `sin`,
   `tan`, and the inverse trig/hyperbolic witnesses using `mpmath_lower`.
2. Separate pure EML expansion from dependency-chain semantic formulas in the
   report.
3. Add NumPy cross-check columns for the arithmetic spine and selected branch
   cases.

## Iteration 3 Findings

Branch-sensitive primitives tested:

```text
i, pi, cos, sin, tan, arsinh, arcosh, arccos, arcsin, artanh, arctan
```

Backend-specific results:

```text
mpmath_principal: passed 6, expected-failed 5
mpmath_lower:     passed 7, expected-failed 4
numpy_principal:  passed 5, expected-failed/not-implemented 6
```

Constants:

- `i`: principal-log dependency-chain witness sign-flips to `-i`; LogLower
  reproduces `+i`.
- `pi`: reproduces numerically under both principal and LogLower when `ln(-1)`
  and `i` are constructed consistently.

Real-domain trig and hyperbolic branch results:

- `cos`, `sin`, `tan`: reproduced numerically on conservative real samples;
  tangent samples avoid poles.
- `arsinh`: reproduced numerically on real samples.
- `arcosh`: reproduced numerically for real `x > 1`.

Still blocked:

- `arccos`, `arcsin`, `artanh`, `arctan` fail on negative real samples in the
  local Python dependency-chain reproduction. Positive samples pass for these
  rows, so this is a branch/semantic gap rather than a source gap.

Extended-real blockers:

- No Iteration 3 branch-sensitive direct dependency-chain test required
  extended-real behavior.
- `i` and `pi` still inherit the earlier `neg_one` fully-inlined `log(0)` risk
  if one insists on pure EML expansion all the way down.

Author branch convention:

- The author `LogLower` convention is now reproducible in Python for exact
  negative-real log behavior and for the `i` sign correction.
- The dependency-chain evaluator snaps numerically tiny imaginary parts of
  intended exact negative-real intermediates before applying the branch. This
  is necessary because floating evaluation of `exp(e +/- i*pi)` otherwise
  lands on an arbitrary side of the cut.

Updated Table 1 status counts:

```text
verified: 6
reproduced-numerically: 18
partially-reproduced: 4
blocked-by-branch-semantics: 4
blocked-by-source-gap: 0
failed: 0
not-yet-tested: 4
```

Unresolved semantic questions:

- Do the inverse-trig witnesses require a Mathematica-specific simplification
  or branch convention beyond `LogLower`?
- Should the lab adopt a formal branch sheet model for `arcosh/arccos` rather
  than relying on backend principal functions?
- Can the pure EML expansion of `neg_one`, `minus`, and `add` be made
  backend-independent without relying on `log(0) = -inf`?

Recommended Iteration 4:

1. Focus on the four still-blocked inverse-trig rows.
2. Compare local Python dependency-chain outputs against
   `mathematica_verify.log` and `verify_eml_symbolic_chain.wl` line by line.
3. Add a small branch-sheet diagnostic notebook/report for `arcosh`,
   `arccos`, `arcsin`, `artanh`, and `arctan`.
4. Add NumPy cross-checks for the non-branch arithmetic and low-risk
   hyperbolic rows.

## Iteration 4 Findings

Literature sources added:

- Kahan on signed zero and side-of-cut continuity;
- DLMF §§4.2, 4.23, and 4.37 for principal log, inverse trig, and inverse
  hyperbolic conventions;
- Corless/Davenport/Jeffrey/Watt on A&S inverse-function branch conventions
  and unwinding-number corrections;
- Rich/Jeffrey on function evaluation on branch cuts;
- England/Bradford/Davenport/Wilson on composed branch cuts and Maple branch
  tools;
- Davenport/Bradford/England/Wilson on program verification with complex
  branch cuts;
- Aprahamian/Higham on unwinding diagnostics;
- Shterenlikht/CMPLX on branch-cut behavior in numerical libraries.

Author witnesses inspected for the four blockers:

```text
arccos: ArcCosh[Cos[ArcCosh[x]]]
arcsin: Pi/2 - ArcCos[x] in the accepted phase-2/Rust chain
artanh: ArcSinh[1/Tan[ArcCos[x]]]
arctan: ArcSin[Tanh[ArcSinh[x]]]
```

The full EML Mathematica chain also records `arcSinEML[x_] :=
arcCosEML[sinEML[arcCosEML[x]]]`; the accepted phase-2 and Rust witness for
`arcsin` is the `Pi/2 - ArcCos[x]` form.

Branch-sheet diagnostic summary:

```text
mpmath_principal:
  arccos: 4 square-root-sheet/composed-cut failures, 5 matches
  arcsin: 4 sign flips, 5 matches
  artanh: 4 sign flips, 5 matches
  arctan: 5 sign flips, 6 matches

mpmath_lower:
  arccos: 4 square-root-sheet/composed-cut failures, 5 matches
  arcsin: 4 sign flips, 5 matches
  artanh: 4 sign flips, 5 matches
  arctan: 5 sign flips, 6 matches
```

Cause of each blocker:

- `arccos`: Python evaluates the dependency chain on the `acos(abs(x))` sheet
  for negative real `x`; this is a square-root/arcosh sheet mismatch in a
  composed expression, not a missing source witness.
- `arcsin`: inherits the `arccos` mismatch and sign-flips for negative real
  samples.
- `artanh`: inherits the `arccos` mismatch through `tan(arccos(x))` and
  sign-flips for negative real samples.
- `arctan`: inherits the `arcsin` mismatch through `arcsin(tanh(arsinh(x)))`
  and sign-flips for negative real samples.

Unwinding and branch-offset findings:

- no blocker has a stable global `2*pi*i*k` logarithmic sheet offset;
- no blocker has a stable global `pi*k` or `pi/2*k` real offset;
- `arctan(-1)` has an isolated `pi/2` coincidence, but other samples show the
  offset is sample-dependent;
- the failure should be classified as branch-sheet selection, not repaired by
  adding a constant offset.

Side-of-cut findings:

- upper/lower probes `x +/- i*eps` were added for `eps = 1e-6, 1e-12, 1e-30`;
- `mpmath` preserves side information for explicit small imaginary
  perturbations;
- the side probes do not repair the negative-real `arccos` mismatch, so the
  current blocker is larger than exact signed-zero support alone.

Backend or registry changes:

- added `src/eml_lab/unwinding.py`;
- added `src/eml_lab/inverse_branch_diagnostics.py`;
- added `tests/test_unwinding.py`;
- added `tests/test_inverse_branch_diagnostics.py`;
- added Iteration 4 branch metadata fields to `src/eml_lab/witnesses.py`;
- added `reports/inverse_function_branch_audit.md`;
- added `docs/branch_literature_review.md`;
- updated `docs/branch_cuts.md`, `docs/semantics.md`, and the status-matrix
  builder.

Updated Table 1 status counts:

```text
verified: 6
reproduced-numerically: 18
partially-reproduced: 4
blocked-by-branch-semantics: 4
blocked-by-source-gap: 0
failed: 0
not-yet-tested: 4
```

Remaining blockers:

- `arccos`, `arcsin`, `artanh`, and `arctan` remain
  `blocked-by-branch-semantics` in Python dependency-chain reproduction;
- the likely next repair target is an author-compatible `arcosh`/square-root
  sheet rule for the composed `arccos` witness.

Rows still `not-yet-tested`:

- `sigmoid`: add real-domain tests against `1/(1+exp(-x))`, avoiding overflow;
- `cosh`: test real-domain dependency chain and then complex samples away from
  overflow;
- `sinh`: test real-domain dependency chain; verify the EML-specific witness
  does not introduce avoidable branch artifacts;
- `tanh`: test real samples away from poles and then selected complex samples.

Recommended Iteration 5:

1. Implement focused positive/real-domain tests for `sigmoid`, `cosh`, `sinh`,
   and `tanh` to retire the remaining `not-yet-tested` rows.
2. Prototype an isolated branch-adjusted `arcosh`/square-root sheet helper for
   the `arccos` witness only, with before/after diagnostics.
3. Verify that any branch helper preserves all Iteration 3 passing rows.
4. If the repair cannot be source-justified, keep the four inverse rows blocked
   and add a Mathematica-vs-Python symbolic branch-cut comparison notebook.

## Iteration 5 Findings

Retired previously untested rows:

```text
sigmoid: reproduced-numerically on deterministic real samples
cosh:    reproduced-numerically on deterministic real samples
sinh:    reproduced-numerically on deterministic real samples
tanh:    reproduced-numerically on deterministic real samples
```

The remaining `not-yet-tested` count is now:

```text
0
```

Direct named-function isolation:

```text
mpmath.acosh(mpmath.cos(mpmath.acosh(x))) == mpmath.acos(x)
```

on samples:

```text
-0.9, -0.5, -0.1, 0, 0.1, 0.5, 0.9
```

Result:

```text
7 exact-match, 0 failed
```

So the author's named formula is not the blocker under direct principal
`mpmath` functions.

Extended-domain derived `arcosh` result:

```text
ordinary real x > 1:
  mpmath_principal: 4 exact-match
  mpmath_lower:     4 exact-match

interior branch-cut interval -1 < x < 1:
  mpmath_principal: 3 wrong-square-root-sheet, 4 conjugation
  mpmath_lower:     3 wrong-square-root-sheet, 4 exact-match

x < -1:
  mpmath_principal: 4 wrong-log-sheet
  mpmath_lower:     4 wrong-log-sheet
```

Root cause of the `arccos` blocker:

- formula-level: direct named `ArcCosh[Cos[ArcCosh[x]]]` passes;
- dependency-level: replacing named `ArcCosh` with the derived `arcosh`
  witness fails for `x in (-1,0)`;
- observed final result: `acos(abs(x))` instead of `acos(x)`;
- immediate root blocker: the derived `arcosh` witness is valid on `x > 1`
  but not safe as a principal `arcosh` dependency on the internal interval
  `(-1,1)`.

Staged `arccos` isolation:

```text
all direct named mpmath functions:                  7 exact-match
derived arcosh + direct cos + derived arcosh:       4 exact-match, 3 acos(abs(x)) sheet
full dependency-chain evaluator:                    4 exact-match, 3 acos(abs(x)) sheet
```

Inherited blockers:

- `arcsin` remains inherited from `arccos`;
- `artanh` remains inherited from `arccos`;
- `arctan` remains inherited from `arcsin`, which inherits from `arccos`.

Repair status:

- no backend repair was attempted;
- this was intentional because the source-justified rule is not yet pinned
  down;
- a global `arcosh` change would be unsafe because `arcosh` is already
  reproduced on `x > 1`, while the defect is internal extended-domain behavior.

Updated Table 1 status counts:

```text
verified: 6
reproduced-numerically: 22
partially-reproduced: 4
blocked-by-branch-semantics: 4
blocked-by-source-gap: 0
failed: 0
not-yet-tested: 0
```

Remaining blockers:

```text
arccos, arcsin, artanh, arctan
```

Recommended Iteration 6:

1. Inspect Mathematica's branch assumptions for `ArcCosh[Cos[ArcCosh[x]]]`
   over `-1 <= x <= 1` and determine whether the proof relies on built-in
   `ArcCosh`, an unstated rewrite, or a sheet convention absent from the EML
   dependency chain.
2. Prototype an isolated `principal_arcosh_internal` helper for branch-sensitive
   reproduction only, starting with the documented domains `(-1,1)` and
   `x < -1`.
3. Retest `arccos` with the helper in staged mode before touching the full
   dependency-chain evaluator.
4. If the helper is source-justified, add regression tests for `i`, `pi`,
   `sin`, `cos`, `tan`, `arsinh`, `arcosh` on `x > 1`, and the arithmetic
   spine before updating any final statuses.

## Iteration 6 Findings

Author proof-chain audit:

- The author Mathematica file defines full EML-level functions including
  `arcCoshEML` and `arcCosEML`.
- The symbolic proof section then switches to phase-2 canonical named forms.
- `arcCoshW[x_] := ArcSinh[Sqrt[x^2 - 1]]` is checked only under `x >= 1`.
- `arcCosW[x_] := ArcCosh[Cos[ArcCosh[x]]]` is checked under
  `-1 <= x <= 1` using named Mathematica `ArcCosh`, not by substituting
  `arcCoshW` into both internal positions.

Full compositional substitution is therefore not shown in the inspected
source. The available source supports named-function phase-2 reproduction, not
a proof that every discovered primitive is globally composable on later
internal branch domains.

Compositional-validity result for `arcosh`:

```text
outward-domain status:          outward-valid on real x > 1
internal compositional status:  compositionally-unsafe for arccos on (-1,0)
unsafe domains observed:        (-1,0) and x < -1
```

Diagnostic internal helper:

```text
principal_arcosh_internal(z) =
  log(z + sqrt(z - 1) * sqrt(z + 1))
```

This helper matches `mpmath.acosh` on:

- real `x > 1`;
- real `-1 < x < 1`;
- real `x < -1`;
- side-of-cut probes with `eps = 1e-6, 1e-12, 1e-30`.

Staged `arccos` results:

```text
named acosh(cos(acosh(x))):                 passes all samples
fully derived dependency chain:             fails on x < 0 as acos(abs(x))
internal helper for both acosh calls:        passes all samples
internal helper for first acosh only:        passes all samples
internal helper for final acosh only:        still fails on x < 0
```

Repair classification:

```text
diagnostic-only repair
```

Reason: the helper reproduces the principal branch needed by the named
identity, but the inspected author sources do not explicitly justify replacing
the derived EML `arcosh` witness with that helper inside later witnesses. The
lab therefore does not globally alter `arcosh` or mark the fully derived
`arccos` chain verified.

Impact on inherited blockers:

- `arcsin`: passes through the diagnostic helper path, but remains inherited
  from source-ambiguous `arccos` for full dependency-chain reproduction.
- `artanh`: passes through the diagnostic helper path, but remains inherited
  from source-ambiguous `arccos`.
- `arctan`: passes through the diagnostic helper path, but remains inherited
  through `arcsin`.

Regression result:

```text
iteration-6 regression tests passed
```

The regression suite covers `e`, `exp`, `ln`, arithmetic samples, `i`, `pi`,
`sin`, `cos`, `tan`, `arsinh`, `arcosh` on `x > 1`, and the newly reproduced
`sigmoid`, `cosh`, `sinh`, `tanh` rows.

Updated Table 1 status counts:

```text
verified: 6
reproduced-numerically: 22
partially-reproduced: 5
blocked-by-branch-semantics: 3
blocked-by-source-gap: 0
failed: 0
not-yet-tested: 0
```

Remaining final-status blockers:

```text
arcsin, artanh, arctan
```

Remaining full-dependency-chain blocker set:

```text
arccos, arcsin, artanh, arctan
```

Recommended Iteration 7:

1. Decide report policy for diagnostic-only internal helpers: keep final
   statuses conservative, or introduce a separate "staged-reproduced" column
   without changing final proof status.
2. If pursuing source justification, inspect Mathematica notebooks/logs for
   any hidden replacement of `ArcCosh` or branch assumptions not present in
   `verify_eml_symbolic_chain.wl`.
3. If no source justification is found, prepare the final report around a
   qualified reproduction: 32/36 Table 1 primitives cleanly reproduced or
   verified by ordinary/dependency semantics, and four inverse-function rows
   blocked or partial at the compositional branch layer.
4. Do not begin symbolic regression until the final branch-semantics verdict is
   written.

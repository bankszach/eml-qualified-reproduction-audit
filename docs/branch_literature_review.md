# Branch Literature Review

**Purpose:** Record branch-cut literature used to interpret the inverse-function blockers.
**Status:** Supporting reference for the qualified audit.
**Last updated:** 2026-04-24.
**Related files:** `docs/branch_cuts.md`, `reports/inverse_function_branch_audit.md`, `reports/final_proof_risks.md`.

This note records only branch facts that affect the EML Table 1 audit. It is
not a general complex analysis survey.

| source | location | branch concept relevant to EML | affected functions | implementation consequence |
| --- | --- | --- | --- | --- |
| W. Kahan, "Branch Cuts for Complex Elementary Functions" | https://people.freebsd.org/~das/kahan86branch.pdf | IEEE signed zero lets a numerical library represent which side of a cut a value approaches. Kahan explicitly treats `sqrt`, `arctan`, and `arccosh` as functions where this side-of-cut convention changes observable values. | `sqrt`, `log`, `arctan`, `arcosh`, composed inverse witnesses | The lab must not treat an exactly real negative sample and the two limits `x +/- i eps` as semantically identical. Python tests need explicit side probes and must document when signed-zero behavior is unavailable. |
| DLMF §4.2, "Logarithm, Exponential, Powers" | https://dlmf.nist.gov/4.2 | The principal logarithm uses a cut on the negative real axis; values on the cut are a convention, not a universal identity. | `log`, `pow`, `sqrt`, every EML expression containing `ln` | `mpmath_principal` and author `LogLower` are separate backends. A result that passes under `LogLower` is not a principal-log pass. |
| DLMF §4.23, "Inverse Trigonometric Functions" | https://dlmf.nist.gov/4.23 | Principal inverse trig functions are single-valued only after cuts are introduced. DLMF assumes principal values unless explicitly stated otherwise. | `arcsin`, `arccos`, `arctan` | Direct `mpmath.asin/acos/atan` is used as the DLMF-style principal reference for real-domain calculator tests. EML witnesses may have different composed branch cuts. |
| DLMF §4.37, "Inverse Hyperbolic Functions" | https://dlmf.nist.gov/4.37 | Principal inverse hyperbolic functions also require cuts and are two-valued on their cuts. | `arsinh`, `arcosh`, `artanh` | The `arcosh` witness is safe on `x > 1`, but using it inside `arccos` for `x in (-1,1)` crosses a branch-sensitive region. |
| Corless, Davenport, Jeffrey, Watt, "According to Abramowitz and Stegun" | https://scipp.ucsc.edu/~haber/archives/physics116A10/arccoth.pdf | A&S-style inverse trig/hyperbolic definitions leave side-of-cut questions. The paper discusses signed zeros and unwinding-number corrections for inverse trig identities. | `arcsin`, `arccos`, `arctan`, inverse hyperbolic relatives | The lab classifies errors as branch-sheet offsets first. Additive identities such as `pi/2 - arccos(x)` are valid only with compatible branches. |
| Rich and Jeffrey, "Function Evaluation on Branch Cuts" | DOI 10.1145/235699.235704 | Once principal branches and cut locations are fixed, values exactly on cuts remain a separate CAS/evaluator question. | all branch-cut functions | Exact real samples on a cut or near a cut need explicit "on-cut" or "side-of-cut" status rather than silent pass/fail. |
| England, Bradford, Davenport, Wilson, "Understanding Branch Cuts of Expressions" | https://arxiv.org/abs/1304.7223, DOI 10.1007/978-3-642-39320-4_9 | Composed expressions can induce cuts more complicated than the cuts of their component functions. | composed `arccos`, `arcsin`, `artanh`, `arctan` EML witnesses | The EML dependency chain must be tested as the expression it is, not assumed equivalent to the named reference function because each component is standard. |
| England, Cheb-Terrab, Bradford, Davenport, Wilson, "Branch Cuts in Maple 17" | https://arxiv.org/abs/1308.6523, DOI 10.1145/2644288.2644293 | CAS tooling needs explicit cut calculation and visualization for composed functions involving `sqrt` and `log`. | composed expressions | A future iteration should add symbolic branch-cut extraction or CAS-assisted cut visualization for the four inverse blockers. |
| Davenport, Bradford, England, Wilson, "Program Verification in the presence of complex numbers, functions with branch cuts etc" | https://arxiv.org/abs/1212.5417, DOI 10.1109/SYNASC.2012.68 | Branch cuts are a verification semantics problem: common algebraic simplifications can be invalid on the chosen principal sheets. | every branch-sensitive EML witness | The status matrix must keep Mathematica proof, Python principal behavior, and author `LogLower` behavior separate. |
| Aprahamian and Higham, "The Matrix Unwinding Function, with an Application to Computing the Matrix Exponential" | DOI 10.1137/130920137 | The unwinding function formalizes corrections needed when logarithm identities cross sheets. | `log`, `pow`, inverse functions represented with logs | The local `unwinding.py` utilities classify `2*pi*i*k`, `pi*k`, and `pi/2` offsets but do not repair tests. |
| Shterenlikht, "On quality of implementation of Fortran 2008 complex intrinsic functions on branch cuts" | https://arxiv.org/abs/1712.10230 and https://cmplx.sourceforge.io/ | Signed zero and branch-cut implementation quality are observable in real numerical libraries. | inverse complex intrinsics, `sqrt`, `log` | Backend verdicts need to say whether the backend can represent side-of-cut semantics at exactly real inputs. |

## Consequences for Iteration 4

- The four blockers are not source gaps: each has an author-chain witness.
- The primary first failure is `arccos`; the dependent witnesses inherit it.
- The observed Python failure is not a constant `pi*k` or `2*pi*i*k` sheet
  offset. For negative real samples, `arccos` follows the `acos(abs(x))` sheet.
- Side-of-cut probes are now mandatory for these rows, because exact real
  samples may erase the sign information needed by Kahan-style semantics.

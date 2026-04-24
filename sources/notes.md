# Source Notes

Initial source targets:

- arXiv `2603.21852v2`;
- arXiv ancillary/supplementary files;
- Zenodo record `10.5281/zenodo.19183008`;
- GitHub `VA00/SymbolicRegressionPackage`;
- follow-up hardware/neuro-symbolic EML papers.

The first source-audit question is where the full Table 1 witness list lives:
main paper, supplementary PDF, GitHub generated output, or missing.

## First Audit Findings

- The arXiv e-print bundle contains `anc/SupplementaryInformation.pdf`; it has
  been extracted to `sources/SupplementaryInformation.pdf`.
- The GitHub repository at commit
  `6ac7c0bc4d16624ff4259cc52b8491b8706be6e8` contains:
  - `EML_toolkit/EmL_verification/verify_eml_symbolic_chain.wl`
  - `EML_toolkit/EmL_verification/rust_verify.log`
  - `EML_toolkit/EmL_verification/mathematica_verify.log`
  - `EML_toolkit/EmL_compiler/eml_compiler_v4.py`
  - `rust_verify/src/main.rs`
- The full constructive dependency chain appears to live primarily in the SI
  and verification code/logs, not in the main paper alone.
- `rust_verify/verify_eml_symbolic_chain.wl` explicitly lists a chain from
  `EML` through `Exp`, `Log`, arithmetic, constants, trig/hyperbolic, and
  inverse trig/hyperbolic functions.

## Open Source Questions

- Extract the exact Table 1 rows from the main PDF or SI.
- Confirm whether the Rust CLI's `--constants 1` mode intentionally still
  loads `EulerGamma` and `Glaisher` as variable placeholders or auxiliary
  symbols; the first captured run reports them in the loaded base constants.
- Compare the Mathematica branch convention in `LogLower` against the local
  principal-log `mpmath`/NumPy semantics.

## Iteration 2 Source Findings

- Table 1 was visually checked on page 6 of `sources/2603.21852v2.pdf`.
- SI Table S2 was visually checked on page 6 of
  `sources/SupplementaryInformation.pdf`.
- SI Table S2 states that EulerGamma and Glaisher are probe inputs and are not
  part of the construction.
- The author Mathematica file defines `LogLower` as a lower-edge branch for
  negative real inputs.

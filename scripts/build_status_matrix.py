#!/usr/bin/env python
"""Build reports/status_matrix.md from the witness registry."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from eml_lab.table1 import TABLE1_PRIMITIVES
from eml_lab.witnesses import WITNESSES, table1_witnesses


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "status_matrix.md"
LAST_UPDATED = "2026-04-24"


def row(values: list[str]) -> str:
    return "| " + " | ".join(value.replace("\n", " ") for value in values) + " |"


def audit_marker(name: str) -> str:
    if name == "arcosh":
        return "outward-valid; compositionally unsafe dependency"
    if name == "arccos":
        return "inverse cluster root; partial but dependency-chain blocked"
    if name in {"arcsin", "artanh", "arctan"}:
        return "inverse cluster inherited branch blocker"
    return ""


def header() -> list[str]:
    return [
        "# Status Matrix",
        "",
        "**Purpose:** Generated Table 1 status matrix for the qualified EML audit.",
        "**Status:** Final generated matrix; edit `scripts/build_status_matrix.py` or `src/eml_lab/witnesses.py`, not generated rows.",
        f"**Last updated:** {LAST_UPDATED}.",
        "**Related files:** `docs/status_policy.md`, `reports/reproduction_report.md`, `reports/final_proof_risks.md`.",
        "",
        "## Reading Notes",
        "",
        "This matrix reports the completed qualified audit. It separates ordinary outward-domain numerical reproduction from full dependency-chain compositional closure. The inverse-function cluster is deliberately marked because it is the remaining branch-semantics qualification.",
        "",
    ]


def footer() -> list[str]:
    counts = Counter(witness.final_status for witness in table1_witnesses().values())
    status_order = [
        "verified",
        "reproduced-numerically",
        "partially-reproduced",
        "blocked-by-branch-semantics",
        "blocked-by-source-gap",
        "failed",
        "not-yet-tested",
    ]
    lines = [
        "",
        "## Legend",
        "",
        "- `verified`: source-supported and checked under explicit assumptions.",
        "- `reproduced-numerically`: numerical reproduction passed on the documented calculator-facing domain.",
        "- `partially-reproduced`: named, staged, or ordinary-domain reproduction succeeded, but a dependency, edge-case, fully expanded path, or compositional substitution remains unresolved. This does not mean failure.",
        "- `blocked-by-branch-semantics`: a source witness exists, but branch/sheet behavior is not explicit enough for the audited claim. This is the status for inherited inverse-function blockers.",
        "- `blocked-by-source-gap`: a needed source witness or derivation is missing.",
        "- `failed`: tested under stated semantics with no qualifying branch/source explanation.",
        "- `not-yet-tested`: no local test has been run for that status column.",
        "",
        "## Footnotes",
        "",
        "- Outward-valid rows reproduce the intended Table 1 primitive on the ordinary calculator-facing domain.",
        "- Compositionally unsafe rows may pass outward tests but fail when substituted into a later witness on that later witness's internal domain.",
        "- Diagnostic-only rows pass through staged helpers that reproduce named principal-function behavior, but those helpers are not source-derived EML witnesses.",
        "- Branch-sensitive rows depend on explicit logarithm, square-root, signed-zero, or side-of-cut semantics.",
        "- Fully dependency-chain reproduced rows pass after replacing named dependencies with their registered source witnesses on the tested domain.",
        "",
        "## Inverse-Function Cluster Note",
        "",
        "`arccos` is included in the full dependency-chain blocker set even though its final status is `partially-reproduced`: named/staged reproduction and diagnostic-helper reproduction pass, while substitution of the derived `arcosh` witness fails on negative real samples. `arcsin`, `artanh`, and `arctan` inherit this branch-semantics blocker through `arccos` or `arcsin`.",
        "",
        "## Final Table 1 Counts",
        "",
        f"- total primitives: {len(TABLE1_PRIMITIVES)}",
    ]
    lines.extend(f"- {status}: {counts.get(status, 0)}" for status in status_order)
    return lines


def main() -> None:
    headers = [
        "primitive",
        "audit marker",
        "type",
        "Table 1 category",
        "witness source",
        "pure EML available?",
        "dependency chain available?",
        "symbolic status",
        "mpmath status",
        "principal-log status",
        "LogLower status",
        "NumPy status",
        "branch risk",
        "extended-real risk",
        "branch convention",
        "generated constants",
        "branch-sheet notes",
        "internal branch status",
        "compositional status",
        "root blocker",
        "final status",
        "notes",
    ]
    lines = header()
    lines.extend([row(headers), row(["---"] * len(headers))])
    ordered_names = [item.canonical_name for item in TABLE1_PRIMITIVES] + [
        name for name, witness in WITNESSES.items() if not witness.table1
    ]
    for name in ordered_names:
        witness = WITNESSES[name]
        lines.append(
            row(
                [
                    witness.primitive,
                    audit_marker(name),
                    witness.primitive_type,
                    witness.table1_category,
                    witness.source,
                    "yes" if witness.pure_eml_available else "no",
                    "yes" if witness.dependency_chain_available else "no",
                    witness.symbolic_status,
                    witness.numeric_status,
                    witness.principal_log_status,
                    witness.loglower_status,
                    witness.numpy_principal_status,
                    witness.branch_risk,
                    witness.extended_real_risk,
                    witness.branch_convention,
                    ", ".join(witness.generated_constants),
                    witness.branch_sheet_notes,
                    witness.internal_branch_cut_status,
                    witness.internal_compositional_status,
                    witness.root_blocker,
                    witness.final_status,
                    witness.notes or witness.dependency_witness,
                ]
            )
        )
    lines.extend(footer())
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

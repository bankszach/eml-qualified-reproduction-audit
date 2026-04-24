"""Traceable expansion of dependency-chain witnesses into EML ASTs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from eml_lab.ast import EML, ONE, Const, Expr, Var, exp_expr, ln_expr


class ExpansionError(ValueError):
    """Raised when a witness cannot be expanded into the local EML AST."""


@dataclass(frozen=True)
class ExprStats:
    nodes: int
    leaves: int
    depth: int


def expr_stats(expr: Expr) -> ExprStats:
    if isinstance(expr, EML):
        left = expr_stats(expr.left)
        right = expr_stats(expr.right)
        return ExprStats(
            nodes=1 + left.nodes + right.nodes,
            leaves=left.leaves + right.leaves,
            depth=1 + max(left.depth, right.depth),
        )
    return ExprStats(nodes=1, leaves=1, depth=0)


def unresolved_dependencies(name: str) -> tuple[str, ...]:
    try:
        expand_witness(name)
    except ExpansionError as exc:
        return (str(exc),)
    return ()


def expand_witness(name: str) -> Expr:
    """Expand a named witness using canonical variables where needed."""

    if name in {"ln", "exp"}:
        return _expand(name, (Var("x"),), ())
    if name in {"x", "y", "one", "e", "zero", "neg_one", "two"}:
        return _expand(name, (), ())
    if name in {"minus", "inv", "half", "sqrt", "sqr"}:
        return _expand(name, (Var("x"),), ())
    if name in {"sub", "add", "mul", "div", "pow", "log_base", "avg", "hypot"}:
        return _expand(name, (Var("x"), Var("y")), ())
    raise ExpansionError(f"no local expansion rule for {name!r}")


def rpn_for(name: str) -> str:
    return expand_witness(name).to_rpn()


def _expand(name: str, args: tuple[Expr, ...], stack: tuple[str, ...]) -> Expr:
    if name in stack:
        raise ExpansionError(f"cycle while expanding {' -> '.join(stack + (name,))}")

    rules: dict[str, Callable[[tuple[Expr, ...], tuple[str, ...]], Expr]] = {
        "one": lambda a, s: ONE,
        "x": lambda a, s: Var("x"),
        "y": lambda a, s: Var("y"),
        "e": lambda a, s: EML(ONE, ONE),
        "exp": lambda a, s: exp_expr(a[0]),
        "ln": lambda a, s: ln_expr(a[0]),
        "zero": lambda a, s: _expand("ln", (ONE,), s + ("zero",)),
        "sub": lambda a, s: EML(_expand("ln", (a[0],), s + ("sub",)), _expand("exp", (a[1],), s + ("sub",))),
        "minus": lambda a, s: _expand("sub", (_expand("zero", (), s + ("minus",)), a[0]), s + ("minus",)),
        "neg_one": lambda a, s: _expand("minus", (ONE,), s + ("neg_one",)),
        "add": lambda a, s: _expand("sub", (a[0], _expand("minus", (a[1],), s + ("add",))), s + ("add",)),
        "two": lambda a, s: _expand("sub", (ONE, _expand("neg_one", (), s + ("two",))), s + ("two",)),
        "inv": lambda a, s: _expand("exp", (_expand("minus", (_expand("ln", (a[0],), s + ("inv",)),), s + ("inv",)),), s + ("inv",)),
        "mul": lambda a, s: _expand(
            "exp",
            (_expand("add", (_expand("ln", (a[0],), s + ("mul",)), _expand("ln", (a[1],), s + ("mul",))), s + ("mul",)),),
            s + ("mul",),
        ),
        "sqr": lambda a, s: _expand("mul", (a[0], a[0]), s + ("sqr",)),
        "div": lambda a, s: _expand("mul", (a[0], _expand("inv", (a[1],), s + ("div",))), s + ("div",)),
        "half": lambda a, s: _expand("div", (a[0], _expand("two", (), s + ("half",))), s + ("half",)),
        "avg": lambda a, s: _expand("half", (_expand("add", (a[0], a[1]), s + ("avg",)),), s + ("avg",)),
        "sqrt": lambda a, s: _expand("exp", (_expand("half", (_expand("ln", (a[0],), s + ("sqrt",)),), s + ("sqrt",)),), s + ("sqrt",)),
        "pow": lambda a, s: _expand("exp", (_expand("mul", (a[1], _expand("ln", (a[0],), s + ("pow",))), s + ("pow",)),), s + ("pow",)),
        "log_base": lambda a, s: _expand("div", (_expand("ln", (a[1],), s + ("log_base",)), _expand("ln", (a[0],), s + ("log_base",))), s + ("log_base",)),
        "hypot": lambda a, s: _expand("sqrt", (_expand("add", (_expand("sqr", (a[0],), s + ("hypot",)), _expand("sqr", (a[1],), s + ("hypot",))), s + ("hypot",)),), s + ("hypot",)),
    }

    if name not in rules:
        raise ExpansionError(f"unresolved dependency {name!r}")
    try:
        return rules[name](args, stack)
    except IndexError as exc:
        raise ExpansionError(f"wrong arity while expanding {name!r}") from exc


def const_value_expr(value: int) -> Expr:
    """Non-pure helper for diagnostics only."""

    return Const(value)

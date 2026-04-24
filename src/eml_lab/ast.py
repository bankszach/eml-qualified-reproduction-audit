"""Minimal EML expression tree and RPN support."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from eml_lab.core import BackendName, eml


class Expr:
    """Base class for EML expressions."""

    def eval(self, env: Mapping[str, Any] | None = None, *, backend: BackendName = "mpmath") -> Any:
        raise NotImplementedError

    def to_rpn(self) -> str:
        raise NotImplementedError

    def pretty(self) -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class Const(Expr):
    value: Any = 1

    def eval(self, env: Mapping[str, Any] | None = None, *, backend: BackendName = "mpmath") -> Any:
        return self.value

    def to_rpn(self) -> str:
        if self.value != 1:
            raise ValueError("pure EML RPN only supports literal constant 1")
        return "1"

    def pretty(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Var(Expr):
    name: str

    def eval(self, env: Mapping[str, Any] | None = None, *, backend: BackendName = "mpmath") -> Any:
        if env is None or self.name not in env:
            raise KeyError(f"missing variable {self.name!r}")
        return env[self.name]

    def to_rpn(self) -> str:
        if len(self.name) != 1:
            raise ValueError("RPN variables must be single-character names")
        return self.name

    def pretty(self) -> str:
        return self.name


@dataclass(frozen=True)
class EML(Expr):
    left: Expr
    right: Expr

    def eval(self, env: Mapping[str, Any] | None = None, *, backend: BackendName = "mpmath") -> Any:
        return eml(self.left.eval(env, backend=backend), self.right.eval(env, backend=backend), backend=backend)

    def to_rpn(self) -> str:
        return f"{self.left.to_rpn()}{self.right.to_rpn()}E"

    def pretty(self) -> str:
        return f"eml({self.left.pretty()}, {self.right.pretty()})"


def parse_rpn(text: str) -> Expr:
    """Parse compact RPN where `1` is the constant, letters are variables, and `E` is eml."""

    stack: list[Expr] = []
    for token in text:
        if token == "1":
            stack.append(Const(1))
        elif token == "E":
            if len(stack) < 2:
                raise ValueError(f"not enough operands before E in {text!r}")
            right = stack.pop()
            left = stack.pop()
            stack.append(EML(left, right))
        elif token.isalpha() and token.islower():
            stack.append(Var(token))
        else:
            raise ValueError(f"unsupported RPN token {token!r}")

    if len(stack) != 1:
        raise ValueError(f"RPN expression left {len(stack)} stack items")
    return stack[0]


ONE = Const(1)


def exp_expr(x: Expr) -> Expr:
    return EML(x, ONE)


def ln_expr(x: Expr) -> Expr:
    return EML(ONE, EML(EML(ONE, x), ONE))


"""Machine-readable Table 1 primitive basis from arXiv:2603.21852v2."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

PrimitiveType = Literal["constant", "unary", "binary"]


@dataclass(frozen=True)
class Table1Primitive:
    canonical_name: str
    paper_name: str
    primitive_type: PrimitiveType
    expected_definition: str
    real_domain: str
    complex_intermediates_expected: bool
    source_pointer: str


TABLE1_PRIMITIVES: tuple[Table1Primitive, ...] = (
    Table1Primitive("pi", "pi", "constant", "pi", "real constant", True, "paper Table 1, page 6; SI Table S2 step 18"),
    Table1Primitive("e", "e", "constant", "Euler's number", "positive real constant", False, "paper Table 1, page 6; SI Table S2 step 1"),
    Table1Primitive("i", "i", "constant", "sqrt(-1)", "imaginary constant", True, "paper Table 1, page 6; repo Mathematica chain line 36"),
    Table1Primitive("neg_one", "-1", "constant", "-1", "real constant", False, "paper Table 1, page 6; SI Table S2 step 5"),
    Table1Primitive("one", "1", "constant", "1", "distinguished terminal", False, "paper Table 1, page 6"),
    Table1Primitive("two", "2", "constant", "2", "real constant", False, "paper Table 1, page 6; SI Table S2 step 6"),
    Table1Primitive("x", "x", "constant", "first variable/input", "input variable", False, "paper Table 1, page 6"),
    Table1Primitive("y", "y", "constant", "second variable/input", "input variable", False, "paper Table 1, page 6"),
    Table1Primitive("exp", "exp", "unary", "exp(x) = e^x", "all real x", False, "paper Table 1, page 6; SI Table S2 step 2"),
    Table1Primitive("ln", "ln", "unary", "natural logarithm ln(x)", "x > 0 for real-valued baseline", False, "paper Table 1, page 6; SI Table S2 step 3"),
    Table1Primitive("inv", "inv", "unary", "1/x", "x != 0", False, "paper Table 1, page 6; SI Table S2 step 9"),
    Table1Primitive("half", "half", "unary", "x/2", "all real x", False, "paper Table 1, page 6; SI Table S2 step 13"),
    Table1Primitive("minus", "minus", "unary", "-x", "all real x", False, "paper Table 1, page 6; SI Table S2 step 7"),
    Table1Primitive("sqrt", "sqrt", "unary", "sqrt(x)", "x >= 0 for real-valued baseline", True, "paper Table 1, page 6; SI Table S2 step 15"),
    Table1Primitive("sqr", "sqr", "unary", "x^2", "all real x", False, "paper Table 1, page 6; SI Table S2 step 11"),
    Table1Primitive("sigmoid", "sigma", "unary", "1/(1 + exp(-x))", "all real x", False, "paper Table 1, page 6; SI Table S2 step 20"),
    Table1Primitive("sin", "sin", "unary", "sin(x)", "all real x", True, "paper Table 1, page 6; SI Table S2 step 25"),
    Table1Primitive("cos", "cos", "unary", "cos(x)", "all real x", True, "paper Table 1, page 6; SI Table S2 step 24"),
    Table1Primitive("tan", "tan", "unary", "tan(x)", "cos(x) != 0", True, "paper Table 1, page 6; SI Table S2 step 26"),
    Table1Primitive("arcsin", "arcsin", "unary", "arcsin(x)", "-1 <= x <= 1 for real-valued baseline", True, "paper Table 1, page 6; SI Table S2 step 31"),
    Table1Primitive("arccos", "arccos", "unary", "arccos(x)", "-1 <= x <= 1 for real-valued baseline", True, "paper Table 1, page 6; SI Table S2 step 29"),
    Table1Primitive("arctan", "arctan", "unary", "arctan(x)", "all real x", True, "paper Table 1, page 6; SI Table S2 step 32"),
    Table1Primitive("sinh", "sinh", "unary", "sinh(x)", "all real x", False, "paper Table 1, page 6; SI Table S2 step 22"),
    Table1Primitive("cosh", "cosh", "unary", "cosh(x)", "all real x", False, "paper Table 1, page 6; SI Table S2 step 21"),
    Table1Primitive("tanh", "tanh", "unary", "tanh(x)", "all real x", False, "paper Table 1, page 6; SI Table S2 step 23"),
    Table1Primitive("arsinh", "arsinh", "unary", "asinh(x)", "all real x", True, "paper Table 1, page 6; SI Table S2 step 27"),
    Table1Primitive("arcosh", "arcosh", "unary", "acosh(x)", "x >= 1 for real-valued baseline", True, "paper Table 1, page 6; SI Table S2 step 28"),
    Table1Primitive("artanh", "artanh", "unary", "atanh(x)", "-1 < x < 1", True, "paper Table 1, page 6; SI Table S2 step 30"),
    Table1Primitive("add", "+", "binary", "x + y", "all real x,y", False, "paper Table 1, page 6; SI Table S2 step 8"),
    Table1Primitive("sub", "-", "binary", "x - y", "all real x,y", False, "paper Table 1, page 6; SI Table S2 step 4"),
    Table1Primitive("mul", "x", "binary", "x * y", "all real x,y", False, "paper Table 1, page 6; SI Table S2 step 10"),
    Table1Primitive("div", "/", "binary", "x / y", "y != 0", False, "paper Table 1, page 6; SI Table S2 step 12"),
    Table1Primitive("log_base", "log", "binary", "log_x(y) = ln(y)/ln(x)", "x > 0, x != 1, y > 0", False, "paper Table 1, page 6; SI Table S2 step 17"),
    Table1Primitive("pow", "pow", "binary", "x^y", "x > 0 for real-valued baseline", True, "paper Table 1, page 6; SI Table S2 step 16"),
    Table1Primitive("avg", "avg", "binary", "(x + y)/2", "all real x,y", False, "paper Table 1, page 6; SI Table S2 step 14"),
    Table1Primitive("hypot", "hypot", "binary", "sqrt(x^2 + y^2)", "all real x,y", False, "paper Table 1, page 6; SI Table S2 step 19"),
)

TABLE1_BY_NAME = {item.canonical_name: item for item in TABLE1_PRIMITIVES}

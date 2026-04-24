"""Witness registry for Table 1-oriented EML reproduction."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Callable, Literal

import mpmath as mp

from eml_lab.ast import EML, ONE, Expr, Var, exp_expr, ln_expr
from eml_lab.domains import Domain
from eml_lab.table1 import TABLE1_BY_NAME

PrimitiveType = Literal["constant", "unary", "binary"]
Status = Literal[
    "verified",
    "reproduced-numerically",
    "partially-reproduced",
    "blocked-by-source-gap",
    "blocked-by-branch-semantics",
    "failed",
    "not-yet-tested",
]


@dataclass(frozen=True)
class Witness:
    primitive: str
    primitive_type: PrimitiveType
    table1_category: str
    expression: Expr | None
    source: str
    domain: Domain
    dependencies: tuple[str, ...]
    symbolic_status: Status
    numeric_status: Status
    edge_case_status: Status
    final_status: Status
    branch_risk: str
    extended_real_risk: str
    reference: Callable[..., object] | None = None
    dependency_witness: str = ""
    branch_convention: str = "principal-log unless noted"
    uses_extended_real: bool = False
    generated_constants: tuple[str, ...] = ()
    table1: bool = True
    notes: str = ""
    requires_loglower: bool = False
    principal_log_expected_to_fail: bool = False
    branch_failure_mode: str = ""
    safe_real_domain: str = ""
    safe_complex_domain: str = ""
    extended_real_required: bool = False
    principal_log_status: Status = "not-yet-tested"
    loglower_status: Status = "not-yet-tested"
    numpy_principal_status: Status = "not-yet-tested"
    requires_signed_zero_or_side_of_cut: bool = False
    requires_square_root_branch_control: bool = False
    requires_mathematica_branch_rules: bool = False
    failure_region: str = "not yet classified"
    observed_failure_mode: str = "not yet classified"
    unwinding_offset_observed: str = "not yet classified"
    author_reference_status: str = "not yet classified"
    python_reproduction_status: str = "not yet classified"
    unsafe_real_domain: str = "not yet classified"
    branch_sheet_notes: str = "not yet classified"
    ordinary_real_domain_status: str = "not applicable"
    internal_branch_cut_status: str = "not applicable"
    interval_neg1_1_status: str = "not applicable"
    below_negative_one_status: str = "not applicable"
    safe_as_arccos_dependency: str = "not applicable"
    root_blocker: str = "not applicable"
    inherited_from: str = "not applicable"
    branch_dependency: str = "not applicable"
    repair_attempted: str = "not attempted"
    repair_status: str = "not applicable"
    source_justification: str = "not applicable"
    outward_domain_status: str = "not applicable"
    internal_compositional_status: str = "not applicable"
    compositionally_unsafe_domains: str = "not applicable"
    used_in_arccos_internal_interval: bool = False
    principal_arcosh_helper_available: bool = False
    principal_arcosh_helper_source_status: str = "not applicable"
    source_chain_type: str = "not applicable"
    named_function_reproduction_status: str = "not applicable"
    dependency_chain_reproduction_status: str = "not applicable"
    internal_helper_reproduction_status: str = "not applicable"
    final_branch_verdict: str = "not applicable"

    @property
    def pure_eml_available(self) -> bool:
        return self.expression is not None

    @property
    def dependency_chain_available(self) -> bool:
        return bool(self.dependencies or self.dependency_witness or self.expression)

    @property
    def rpn(self) -> str:
        if self.expression is None:
            return ""
        return self.expression.to_rpn()


X = Var("x")
Y = Var("y")


def _t(name: str) -> str:
    return TABLE1_BY_NAME[name].primitive_type


def _category(name: str) -> str:
    primitive = TABLE1_BY_NAME.get(name)
    if primitive is None:
        return "support"
    if primitive.primitive_type == "constant":
        return "constants/terminals"
    if primitive.canonical_name in {"exp", "ln", "log_base", "pow"}:
        return "exponential/logarithmic"
    if primitive.canonical_name in {"add", "sub", "mul", "div", "avg", "hypot", "inv", "half", "minus", "sqrt", "sqr", "sigmoid"}:
        return "arithmetic/algebraic"
    return "trig/hyperbolic"


def _paper_source(name: str) -> str:
    primitive = TABLE1_BY_NAME.get(name)
    return primitive.source_pointer if primitive else "repo Mathematica chain; support primitive not in paper Table 1"


WITNESSES: dict[str, Witness] = {
    "one": Witness(
        primitive="one",
        primitive_type="constant",
        table1_category=_category("one"),
        expression=ONE,
        source="paper Table 1, page 6",
        domain=Domain.POSITIVE_REAL,
        dependencies=(),
        symbolic_status="verified",
        numeric_status="verified",
        edge_case_status="verified",
        final_status="verified",
        branch_risk="none",
        extended_real_risk="none",
        reference=lambda: mp.mpf(1),
        dependency_witness="distinguished terminal 1",
        notes="This is the only allowed terminal in the EML construction.",
    ),
    "x": Witness(
        primitive="x",
        primitive_type="constant",
        table1_category=_category("x"),
        expression=X,
        source="paper Table 1, page 6",
        domain=Domain.SOURCE_DEPENDENT,
        dependencies=(),
        symbolic_status="verified",
        numeric_status="verified",
        edge_case_status="not-yet-tested",
        final_status="verified",
        branch_risk="input variable; depends on enclosing witness",
        extended_real_risk="input variable; depends on enclosing witness",
        reference=lambda x: x,
        dependency_witness="input variable",
    ),
    "y": Witness(
        primitive="y",
        primitive_type="constant",
        table1_category=_category("y"),
        expression=Y,
        source="paper Table 1, page 6",
        domain=Domain.SOURCE_DEPENDENT,
        dependencies=(),
        symbolic_status="verified",
        numeric_status="verified",
        edge_case_status="not-yet-tested",
        final_status="verified",
        branch_risk="input variable; depends on enclosing witness",
        extended_real_risk="input variable; depends on enclosing witness",
        reference=lambda y: y,
        dependency_witness="input variable",
    ),
    "e": Witness(
        primitive="e",
        primitive_type="constant",
        table1_category=_category("e"),
        expression=EML(ONE, ONE),
        source="main paper abstract/example; SI Table S2 step 1",
        domain=Domain.POSITIVE_REAL,
        dependencies=("one",),
        symbolic_status="verified",
        numeric_status="verified",
        edge_case_status="verified",
        final_status="verified",
        branch_risk="none",
        extended_real_risk="none",
        reference=lambda: mp.e,
        dependency_witness="eml(1, 1)",
    ),
    "exp": Witness(
        primitive="exp",
        primitive_type="unary",
        table1_category=_category("exp"),
        expression=exp_expr(X),
        source="main paper abstract/example; SI Table S2 step 2",
        domain=Domain.POSITIVE_REAL,
        dependencies=("one",),
        symbolic_status="verified",
        numeric_status="verified",
        edge_case_status="not-yet-tested",
        final_status="verified",
        branch_risk="none for this identity",
        extended_real_risk="overflow backend-dependent for finite precision",
        reference=mp.exp,
        dependency_witness="eml(x, 1)",
    ),
    "ln": Witness(
        primitive="ln",
        primitive_type="unary",
        table1_category=_category("ln"),
        expression=ln_expr(X),
        source="main paper abstract/example; SI Table S2 step 3",
        domain=Domain.POSITIVE_REAL,
        dependencies=("one", "exp"),
        symbolic_status="verified",
        numeric_status="verified",
        edge_case_status="partially-reproduced",
        final_status="verified",
        branch_risk="requires branch convention outside positive reals",
        extended_real_risk="log(0) depends on extended-real/backend convention",
        reference=mp.log,
        dependency_witness="eml(1, exp(eml(1, x)))",
        branch_convention="principal target; author uses LogLower inside EML to align negative real axis",
    ),
    "zero": Witness(
        primitive="zero",
        primitive_type="constant",
        table1_category="support",
        expression=ln_expr(ONE),
        source="repo Mathematica chain zeroEML line 22; support primitive not in Table 1",
        domain=Domain.POSITIVE_REAL,
        dependencies=("one", "ln"),
        symbolic_status="verified",
        numeric_status="reproduced-numerically",
        edge_case_status="not-yet-tested",
        final_status="reproduced-numerically",
        branch_risk="none for ln(1)",
        extended_real_risk="none for this witness",
        reference=lambda: mp.mpf(0),
        dependency_witness="ln(1)",
        table1=False,
    ),
    "neg_one": Witness(
        primitive="neg_one",
        primitive_type="constant",
        table1_category=_category("neg_one"),
        expression=None,
        source="SI Table S2 step 5; repo Mathematica chain negEML line 23",
        domain=Domain.POSITIVE_REAL,
        dependencies=("ln", "sub", "one"),
        symbolic_status="verified",
        numeric_status="reproduced-numerically",
        edge_case_status="partially-reproduced",
        final_status="reproduced-numerically",
        branch_risk="inherits subtraction/zero branch assumptions",
        extended_real_risk="derived sign flip may rely on log(0) in fully inlined form",
        reference=lambda: mp.mpf(-1),
        dependency_witness="ln(1) - 1",
        uses_extended_real=True,
        generated_constants=("zero",),
    ),
    "two": Witness(
        primitive="two",
        primitive_type="constant",
        table1_category=_category("two"),
        expression=None,
        source="SI Table S2 step 6; repo Mathematica chain twoEML line 24",
        domain=Domain.POSITIVE_REAL,
        dependencies=("one", "neg_one", "sub"),
        symbolic_status="verified",
        numeric_status="reproduced-numerically",
        edge_case_status="not-yet-tested",
        final_status="reproduced-numerically",
        branch_risk="inherits subtraction branch assumptions",
        extended_real_risk="inherits neg_one construction risk",
        reference=lambda: mp.mpf(2),
        dependency_witness="1 - (-1)",
        generated_constants=("neg_one",),
    ),
    "sub": Witness(
        primitive="sub",
        primitive_type="binary",
        table1_category=_category("sub"),
        expression=None,
        source="SI Table S2 step 4; repo Mathematica chain subtractEML line 27",
        domain=Domain.POSITIVE_REAL,
        dependencies=("ln", "exp"),
        symbolic_status="verified",
        numeric_status="reproduced-numerically",
        edge_case_status="not-yet-tested",
        final_status="reproduced-numerically",
        branch_risk="Log(exp(y)) requires y in principal strip; real y is safe",
        extended_real_risk="first argument zero triggers log(0) in naive inlining",
        reference=lambda x, y: x - y,
        dependency_witness="eml(ln(x), exp(y))",
    ),
    "minus": Witness(
        primitive="minus",
        primitive_type="unary",
        table1_category=_category("minus"),
        expression=None,
        source="SI Table S2 step 7; repo Mathematica chain minusEML line 28",
        domain=Domain.POSITIVE_REAL,
        dependencies=("zero", "sub"),
        symbolic_status="verified",
        numeric_status="reproduced-numerically",
        edge_case_status="partially-reproduced",
        final_status="partially-reproduced",
        branch_risk="inherits subtraction branch assumptions",
        extended_real_risk="fully inlined EML form can depend on log(0)",
        reference=lambda x: -x,
        dependency_witness="ln(1) - x",
        uses_extended_real=True,
        generated_constants=("zero",),
    ),
    "add": Witness(
        primitive="add",
        primitive_type="binary",
        table1_category=_category("add"),
        expression=None,
        source="SI Table S2 step 8; repo Mathematica chain plusEML line 29",
        domain=Domain.POSITIVE_REAL,
        dependencies=("sub", "minus"),
        symbolic_status="verified",
        numeric_status="reproduced-numerically",
        edge_case_status="partially-reproduced",
        final_status="partially-reproduced",
        branch_risk="inherits sign flip and subtraction assumptions",
        extended_real_risk="inherits minus/zero construction risk",
        reference=lambda x, y: x + y,
        dependency_witness="x - (-y)",
        uses_extended_real=True,
    ),
    "inv": Witness(
        primitive="inv",
        primitive_type="unary",
        table1_category=_category("inv"),
        expression=None,
        source="SI Table S2 step 9; repo Mathematica chain invEML line 30",
        domain=Domain.POSITIVE_REAL,
        dependencies=("exp", "minus", "ln"),
        symbolic_status="verified",
        numeric_status="reproduced-numerically",
        edge_case_status="not-yet-tested",
        final_status="reproduced-numerically",
        branch_risk="complex reciprocal via log is branch-sensitive",
        extended_real_risk="x=0 excluded",
        reference=lambda x: 1 / x,
        dependency_witness="exp(-ln(x))",
    ),
    "mul": Witness(
        primitive="mul",
        primitive_type="binary",
        table1_category=_category("mul"),
        expression=None,
        source="SI Table S2 step 10; repo Mathematica chain timesEML line 31",
        domain=Domain.POSITIVE_REAL,
        dependencies=("exp", "ln", "add"),
        symbolic_status="verified",
        numeric_status="reproduced-numerically",
        edge_case_status="partially-reproduced",
        final_status="partially-reproduced",
        branch_risk="complex logarithm additivity is branch-sensitive",
        extended_real_risk="zero inputs need separate handling",
        reference=lambda x, y: x * y,
        dependency_witness="exp(ln(x) + ln(y))",
    ),
    "sqr": Witness(
        primitive="sqr",
        primitive_type="unary",
        table1_category=_category("sqr"),
        expression=None,
        source="SI Table S2 step 11; repo Mathematica chain sqrEML line 32",
        domain=Domain.POSITIVE_REAL,
        dependencies=("mul",),
        symbolic_status="verified",
        numeric_status="reproduced-numerically",
        edge_case_status="not-yet-tested",
        final_status="reproduced-numerically",
        branch_risk="inherits multiplication branch assumptions",
        extended_real_risk="none on positive reals",
        reference=lambda x: x * x,
        dependency_witness="x * x",
    ),
    "div": Witness(
        primitive="div",
        primitive_type="binary",
        table1_category=_category("div"),
        expression=None,
        source="SI Table S2 step 12; repo Mathematica chain divideEML line 33",
        domain=Domain.POSITIVE_REAL,
        dependencies=("mul", "inv"),
        symbolic_status="verified",
        numeric_status="reproduced-numerically",
        edge_case_status="not-yet-tested",
        final_status="reproduced-numerically",
        branch_risk="complex logarithm subtraction is branch-sensitive",
        extended_real_risk="division by zero excluded",
        reference=lambda x, y: x / y,
        dependency_witness="x * inv(y)",
    ),
    "half": Witness(
        primitive="half",
        primitive_type="unary",
        table1_category=_category("half"),
        expression=None,
        source="SI Table S2 step 13; repo Mathematica chain halfEML line 34",
        domain=Domain.POSITIVE_REAL,
        dependencies=("div", "two"),
        symbolic_status="verified",
        numeric_status="reproduced-numerically",
        edge_case_status="not-yet-tested",
        final_status="reproduced-numerically",
        branch_risk="inherits division assumptions",
        extended_real_risk="inherits two construction risk",
        reference=lambda x: x / 2,
        dependency_witness="x / 2",
        generated_constants=("two",),
    ),
    "avg": Witness(
        primitive="avg",
        primitive_type="binary",
        table1_category=_category("avg"),
        expression=None,
        source="SI Table S2 step 14; repo Mathematica chain avgEML line 35",
        domain=Domain.POSITIVE_REAL,
        dependencies=("half", "add"),
        symbolic_status="verified",
        numeric_status="reproduced-numerically",
        edge_case_status="partially-reproduced",
        final_status="partially-reproduced",
        branch_risk="inherits addition assumptions",
        extended_real_risk="inherits add/half construction risk",
        reference=lambda x, y: (x + y) / 2,
        dependency_witness="half(x + y)",
    ),
    "sqrt": Witness(
        primitive="sqrt",
        primitive_type="unary",
        table1_category=_category("sqrt"),
        expression=None,
        source="SI Table S2 step 15; repo Mathematica chain sqrtEML line 38",
        domain=Domain.POSITIVE_REAL,
        dependencies=("exp", "half", "ln"),
        symbolic_status="verified",
        numeric_status="reproduced-numerically",
        edge_case_status="not-yet-tested",
        final_status="reproduced-numerically",
        branch_risk="principal square root for complex inputs",
        extended_real_risk="x=0 edge not covered by positive-real pass",
        reference=mp.sqrt,
        dependency_witness="exp(half(ln(x)))",
    ),
    "pow": Witness(
        primitive="pow",
        primitive_type="binary",
        table1_category=_category("pow"),
        expression=None,
        source="SI Table S2 step 16; repo Mathematica chain powerEML line 39",
        domain=Domain.POSITIVE_REAL,
        dependencies=("exp", "mul", "ln"),
        symbolic_status="verified",
        numeric_status="reproduced-numerically",
        edge_case_status="not-yet-tested",
        final_status="reproduced-numerically",
        branch_risk="principal power is branch-sensitive for complex/negative bases",
        extended_real_risk="zero base and nonpositive exponent require exclusions",
        reference=lambda x, y: mp.power(x, y),
        dependency_witness="exp(y * ln(x))",
    ),
    "log_base": Witness(
        primitive="log_base",
        primitive_type="binary",
        table1_category=_category("log_base"),
        expression=None,
        source="SI Table S2 step 17; repo Mathematica chain logaritmEML line 40",
        domain=Domain.POSITIVE_REAL,
        dependencies=("ln", "div"),
        symbolic_status="verified",
        numeric_status="reproduced-numerically",
        edge_case_status="not-yet-tested",
        final_status="reproduced-numerically",
        branch_risk="complex logarithm quotient is branch-sensitive",
        extended_real_risk="base 1 and nonpositive inputs excluded",
        reference=lambda base, x: mp.log(x) / mp.log(base),
        dependency_witness="ln(y) / ln(x)",
    ),
    "pi": Witness(
        primitive="pi",
        primitive_type="constant",
        table1_category=_category("pi"),
        expression=None,
        source="SI Table S2 step 18; repo Mathematica chain piConst line 37",
        domain=Domain.COMPLEX_BRANCH_SENSITIVE,
        dependencies=("ln", "neg_one", "i", "div"),
        symbolic_status="verified",
        numeric_status="not-yet-tested",
        edge_case_status="blocked-by-branch-semantics",
        final_status="blocked-by-branch-semantics",
        branch_risk="depends on sign of log(-1) and i construction",
        extended_real_risk="inherits neg_one construction risk",
        reference=lambda: mp.pi,
        dependency_witness="sqrt(-(ln(-1))^2) in SI Table S2; piConst = logEML[-1] / iConst in repo",
        branch_convention="author LogLower plus principal target; compiler may manually correct i sign",
        generated_constants=("neg_one", "i"),
    ),
    "i": Witness(
        primitive="i",
        primitive_type="constant",
        table1_category=_category("i"),
        expression=None,
        source="repo Mathematica chain iConst line 36; compiler v4 lines 50-58",
        domain=Domain.COMPLEX_BRANCH_SENSITIVE,
        dependencies=("ln", "neg_one", "half", "exp"),
        symbolic_status="verified",
        numeric_status="not-yet-tested",
        edge_case_status="blocked-by-branch-semantics",
        final_status="blocked-by-branch-semantics",
        branch_risk="sign changes under branch convention; compiler v4 manually negates one form",
        extended_real_risk="inherits neg_one construction risk",
        reference=lambda: mp.j,
        dependency_witness="exp(half(ln(-1))) in repo Mathematica; compiler uses -exp(log(-1)/2) to correct sign in another convention",
        branch_convention="branch-sensitive: LogLower is required in Mathematica chain",
        generated_constants=("neg_one",),
    ),
    "hypot": Witness(
        primitive="hypot",
        primitive_type="binary",
        table1_category=_category("hypot"),
        expression=None,
        source="SI Table S2 step 19; repo Mathematica chain hypotEML line 41",
        domain=Domain.POSITIVE_REAL,
        dependencies=("sqrt", "add", "sqr"),
        symbolic_status="verified",
        numeric_status="reproduced-numerically",
        edge_case_status="not-yet-tested",
        final_status="reproduced-numerically",
        branch_risk="principal sqrt for complex inputs",
        extended_real_risk="none on positive real samples",
        reference=lambda x, y: mp.sqrt(x * x + y * y),
        dependency_witness="sqrt(x^2 + y^2)",
    ),
    "sigmoid": Witness(
        primitive="sigmoid",
        primitive_type="unary",
        table1_category=_category("sigmoid"),
        expression=None,
        source="SI Table S2 step 20; repo Mathematica chain logisticSigmoidEML line 42",
        domain=Domain.POSITIVE_REAL,
        dependencies=("inv", "minus", "exp"),
        symbolic_status="verified",
        numeric_status="not-yet-tested",
        edge_case_status="not-yet-tested",
        final_status="not-yet-tested",
        branch_risk="low on reals",
        extended_real_risk="inherits minus construction risk",
        reference=lambda x: 1 / (1 + mp.exp(-x)),
        dependency_witness="1 / eml(-x, exp(-1))",
    ),
    "cosh": Witness("cosh", "unary", _category("cosh"), None, "SI Table S2 step 21; repo Mathematica chain coshEML line 43", Domain.POSITIVE_REAL, ("avg", "exp", "minus"), "verified", "not-yet-tested", "not-yet-tested", "not-yet-tested", "low on reals", "inherits avg/minus construction risk", mp.cosh, "avg(exp(x), exp(-x))"),
    "sinh": Witness("sinh", "unary", _category("sinh"), None, "SI Table S2 step 22; repo Mathematica chain sinhEML line 44", Domain.POSITIVE_REAL, ("eml", "exp", "cosh"), "verified", "not-yet-tested", "not-yet-tested", "not-yet-tested", "low on reals", "none on finite positive samples", mp.sinh, "eml(x, exp(cosh(x)))"),
    "tanh": Witness("tanh", "unary", _category("tanh"), None, "SI Table S2 step 23; repo Mathematica chain tanhEML line 46", Domain.POSITIVE_REAL, ("sinh", "cosh", "div"), "verified", "not-yet-tested", "not-yet-tested", "not-yet-tested", "poles where cosh is zero in complex domain", "none on reals", mp.tanh, "sinh(x) / cosh(x)"),
    "cos": Witness("cos", "unary", _category("cos"), None, "SI Table S2 step 24; repo Mathematica chain cosEML line 45", Domain.COMPLEX_BRANCH_SENSITIVE, ("cosh", "div", "i"), "verified", "not-yet-tested", "blocked-by-branch-semantics", "blocked-by-branch-semantics", "requires i branch/sign", "inherits i construction risk", mp.cos, "cosh(x / i)", "author LogLower plus i sign convention", False, ("i",)),
    "sin": Witness("sin", "unary", _category("sin"), None, "SI Table S2 step 25; repo Mathematica chain sinEML line 48", Domain.COMPLEX_BRANCH_SENSITIVE, ("cos", "sub", "half", "pi"), "verified", "not-yet-tested", "blocked-by-branch-semantics", "blocked-by-branch-semantics", "requires pi/i branch/sign", "inherits pi construction risk", mp.sin, "cos(x - pi/2)", "author LogLower plus pi/i sign convention", False, ("pi",)),
    "tan": Witness("tan", "unary", _category("tan"), None, "SI Table S2 step 26; repo Mathematica chain tanEML line 47", Domain.COMPLEX_BRANCH_SENSITIVE, ("sin", "cos", "div"), "verified", "not-yet-tested", "blocked-by-branch-semantics", "blocked-by-branch-semantics", "inherits sin/cos branch requirements and excludes poles", "none away from poles", mp.tan, "sin(x) / cos(x)"),
    "arsinh": Witness("arsinh", "unary", _category("arsinh"), None, "SI Table S2 step 27; repo Mathematica chain arcSinhEML line 49", Domain.COMPLEX_BRANCH_SENSITIVE, ("ln", "add", "hypot", "neg_one"), "verified", "not-yet-tested", "blocked-by-branch-semantics", "blocked-by-branch-semantics", "principal log/sqrt branch-sensitive", "inherits neg_one construction risk", mp.asinh, "ln(x + hypot(-1, x))"),
    "arcosh": Witness("arcosh", "unary", _category("arcosh"), None, "SI Table S2 step 28; repo Mathematica chain arcCoshEML line 50", Domain.COMPLEX_BRANCH_SENSITIVE, ("arsinh", "hypot", "i"), "verified", "not-yet-tested", "blocked-by-branch-semantics", "blocked-by-branch-semantics", "principal acosh branch and i sign", "inherits i construction risk", mp.acosh, "arsinh(hypot(x, sqrt(-1)))", "author LogLower plus i sign convention", False, ("i",)),
    "arccos": Witness("arccos", "unary", _category("arccos"), None, "SI Table S2 step 29; repo Mathematica chain arcCosEML line 51", Domain.COMPLEX_BRANCH_SENSITIVE, ("arcosh", "cos"), "verified", "not-yet-tested", "blocked-by-branch-semantics", "blocked-by-branch-semantics", "principal inverse trig branch-sensitive", "inherits arcosh/cos branch risk", mp.acos, "arcosh(cos(arcosh(x)))"),
    "artanh": Witness("artanh", "unary", _category("artanh"), None, "SI Table S2 step 30; repo Mathematica chain arcTanhEML line 53", Domain.COMPLEX_BRANCH_SENSITIVE, ("arsinh", "tan", "arccos", "inv"), "verified", "not-yet-tested", "blocked-by-branch-semantics", "blocked-by-branch-semantics", "principal inverse hyperbolic branch-sensitive", "inherits tan/arccos branch risk", mp.atanh, "arsinh(1 / tan(arccos(x)))"),
    "arcsin": Witness("arcsin", "unary", _category("arcsin"), None, "SI Table S2 step 31; repo Mathematica chain arcSinEML line 52", Domain.COMPLEX_BRANCH_SENSITIVE, ("pi", "half", "sub", "arccos"), "verified", "not-yet-tested", "blocked-by-branch-semantics", "blocked-by-branch-semantics", "principal inverse trig branch-sensitive", "inherits pi/arccos branch risk", mp.asin, "pi/2 - arccos(x)", "author LogLower plus pi sign convention", False, ("pi",)),
    "arctan": Witness("arctan", "unary", _category("arctan"), None, "SI Table S2 step 32; repo Mathematica chain arcTanEML line 54", Domain.COMPLEX_BRANCH_SENSITIVE, ("arcsin", "tanh", "arsinh"), "verified", "not-yet-tested", "blocked-by-branch-semantics", "blocked-by-branch-semantics", "principal inverse trig branch-sensitive", "inherits arcsin branch risk", mp.atan, "arcsin(tanh(arsinh(x)))"),
}


_BRANCH_METADATA = {
    "i": dict(
        requires_loglower=True,
        principal_log_expected_to_fail=True,
        branch_failure_mode="principal-log dependency chain returns -i; LogLower returns +i",
        safe_real_domain="constant",
        safe_complex_domain="constant",
        extended_real_required=False,
        principal_log_status="blocked-by-branch-semantics",
        loglower_status="reproduced-numerically",
        numpy_principal_status="reproduced-numerically",
        numeric_status="reproduced-numerically",
        final_status="reproduced-numerically",
    ),
    "pi": dict(
        branch_failure_mode="sign-stable when log(-1) and i are constructed consistently",
        safe_real_domain="constant",
        safe_complex_domain="constant",
        principal_log_status="reproduced-numerically",
        loglower_status="reproduced-numerically",
        numpy_principal_status="reproduced-numerically",
        numeric_status="reproduced-numerically",
        final_status="reproduced-numerically",
    ),
    "cos": dict(
        branch_failure_mode="i sign cancels in cosh(x / i) on tested real samples",
        safe_real_domain="real x",
        safe_complex_domain="not yet tested",
        principal_log_status="reproduced-numerically",
        loglower_status="reproduced-numerically",
        numpy_principal_status="reproduced-numerically",
        numeric_status="reproduced-numerically",
        final_status="reproduced-numerically",
    ),
    "sin": dict(
        branch_failure_mode="depends on pi; tested real samples pass once pi is sign-stable",
        safe_real_domain="real x",
        safe_complex_domain="not yet tested",
        principal_log_status="reproduced-numerically",
        loglower_status="reproduced-numerically",
        numpy_principal_status="reproduced-numerically",
        numeric_status="reproduced-numerically",
        final_status="reproduced-numerically",
    ),
    "tan": dict(
        branch_failure_mode="inherits sin/cos and excludes tangent poles",
        safe_real_domain="real x with cos(x) != 0",
        safe_complex_domain="not yet tested",
        principal_log_status="reproduced-numerically",
        loglower_status="reproduced-numerically",
        numpy_principal_status="reproduced-numerically",
        numeric_status="reproduced-numerically",
        final_status="reproduced-numerically",
    ),
    "arsinh": dict(
        branch_failure_mode="tested real samples pass under both branches",
        safe_real_domain="real x",
        safe_complex_domain="not yet tested",
        principal_log_status="reproduced-numerically",
        loglower_status="reproduced-numerically",
        numeric_status="reproduced-numerically",
        final_status="reproduced-numerically",
    ),
    "arcosh": dict(
        branch_failure_mode="x > 1 passes, but the derived witness is not principal acosh on the full internal branch-cut domain",
        safe_real_domain="real x > 1",
        safe_complex_domain="not yet tested",
        principal_log_status="reproduced-numerically",
        loglower_status="reproduced-numerically",
        numeric_status="reproduced-numerically",
        final_status="reproduced-numerically",
        ordinary_real_domain_status="reproduced-numerically for x > 1",
        internal_branch_cut_status="blocked as a principal acosh dependency inside arccos",
        interval_neg1_1_status="LogLower matches principal only on [0,1); negative interior samples choose acos(abs(x)) sheet",
        below_negative_one_status="misses the +i*pi principal acosh sheet",
        safe_as_arccos_dependency="no: safe x > 1 result does not justify internal use on (-1,1)",
        branch_sheet_notes="ArcSinh[Sqrt[x^2-1]] is checked by author only for x >= 1; using it as internal acosh on (-1,1) changes sheets",
        outward_domain_status="outward-valid on real x > 1",
        internal_compositional_status="compositionally-unsafe as principal acosh inside arccos",
        compositionally_unsafe_domains="(-1,0) and x < -1 under principal acosh comparison",
        used_in_arccos_internal_interval=True,
        principal_arcosh_helper_available=True,
        principal_arcosh_helper_source_status="diagnostic-only; matches DLMF/mpmath principal acosh but is not an EML-derived witness",
    ),
    "sigmoid": dict(
        numeric_status="reproduced-numerically",
        edge_case_status="not-yet-tested",
        final_status="reproduced-numerically",
        safe_real_domain="tested on deterministic real samples -3..3",
    ),
    "cosh": dict(
        numeric_status="reproduced-numerically",
        edge_case_status="not-yet-tested",
        final_status="reproduced-numerically",
        safe_real_domain="tested on deterministic real samples -3..3",
    ),
    "sinh": dict(
        numeric_status="reproduced-numerically",
        edge_case_status="not-yet-tested",
        final_status="reproduced-numerically",
        safe_real_domain="tested on deterministic real samples -3..3",
    ),
    "tanh": dict(
        numeric_status="reproduced-numerically",
        edge_case_status="not-yet-tested",
        final_status="reproduced-numerically",
        safe_real_domain="tested on deterministic real samples -3..3",
    ),
    "arccos": dict(
        principal_log_expected_to_fail=True,
        branch_failure_mode="negative real samples return the complementary/absolute-value branch in Python dependency-chain reproduction",
        safe_real_domain="partially: positive samples in (0, 1) pass; negative samples fail",
        safe_complex_domain="not yet tested",
        principal_log_status="blocked-by-branch-semantics",
        loglower_status="blocked-by-branch-semantics",
        numpy_principal_status="not-yet-tested",
        requires_signed_zero_or_side_of_cut=True,
        requires_square_root_branch_control=True,
        requires_mathematica_branch_rules=True,
        failure_region="real x in (-1, 0)",
        observed_failure_mode="returns acos(abs(x)) on negative real samples",
        unwinding_offset_observed="sample-dependent offset, not a constant pi*k or 2*pi*i*k",
        author_reference_status="Mathematica chain asserts FullSimplify to ArcCos[x] under -1 <= x <= 1",
        python_reproduction_status="blocked under principal mpmath and LogLower dependency-chain evaluation",
        unsafe_real_domain="-1 < x < 0",
        branch_sheet_notes="arcosh(cos(arcosh(x))) composes sqrt/log branches; Python follows the wrong arcosh square-root sheet for negative inputs",
        root_blocker="derived arcosh internal branch behavior",
        inherited_from="root blocker",
        branch_dependency="first arcosh(x) in ArcCosh[Cos[ArcCosh[x]]] on x in (-1,0)",
        repair_attempted="no",
        repair_status="not attempted; diagnosis only",
        source_justification="author phase-2 proof uses built-in Mathematica ArcCosh for ArcCos witness; derived ArcCosh witness was checked only on x >= 1",
        source_chain_type="named-function Mathematica phase-2 proof; fully derived EML function exists but is not substituted in the proof check",
        named_function_reproduction_status="passes with direct mpmath acosh(cos(acosh(x)))",
        dependency_chain_reproduction_status="fails on x in (-1,0), returning acos(abs(x))",
        internal_helper_reproduction_status="passes diagnostically when the first internal arcosh is principal",
        final_branch_verdict="diagnostic-only repair; full dependency-chain reproduction remains branch-blocked",
        final_status="partially-reproduced",
    ),
    "arcsin": dict(
        principal_log_expected_to_fail=True,
        branch_failure_mode="negative real samples have wrong sign because arccos branch is wrong there",
        safe_real_domain="partially: positive samples in (0, 1) pass; negative samples fail",
        safe_complex_domain="not yet tested",
        principal_log_status="blocked-by-branch-semantics",
        loglower_status="blocked-by-branch-semantics",
        numpy_principal_status="not-yet-tested",
        requires_signed_zero_or_side_of_cut=True,
        requires_square_root_branch_control=True,
        requires_mathematica_branch_rules=True,
        failure_region="real x in (-1, 0)",
        observed_failure_mode="sign flip on negative real samples",
        unwinding_offset_observed="sign flip inherited from arccos, not a constant additive branch offset",
        author_reference_status="Mathematica chain defines ArcSin through Pi/2 - ArcCos[x] and asserts ArcSin[x]",
        python_reproduction_status="blocked under principal mpmath and LogLower dependency-chain evaluation for negative reals",
        unsafe_real_domain="-1 < x < 0",
        branch_sheet_notes="inherits arccos branch sheet; no independent source gap observed",
        root_blocker="derived arcosh internal branch behavior",
        inherited_from="arccos",
        branch_dependency="Pi/2 - arccos(x)",
        repair_attempted="no",
        repair_status="not attempted; remains inherited",
        source_justification="accepted phase-2/Rust witness depends on ArcCos; no separate repair before arccos is fixed",
        source_chain_type="depends on accepted arccos witness",
        named_function_reproduction_status="passes as pi/2 - named arccos",
        dependency_chain_reproduction_status="fails by inherited arccos sign/sheet issue",
        internal_helper_reproduction_status="passes diagnostically through arccos helper",
        final_branch_verdict="source-ambiguous inherited blocker; no independent repair",
    ),
    "artanh": dict(
        principal_log_expected_to_fail=True,
        branch_failure_mode="negative real samples have wrong sign through arccos/tan dependency chain",
        safe_real_domain="partially: positive samples in (0, 1) pass; negative samples fail",
        safe_complex_domain="not yet tested",
        principal_log_status="blocked-by-branch-semantics",
        loglower_status="blocked-by-branch-semantics",
        numpy_principal_status="not-yet-tested",
        requires_signed_zero_or_side_of_cut=True,
        requires_square_root_branch_control=True,
        requires_mathematica_branch_rules=True,
        failure_region="real x in (-1, 0)",
        observed_failure_mode="sign flip on negative real samples",
        unwinding_offset_observed="sign flip inherited through tan(arccos(x)), not a constant additive branch offset",
        author_reference_status="Mathematica chain asserts ArcTanh[x] from ArcSinh[1/Tan[ArcCos[x]]] under -1 < x < 1",
        python_reproduction_status="blocked under principal mpmath and LogLower dependency-chain evaluation for negative reals",
        unsafe_real_domain="-1 < x < 0",
        branch_sheet_notes="depends on arccos branch sheet before tan and arsinh are applied",
        root_blocker="derived arcosh internal branch behavior",
        inherited_from="arccos",
        branch_dependency="ArcSinh[1/Tan[ArcCos[x]]]",
        repair_attempted="no",
        repair_status="not attempted; remains inherited",
        source_justification="accepted phase-2/Rust witness depends on ArcCos; no separate repair before arccos is fixed",
        source_chain_type="depends on accepted arccos witness",
        named_function_reproduction_status="passes with named ArcCos in the source chain",
        dependency_chain_reproduction_status="fails by inherited arccos sheet issue",
        internal_helper_reproduction_status="passes diagnostically through arccos helper",
        final_branch_verdict="source-ambiguous inherited blocker; no independent repair",
    ),
    "arctan": dict(
        principal_log_expected_to_fail=True,
        branch_failure_mode="negative real samples have wrong sign through arcsin dependency chain; zero is numerically unstable",
        safe_real_domain="partially: positive samples pass; negative samples fail",
        safe_complex_domain="not yet tested",
        principal_log_status="blocked-by-branch-semantics",
        loglower_status="blocked-by-branch-semantics",
        numpy_principal_status="not-yet-tested",
        requires_signed_zero_or_side_of_cut=True,
        requires_square_root_branch_control=True,
        requires_mathematica_branch_rules=True,
        failure_region="real x < 0; x = 0 has tiny complex roundoff residual",
        observed_failure_mode="sign flip on negative real samples",
        unwinding_offset_observed="sample-dependent sign flip, not a constant pi*k offset",
        author_reference_status="Mathematica chain asserts ArcTan[x] from ArcSin[Tanh[ArcSinh[x]]] on real x",
        python_reproduction_status="blocked under principal mpmath and LogLower dependency-chain evaluation for negative reals",
        unsafe_real_domain="x < 0",
        branch_sheet_notes="inherits arcsin branch sheet after tanh(arsinh(x)); exact zero also needs stronger exact/signed-zero semantics",
        root_blocker="derived arcosh internal branch behavior",
        inherited_from="arcsin, which inherits from arccos",
        branch_dependency="ArcSin[Tanh[ArcSinh[x]]]",
        repair_attempted="no",
        repair_status="not attempted; remains inherited",
        source_justification="accepted phase-2/Rust witness depends on ArcSin; no separate repair before arccos/arcsin are fixed",
        source_chain_type="depends on arcsin, which depends on arccos",
        named_function_reproduction_status="passes with named ArcSin/ArcSinh/Tanh chain",
        dependency_chain_reproduction_status="fails by inherited arcsin/arccos sheet issue",
        internal_helper_reproduction_status="passes diagnostically through arccos-derived helper chain",
        final_branch_verdict="source-ambiguous inherited blocker; no independent repair",
    ),
}

for _name, _meta in _BRANCH_METADATA.items():
    WITNESSES[_name] = replace(WITNESSES[_name], **_meta)


ALIASES = {
    "1": "one",
    "0": "zero",
    "-1": "neg_one",
    "neg": "minus",
}


def get_witness(name: str) -> Witness:
    return WITNESSES[ALIASES.get(name, name)]


def table1_witnesses() -> dict[str, Witness]:
    return {name: witness for name, witness in WITNESSES.items() if witness.table1}

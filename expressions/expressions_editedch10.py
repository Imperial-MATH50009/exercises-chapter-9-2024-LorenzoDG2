"""."""

import numbers
from functools import singledispatch, wraps

def make_other_expr(meth):
    @wraps(meth)
    def fn(self, other):  # replacement for __add__ so takes same args as __add__ method
        if isinstance(other, numbers.Number):  # Number in numbers
            other = Number(other)  # custom Number class I made
        return meth(self,other)
    return fn

class Expression:
    #  Base Class
    """."""

    def __init__(self, *operands):
        self.operands = operands

    @make_other_expr
    def __add__(self, other):
        return Add(self, other)  # first try

    def __radd__(self, other):
        if isinstance(other, numbers.Number):
            return Add(Number(other), self)

        return NotImplemented  # second chance- if this doesnt work- give up

    def __sub__(self, other):
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Sub(self, other)

    def __rsub__(self, other):
        if isinstance(other, numbers.Number):
            return Sub(Number(other), self)

        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Mul(self, other)

    def __rmul__(self, other):
        if isinstance(other, numbers.Number):
            return Mul(Number(other), self)

        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Div(self, other)

    def __rtruediv__(self, other):
        if isinstance(other, numbers.Number):
            return Div(Number(other), self)

        return NotImplemented

    def __pow__(self, other):
        if isinstance(other, numbers.Number):
            other = Number(other)

        return Pow(self, other)

    def __rpow__(self, other):

        if isinstance(other, numbers.Number):
            return Pow(Number(other), self)

        return NotImplemented


class Operator(Expression):   # Nodes with 2 children (binary operator)
    """."""

    def __repr__(self):
        return type(self).__name__ + repr(self.operands)

    def __str__(self):

        def paren(expr):
            if expr.precedence < self.precedence:
                return f"({expr!s})"
            else:
                return str(expr)

        return " ".join((paren(self.operands[0]),
                         self.symbol,
                         paren(self.operands[1])))


class Add(Operator):
    """."""

    precedence = 0
    symbol = "+"


class Sub(Operator):
    """."""

    precedence = 0
    symbol = "-"


class Mul(Operator):
    """."""

    precedence = 1
    symbol = "*"


class Div(Operator):
    """."""

    precedence = 1
    symbol = "/"


class Pow(Operator):
    """."""

    precedence = 2
    symbol = "^"


class Terminal(Expression):
    #  Nodes with no children
    """."""

    precedence = 3

    def __init__(self, value):
        self.value = value

        super().__init__()  # Calls parent class constructor.

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)


class Symbol(Terminal):
    """."""

    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError("Symbol value must be a string.")

        super().__init__(value)  # Calls parent class constructor w
# arg "value".
# Passes that value up the chain so Terminal can do: self.value = value
# super().__init__() which then calls Expression with no operands


class Number(Terminal):
    """."""

    def __init__(self, value):
        if not isinstance(value, numbers.Number):
            raise TypeError("Number value must be a number.")

        super().__init__(value)


def postvisitor(expr, fn, **kwargs):
    """."""
    stack = []
    visited = {}  # memoization dictionary: stores the result of fn(e, ...)
    # for each expression node e
    stack.append(expr)
    while stack:
        e = stack.pop()
        unvisited_children = []
        for o in e.operands:
            if o not in visited:
                unvisited_children.append(o)

        if unvisited_children:
            stack.append(e)
            for uc in unvisited_children:
                stack.append(uc)
        else:
            visited[e] = fn(e, *(visited[o] for o in e.operands), **kwargs)

    return visited[expr]


@singledispatch
def differentiate(expr, *o, **kwargs):  # Default behaviour.
    """."""
    raise NotImplementedError(
        f"Cannot differentiate a {type(expr).__name__}"
    )


@differentiate.register(Number)  # Constant differentiation --> 0
def _(expr, *o, **kwargs):
    return 0.0


@differentiate.register(Symbol)  # Symbol differentiation
def _(expr, *o, **kwargs):
    return 1 if kwargs["var"] == expr.value else 0.0  # Is this the symbol we
# are differentiating wrt yes-->1, no-->0


@differentiate.register(Add)
def _(expr, *o, **kwargs):
    return o[0] + o[1]


@differentiate.register(Sub)
def _(expr, *o, **kwargs):
    return o[0] - o[1]


@differentiate.register(Mul)
def _(expr, *o, **kwargs):
    return o[0]*expr.operands[1] + expr.operands[0]*o[1]


@differentiate.register(Div)
def _(expr, *o, **kwargs):
    return (o[0]*expr.operands[1] - expr.operands[0]*o[1])\
            / (expr.operands[1])**2


@differentiate.register(Pow)
def _(expr, *o, **kwargs):
    return expr.operands[1]*(expr.operands[0]**(expr.operands[1]-1))*o[0]

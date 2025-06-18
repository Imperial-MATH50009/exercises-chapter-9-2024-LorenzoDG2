import numbers

class Expression:  #  Base Class
    def __init__(self, *operands):
        self.operands = operands

    def __add__(self, other):
        if isinstance(other, numbers.Number):  # Number in numbers
            other = Number(other)  # custom Number class I made
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
    precedence = 0
    symbol = "+"


class Sub(Operator):
    precedence = 0
    symbol = "-"


class Mul(Operator):
    precedence = 1
    symbol = "*"


class Div(Operator):
    precedence = 1
    symbol = "/"


class Pow(Operator):
    precedence = 2
    symbol = "^"





class Terminal(Expression):    #  Nodes with no children
    precedence = 3
    def __init__(self, value):
        self.value = value

        super().__init__()

    def __repr__(self):
        return repr(self.value)
    
    def __str__(self):
        return str(self.value)


class Symbol(Terminal):
    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError("Symbol value must be a string.")

        super().__init__(value)

class Number(Terminal):
    def __init__(self, value):
        if not isinstance(value, numbers.Number):
            raise TypeError("Number value must be a number.")

        super().__init__(value)

def postvisitor():
    pass
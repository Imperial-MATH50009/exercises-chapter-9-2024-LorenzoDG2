from numbers import Number
from numbers import Integral


class Polynomial:

    def __init__(self, coefs):
        self.coefficients = coefs

    @property  # no brackets needed after p.degreee
    def degree(self):
        return len(self.coefficients) - 1

    def __str__(self):
        coefs = self.coefficients
        terms = []

        if coefs[0]:
            terms.append(str(coefs[0]))
        if self.degree() and coefs[1]:
            terms.append(f"{'' if coefs[1] == 1 else coefs[1]}x")

        terms += [f"{'' if c == 1 else c}x^{d}"
                  for d, c in enumerate(coefs[2:], start=2) if c]

        return " + ".join(reversed(terms)) or "0"

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.coefficients) + ")"

    def __eq__(self, other):

        return isinstance(other, Polynomial) and\
             self.coefficients == other.coefficients

    def __add__(self, other):

        if isinstance(other, Polynomial):
            common = min(self.degree(), other.degree()) + 1
            coefs = tuple(a + b for a, b in zip(self.coefficients,
                                                other.coefficients))
            coefs += self.coefficients[common:] + other.coefficients[common:]

            return Polynomial(coefs)

        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] + other,)
                              + self.coefficients[1:])

        else:
            return NotImplemented

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):

        if isinstance(other, Polynomial):
            common = min(self.degree(), other.degree()) + 1
            coefs = tuple(a - b for a, b in zip(self.coefficients,
                                                other.coefficients))
            coefs += self.coefficients[common:] + tuple([-x for x in other.coefficients[common:]]) 

            return Polynomial(coefs)

        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] - other,)
                              + self.coefficients[1:])

        else:
            return NotImplemented

    def __rsub__(self, other):
        return Polynomial( tuple([-x for x in (self-other).coefficients]))

    def __mul__(self, other):

        if isinstance(other, Polynomial):
            coefs=[0 for i in range(self.degree()+other.degree()+1)]
            for i in range(self.degree()+1):
                for j in range(other.degree()+1):
                    coefs[i+j]+= self.coefficients[i]*other.coefficients[j]
            return Polynomial(tuple(coefs))

        elif isinstance(other, Number):
            return Polynomial(tuple([other*x for x in self.coefficients]))

        else:
            return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __pow__(self, other):
        if isinstance(other, Integral) and other>0:
            if other == 1:
                return self
            else:
                return self * self**(other-1)

        else:
            return NotImplemented

    def __call__(self, x):
        if isinstance(x, Number):
            return sum([self.coefficients[i]*x**i for i in range(self.degree()+1)])

    def dx(self):
        if self.degree()==0:
            return Polynomial((0,))
        else:
            return Polynomial(tuple([self.coefficients[i]*i for i in range(1,self.degree()+1)]))

def derivative(p):
    return p.dx()
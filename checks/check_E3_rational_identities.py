#!/usr/bin/env python3
"""Exact polynomial identities, not finite coefficient fitting.

Run with a Python containing python-flint. All equalities are checked by
integer-polynomial arithmetic in Q(t).
"""
from flint import fmpz_poly


class Rat:
    def __init__(self, n, d=1):
        self.n = n if isinstance(n, fmpz_poly) else fmpz_poly([n])
        self.d = d if isinstance(d, fmpz_poly) else fmpz_poly([d])
        g = self.n.gcd(self.d)
        if g:
            self.n //= g
            self.d //= g

    @staticmethod
    def cast(x):
        return x if isinstance(x, Rat) else Rat(x)

    def __add__(self, other):
        o = self.cast(other)
        return Rat(self.n * o.d + o.n * self.d, self.d * o.d)

    __radd__ = __add__

    def __neg__(self):
        return Rat(-self.n, self.d)

    def __sub__(self, other):
        return self + -self.cast(other)

    def __rsub__(self, other):
        return self.cast(other) + -self

    def __mul__(self, other):
        o = self.cast(other)
        return Rat(self.n * o.n, self.d * o.d)

    __rmul__ = __mul__

    def __truediv__(self, other):
        o = self.cast(other)
        return Rat(self.n * o.d, self.d * o.n)

    def __rtruediv__(self, other):
        return self.cast(other) / self

    def __pow__(self, exponent):
        return Rat(self.n ** exponent, self.d ** exponent)

    def __eq__(self, other):
        o = self.cast(other)
        return self.n * o.d == o.n * self.d


t = Rat(fmpz_poly([0, 1]))
B = 2*t**4/(1-t**4) + t**6*(1+t**2)/(1-t**4)**2
U = B*(2-t**2)/(1-t**2) + t**2*(2+t+t**2+t**4)/(1-t**8)
V = (t**4/((1-t**2)*(1-t**4))
     + (t**3+t**4-3*t**6)/(1-t**8)
     - 4*t**10/((1-t**4)*(1-t**8)))

# E(t,y) = F(t,y)/(1-y) + t²(ty+t²y²)/(1-t⁸y⁴).
# Evaluate F and its y derivative exactly at y=1.
A1 = 2*t**2/(1-t**4) + 2*t**4*(1+t**2)/(1-t**4)**2
A0 = t**2*(1+t**2)/(1-t**4)**2
N1 = B - A1 + A0
Np1 = -2*A1 + 4*A0
assert Np1 == 0
assert N1 == -t**2/(1+t**2)
F1 = N1/(1-t**2) + t**2*(1+t**4)/(1-t**8)
assert F1 == 0
Fp1 = (t**2*N1/(1-t**2)**2 + Np1/(1-t**2)
       + t**2*(3*t**4/(1-t**8)
               + 4*t**8*(1+t**4)/(1-t**8)**2))
E_at_y1 = -Fp1 + t**2*(t+t**2)/(1-t**8)
assert E_at_y1 == V
print('PASS: exact cancellation of 1-y and symbolic specialization equals V(t).')

q = t**8
linear = [4, 2, 6, 8, 8, 6, 10, 12]
constant = [1, 1, 2, 3, 5, 3, 5, 7]
low = 2*t**2 + 3*t**3 + 5*t**4 + 3*t**5 + 5*t**6 + 7*t**7
eight_residue = low + q/(1-q)**3 * sum(
    t**r * (4*(1+q) + linear[r]*(1-q) + constant[r]*(1-q)**2)
    for r in range(8))
assert (1+t)*U-t*V == eight_residue
print('PASS: exact rational identity gives all eight quadratic formulas for every d>=1.')

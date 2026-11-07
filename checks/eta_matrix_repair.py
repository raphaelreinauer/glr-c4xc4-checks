#!/usr/bin/env python3
"""Exact eta repair research. No arbitrary BGS normalization is inserted.

See README.md for installation and execution instructions. The optional
symbolic audit uses SymPy and is enabled with `--symbolic`.
"""

from fractions import Fraction as F
from math import gcd, lcm
import sys

from flint import fmpz_mat

ROWS = ((0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2))
SLOPES = ((0, 1), (1, 1), (1, 3), (2, 1), (1, 0), (1, 2))


def integer_matrix(a, mixed):
    result = []
    for u, v in ROWS:
        row = []
        for s, t in SLOPES:
            r = (s * u + t * v) % 4
            row.extend((0, 0) if r == 0 else (2*a, 2*a) if r == 2 else (a+1, a-1))
        if mixed and u % 2 == v % 2 == 0:
            row = [F(1, 2)*z for z in row] if not isinstance(a, int) else [z // 2 for z in row]
        result.append(row)
    return result


def smith_data(q, mixed):
    a = 2 ** (q - 1)
    denominator = 2 * a*a
    smith = fmpz_mat(integer_matrix(a, mixed)).snf()
    diagonal = tuple(abs(int(smith[i, i])) for i in range(9))
    expected = (1, 1, 2, 2*a, 2*a, 4*a, 4*a, 4*a, 4*a) if mixed else (1, 1, 2, 4*a, 4*a, 4*a, 4*a, 4*a, 8*a)
    assert diagonal == expected, (a, mixed, diagonal)
    factors = tuple(denominator // gcd(denominator, z) for z in diagonal)
    logorder = sum(z.bit_length()-1 for z in factors)
    return diagonal, factors, logorder


def pair_add(a, b):
    return a[0]+b[0], a[1]+b[1]


def pair_mul(a, b):
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def pair_div(a, b):
    den = b[0]*b[0]+b[1]*b[1]
    return (a[0]*b[0]+a[1]*b[1])/den, (a[1]*b[0]-a[0]*b[1])/den


def i_power(j):
    return ((F(1), F(0)), (F(0), F(1)), (F(-1), F(0)), (F(0), F(-1)))[j % 4]


def lens_eta(weights, r):
    """Direct reduced-eta fixed-point sum for the specified spin lift."""
    assert len(weights) % 2 == 0 and sum(weights) % 2 == 0
    answer = F(0), F(0)
    for j in (1, 2, 3):
        numerator = pair_mul(i_power(j * sum(weights)//2), pair_add(i_power(j*r), (F(-1), F(0))))
        denominator = F(1), F(0)
        for w in weights:
            z = i_power(j*w)
            denominator = pair_mul(denominator, (1-z[0], -z[1]))
        answer = pair_add(answer, pair_div(numerator, denominator))
    assert answer[1] == 0
    return answer[0] / 4


def bundle_eta(m, r):
    """Fixed-point sum for S(H^2 + C^(m-1))/C4 with all weights one."""
    assert m % 2 == 0
    answer = F(0), F(0)
    for j in (1, 2, 3):
        z = i_power(j)
        numerator = pair_mul(i_power(j*m//2), pair_add((F(1), F(0)), z))
        numerator = pair_mul(numerator, pair_add(i_power(j*r), (F(-1), F(0))))
        denominator = F(1), F(0)
        for _ in range(m+1):
            denominator = pair_mul(denominator, (1-z[0], -z[1]))
        answer = pair_add(answer, pair_div(numerator, denominator))
    assert answer[1] == 0
    return answer[0] / 4


def verify_lens_tables():
    for m in range(2, 42, 2):
        x = F(1, 2 ** (m//2+1))
        sign = (-1) ** (m//2+1)
        for j in (0, 1):
            weights = [1] * (m-1) + [1+2*j]
            expected = (F(0), sign*(x+(-1)**j*2*x*x), sign*2*x, sign*(x+(-1)**j*2*x*x))
            actual = tuple(lens_eta(weights, r) for r in range(4))
            assert actual == expected, (m, j, actual, expected)
        expected_bundle = (F(0), sign*x, F(0), -sign*x)
        assert tuple(bundle_eta(m, r) for r in range(4)) == expected_bundle
    print('L3 all-one:', tuple(lens_eta([1, 1], r) for r in range(4)))
    print('L3 one-three:', tuple(lens_eta([1, 3], r) for r in range(4)))


def symbolic_audit(mixed):
    """Certify a universal 2-local diagonalization for every positive a=4t.

    Every elimination multiplier has an integer polynomial numerator and a
    denominator identically odd modulo two after setting a=4t. Each diagonal
    entry differs from its asserted 2-power factor by a universal 2-adic unit.
    Thus these are invertible operations over Z_(2), for every positive t.
    """
    import sympy as sp
    a = sp.Symbol('a')
    t = sp.Symbol('t')
    matrix = sp.Matrix(integer_matrix(a, mixed))
    multipliers = []
    swaps = []
    def universally_integral_at_two(expression):
        num, den = sp.fraction(sp.cancel(expression.subs(a, 4*t)))
        numerator = sp.Poly(num, t, domain=sp.ZZ)
        denominator = sp.Poly(den, t, domain=sp.ZZ)
        # Denominator is odd for every integer t, by coefficient parity.
        assert denominator.nth(0) % 2 == 1, expression
        assert all(denominator.nth(i) % 2 == 0
                   for i in range(1, denominator.degree()+1)), expression
        return True
    def v2(z):
        z = F(str(z))
        def one(n):
            n = abs(n)
            return (n & -n).bit_length()-1 if n else 10000
        return one(z.numerator)-one(z.denominator)
    pivots = []
    for k in range(9):
        _, i, j = min((v2(matrix[i, j].subs(a, 4)), i, j)
                      for i in range(k, 9) for j in range(k, 12) if matrix[i, j] != 0)
        swaps.append((k, i, j))
        matrix.row_swap(k, i)
        matrix.col_swap(k, j)
        pivot = sp.factor(matrix[k, k])
        pivots.append(pivot)
        for i in range(k+1, 9):
            if matrix[i, k] != 0:
                ratio = sp.factor(matrix[i, k] / pivot)
                assert universally_integral_at_two(ratio)
                multipliers.append(ratio)
                for j in range(k, 12):
                    matrix[i, j] = sp.cancel(matrix[i, j]-ratio*matrix[k, j])
        for j in range(k+1, 12):
            if matrix[k, j] != 0:
                ratio = sp.factor(matrix[k, j]/pivot)
                assert universally_integral_at_two(ratio)
                multipliers.append(ratio)
                for i in range(k, 9):
                    matrix[i, j] = sp.cancel(matrix[i, j]-ratio*matrix[i, k])
    expected = (1, 1, 2, 2*a, 2*a, 4*a, 4*a, 4*a, 4*a) if mixed else (1, 1, 2, 4*a, 4*a, 4*a, 4*a, 4*a, 8*a)
    for pivot, factor in zip(pivots, expected):
        quotient = sp.cancel(pivot/factor)
        assert universally_integral_at_two(quotient)
        assert universally_integral_at_two(1/quotient)
    assert all(sp.cancel(matrix[i, j] - (pivots[i] if i == j else 0)) == 0
               for i in range(9) for j in range(12))
    print('mixed periods:', mixed)
    print('pivot swaps (0-based k,row,column):', swaps)
    print('symbolic pivots:', pivots)
    print('unique elimination multipliers:', sorted(set(map(str, multipliers))))
    print('Universal 2-local diagonalization certified for every positive a divisible by four.')


def main():
    verify_lens_tables()
    for d in range(21):
        for residue in (3, 7):
            q = 2*d + (2 if residue == 3 else 3)
            diagonal, factors, logorder = smith_data(q, residue == 3)
            expected = 24*d + (10 if residue == 3 else 19)
            assert logorder == expected
            if d < 3:
                print(f'n={8*d+residue}: q={q}, Smith={diagonal}, image factors={factors}, log2={logorder}')
    print('All exact geometric lens table and Smith checks passed through d=20.')
    odd_rows = [r for r in ROWS if r[0] % 2 or r[1] % 2]
    bundle_matrix = fmpz_mat([[(0, 1, 0, -1)[(s*u+t*v) % 4]
                              for s, t in SLOPES] for u, v in odd_rows])
    smith = bundle_matrix.snf()
    bundle_diagonal = tuple(abs(int(smith[i, i])) for i in range(6))
    assert bundle_diagonal == (1, 1, 2, 2, 4, 4)
    print('Constant six-slope bundle matrix Smith diagonal:', bundle_diagonal)
    if '--symbolic' in sys.argv:
        symbolic_audit(True)
        symbolic_audit(False)


if __name__ == '__main__':
    main()

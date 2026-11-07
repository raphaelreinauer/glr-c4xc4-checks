#!/usr/bin/env python3
"""Exact regression checks for the two top spin-index diagonals.

The proof of the geometric Gysin identification is in the manuscript.
This checks its integral projective-bundle arithmetic and row spanning;
it does not replace the geometric argument.
"""
from fractions import Fraction


def rank_f2(columns):
    pivots = {}
    for column in columns:
        while column:
            pivot = column.bit_length() - 1
            if pivot in pivots:
                column ^= pivots[pivot]
            else:
                pivots[pivot] = column
                break
    return len(pivots)


def check(N):
    m = 2 * N
    rows = []
    for r in range(N):
        a = 2 * r + 1
        # Independent reduction using y^(b-1)(x+y)^2=0.
        I = [0] * (m + 2)
        I[a] = 1
        for i in range(a - 1, -1, -1):
            I[i] = -2 * I[i + 1] - I[i + 2]
        assert I[:m + 1] == [
            (-1) ** (a - i) * (a - i + 1) if i <= a else 0
            for i in range(m + 1)
        ]
        J = [
            Fraction(i * I[i + 1] + (m - 1 - i) * I[i], 2)
            for i in range(m)
        ]
        assert all(value.denominator == 1 for value in J)
        # The product bases CP^(2j+1) x CP^(m-2j-1).
        product_next = [0] * m
        product_top = [0] * (m + 1)
        for j in range(r + 1):
            k = 2 * j + 1
            product_top[k] += 1
            for i in range(m):
                product_next[i] += Fraction(
                    i * int(i + 1 == k)
                    + (m - 1 - i) * int(i == k), 2
                )
        expected = [0] * m
        for j in range(r + 1):
            expected[2 * j] = (r - j + 1) % 2
            expected[2 * j + 1] = (r - j) % 2
        actual = [int(J[i] - product_next[i]) % 2 for i in range(m)]
        assert actual == expected
        # Top coefficients give the forced h0 corrections, not zero.
        top_half = [
            Fraction(I[i] - product_top[i], 2) for i in range(m + 1)
        ]
        assert all(value.denominator == 1 for value in top_half)
        assert [int(value) % 2 for value in top_half[:m]] == expected
        assert top_half[m] == 0
        vector = sum(bit << i for i, bit in enumerate(actual))
        rows.append(vector)
    # Y_0 reflected in the two reference factors supplies the last endpoint.
    assert rows[0] == 1
    rows.append(1 << (m - 1))
    assert rank_f2(rows) == N + 1
    # Verify the exact lower-triangular real-bow description.
    basis = [1] + [
        (1 << (2 * j - 1)) | (1 << (2 * j)) for j in range(1, N)
    ] + [1 << (m - 1)]
    for r, vector in enumerate(rows[:-1]):
        reconstructed = ((r + 1) % 2) * basis[0]
        for j in range(1, r + 1):
            if (r - j + 1) % 2:
                reconstructed ^= basis[j]
        assert reconstructed == vector


if __name__ == "__main__":
    for N in range(2, 65):
        check(N)
    print("PASS: integral spin-index diagonals, forced h0 corrections,")
    print("and full first-row rank N+1 for every N=2,...,64.")

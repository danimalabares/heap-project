#!/usr/bin/env python3
"""Exact check of the Kauffman bracket and Jones
polynomial computations in knot-theory.tex.

Conventions (Lickorish, An Introduction to Knot
Theory, Definition 3.1 and Definition 3.6):

  <O> = 1,
  <D u O> = (-A^2 - A^-2) <D>,
  <crossing> = A <A-smoothing> + A^-1 <B-smoothing>,
  V(L) = (-A)^(-3 w(D)) <D>   with   A = t^(-1/4).

A diagram is a list of crossings [a, b, c, d]: the
four arc labels around the crossing, counter-
clockwise, starting from the incoming under-arc.
Then a -> c is the under-strand, and the
A-smoothing joins a with b and c with d, the
B-smoothing joins a with d and b with c.
The crossing is positive exactly when the over-
strand runs from d to b.

Laurent polynomials in A are dicts
{exponent: integer coefficient}; all arithmetic is
exact integer arithmetic.
"""

from itertools import product


def add(p, q):
    r = dict(p)
    for e, c in q.items():
        r[e] = r.get(e, 0) + c
        if r[e] == 0:
            del r[e]
    return r


def mul(p, q):
    r = {}
    for e1, c1 in p.items():
        for e2, c2 in q.items():
            r[e1 + e2] = r.get(e1 + e2, 0) + c1 * c2
    return {e: c for e, c in r.items() if c}


def power(p, n):
    r = {0: 1}
    for _ in range(n):
        r = mul(r, p)
    return r


D_LOOP = {2: -1, -2: -1}  # -A^2 - A^-2


def loops(pairs):
    """Number of closed curves made by the arcs."""
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for x, y in pairs:
        parent[find(x)] = find(y)
    return len({find(x) for x in list(parent)})


def bracket(pd):
    """State sum over all 2^n smoothings."""
    total = {}
    for state in product("AB", repeat=len(pd)):
        pairs = []
        exponent = 0
        for (a, b, c, d), s in zip(pd, state):
            if s == "A":
                pairs += [(a, b), (c, d)]
                exponent += 1
            else:
                pairs += [(a, d), (b, c)]
                exponent -= 1
        term = mul({exponent: 1},
                   power(D_LOOP, loops(pairs) - 1))
        total = add(total, term)
    return total


def writhe(pd, over_positive):
    """Sum of crossing signs. over_positive(a,b,c,d)
    says whether the over-strand runs from d to b."""
    return sum(1 if over_positive(*x) else -1
               for x in pd)


def normalised(pd, w):
    """(-A)^(-3w) <D> as a Laurent polynomial in A."""
    sign = -1 if (3 * w) % 2 else 1
    return mul({-3 * w: sign}, bracket(pd))


def to_t(p):
    """Substitute A = t^(-1/4). The keys of the
    result are four times the exponents of t."""
    return {-e: c for e, c in p.items()}


def show_t(p):
    q = to_t(p)
    parts = []
    for e in sorted(q):
        num = e
        if num % 4 == 0:
            ex = str(num // 4)
        elif num % 2 == 0:
            ex = f"{num // 2}/2"
        else:
            ex = f"{num}/4"
        parts.append(f"{q[e]:+d}*t^({ex})")
    return " ".join(parts)


def braid_closure(n):
    """Closure of the 2-strand braid with n positive
    crossings: the torus link T(2,n). Arcs: below
    crossing i the left arc is ('l', i) and the right
    arc is ('r', i); indices are taken modulo n.
    Both strands point upwards; the over-strand goes
    from bottom-left to top-right."""
    pd = []
    for i in range(n):
        j = (i + 1) % n
        pd.append([("r", i), ("r", j), ("l", j), ("l", i)])
    return pd


def formula_bracket(n):
    """<D_n> = A^n d + sum_{k>=1} C(n,k) A^(n-2k) d^(k-1)."""
    from math import comb
    total = mul({n: 1}, D_LOOP)
    for k in range(1, n + 1):
        total = add(total, mul({n - 2 * k: comb(n, k)},
                               power(D_LOOP, k - 1)))
    return total


def main():
    # 1. Hopf link and trefoil as braid closures.
    assert bracket(braid_closure(2)) == {4: -1, -4: -1}
    tref = bracket(braid_closure(3))
    assert tref == {-7: 1, -3: -1, 5: -1}, tref
    print("<trefoil, 3 positive crossings> =", tref)

    v = normalised(braid_closure(3), 3)
    assert to_t(v) == {4: 1, 12: 1, 16: -1}, v
    print("V(right-handed trefoil) =", show_t(v))

    # 2. Bracket of the closure of n crossings against
    #    the closed state-sum formula and the recursion.
    for n in range(1, 11):
        b = bracket(braid_closure(n))
        assert b == formula_bracket(n), n
        if n > 1:
            sign = -1 if (n - 1) % 2 else 1
            rec = add(mul({1: 1}, bracket(braid_closure(n - 1))),
                      {-1 - 3 * (n - 1): sign})
            assert b == rec, n
        # (d) * <D_n> = (-A^-3)^n + A^n (d^2 - 1)
        lhs = mul(D_LOOP, b)
        sign = -1 if n % 2 else 1
        rhs = add({-3 * n: sign},
                  mul({n: 1}, add(power(D_LOOP, 2), {0: -1})))
        assert lhs == rhs, n
    print("bracket of T(2,n): formula and recursion agree, n = 1..10")

    # 3. Jones polynomial of T(2,n), n odd, against
    #    t^((n-1)/2) (1 - t^3 - t^(n+1) + t^(n+2)) / (1 - t^2).
    for n in range(3, 12, 2):
        v = to_t(normalised(braid_closure(n), n))
        one_minus_t2 = {0: 1, 8: -1}
        lhs = mul(v, one_minus_t2)
        s = 4 * (n - 1) // 2
        rhs = {s: 1, s + 12: -1, s + 4 * (n + 1): -1,
               s + 4 * (n + 2): 1}
        assert lhs == rhs, n
    print("V(T(2,n)) matches the torus knot formula, n = 3..11 odd")

    # 4. Independent diagrams from the knot tables
    #    (planar diagram codes with arcs numbered
    #    1..2n along the knot).
    def over_positive_numbered(n):
        def f(a, b, c, d):
            return (d % (2 * n)) + 1 == b
        return f

    tref_pd = [[1, 4, 2, 5], [3, 6, 4, 1], [5, 2, 6, 3]]
    w = writhe(tref_pd, over_positive_numbered(3))
    v = to_t(normalised(tref_pd, w))
    print("table trefoil: writhe", w, " V =",
          show_t(normalised(tref_pd, w)))
    assert w == -3 and v == {-4: 1, -12: 1, -16: -1}

    fig8 = [[4, 2, 5, 1], [8, 6, 1, 5],
            [6, 3, 7, 4], [2, 7, 3, 8]]
    w = writhe(fig8, over_positive_numbered(4))
    v = to_t(normalised(fig8, w))
    print("figure eight: writhe", w, " V =",
          show_t(normalised(fig8, w)))
    assert v == {-8: 1, -4: -1, 0: 1, 4: -1, 8: 1}
    assert v == {-e: c for e, c in v.items()}

    # 5. Value at t = 1 (A = -1 gives t = 1 with
    #    t^(1/2) = A^-2 = 1): V = (-2)^(components-1).
    for n in range(1, 9):
        p = normalised(braid_closure(n), n)
        value = sum(c * (-1) ** (e % 2) for e, c in p.items())
        comps = 2 if n % 2 == 0 else 1
        assert value == (-2) ** (comps - 1), (n, value)
    print("V(1) = (-2)^(components - 1) for T(2,n), n = 1..8")
    print("all checks passed")


if __name__ == "__main__":
    main()

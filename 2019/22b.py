#!/usr/bin/env python3

from __future__ import print_function

import re
import sys

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

N = 119315717514047
REPS = 101741582076661
POS = 2020

#N, REPS, POS  = 10, 2, 9

# xgcd and modinv were copied from wikipedia or stack overflow or somewhere
def xgcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def modinv(a, b):
    """return x such that (x * a) % b == 1"""
    # return pow(a, -1, b)  # In python3.8 you can just use pow!
    g, x, _ = xgcd(a, b)
    assert g == 1
    return x % b


def compose(f1, f2):
    """Compose two shuffle functions.

    f1(f2(x)) = a1*(a2*x + b2) + b1
              = a1*a2*x + a1*b2 + b1
    """
    (a1, b1), (a2, b2) = f1, f2
    return a1*a2 % N, (a1*b2 + b1) % N


def exp(f, n):
    """Do standard exponentiation by squaring"""
    if n == 0:
        return (1, 0)
    elif n % 2 == 0:
        return exp(compose(f, f), n // 2)
    else:
        return compose(f, exp(compose(f, f), n // 2))


def main(args):
    data = [s.strip() for s in sys.stdin]
    reps = int(args[1]) if args[1:] else REPS
    pos = int(args[2]) if args[2:] else POS

    # The transformation is equivalent to a function
    # f(x) = (ax + b) % N, where f(x) is the position of
    # card x after shuffling.
    f = 1, 0
    for s in data:
        if s == "deal into new stack":
            op = -1, -1
        elif s.startswith("deal with"):
            op = extract(s)[0], 0
        else:
            op = 1, -extract(s)[0]

        f = compose(op, f)

    af, bf = exp(f, reps)
    # pos = ipos * af + bf  (mod N), so compute
    # ipos = (pos - bf) * af^-1  (mod N)
    afn1 = modinv(af, N)
    ipos = ((pos - bf) * afn1) % N
    print(ipos)

if __name__ == '__main__':
    main(sys.argv)

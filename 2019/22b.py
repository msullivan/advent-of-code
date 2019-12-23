#!/usr/bin/env python3

from __future__ import print_function

from collections import defaultdict, deque
import sys
import time
import math
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

N = 119315717514047
REPS = 101741582076661
POS = 2020

#N, REPS, POS  = 10, 2, 9

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
    g, x, _ = xgcd(a, b)
    # print(a, b, g, x%b)

    if g == 1:
        return x % b
    assert False


def compose(x1, x2):
    return x1[0]*x2[0] % N, (x1[0]*x2[1] + x1[1]) % N


def exp(f, n):
#    print(n)
    if n == 0:
        return (1, 0)
    elif n % 2 == 0:
        return exp(compose(f, f), n // 2)
    else:
        return compose(f, exp(compose(f, f), n // 2))



def main(args):
    data = [s.strip() for s in sys.stdin]
    reps = int(args[1]) if args[1:] else REPS


#    pos = 2020
    pos = POS

    ndata = []
    for s in data:
        if s == "deal into new stack":
            ndata.append("deal with %s" % (N-1))
            ndata.append("cut 1")
        else:
            ndata.append(s)

    data = ndata

    a, b = 1, 0
    for s in data:
        if s.startswith("deal with"):
            (increment,) = extract(s)
            #inv = modinv(increment, N)
            mul = increment
            a = (a * mul) % N
            b = (b * mul) % N

        else:
            (cut,) = extract(s)
            b = (b - cut) % N
        print(s, (a,b))

    af, bf = exp((a, b), reps)
    print(af, bf)
    #pos = (pos * af + bf) % N
    afn1 = modinv(af, N)
    pos = ((pos - bf) * afn1) % N
    print(pos)

if __name__ == '__main__':
    main(sys.argv)

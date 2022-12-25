#!/usr/bin/env python3

import sys

DIGITS = "=-012"

def num(s):
    return DIGITS.index(s) - 2

def to_dec(s):
    v = 0
    for i, c in enumerate(reversed(s)):
        v += num(c) * 5**i
    return v

def to_snafu(n):
    # adapated from https://rosettacode.org/wiki/Balanced_ternary#Python
    if n == 0: return ''
    if (n % 5) == 0: return to_snafu(n // 5) + '0'
    if (n % 5) == 1: return to_snafu(n // 5) + '1'
    if (n % 5) == 2: return to_snafu(n // 5) + '2'
    if (n % 5) == 3: return to_snafu((n+2) // 5) + '='
    if (n % 5) == 4: return to_snafu((n+1) // 5) + '-'

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    x = 0
    for s in data:
        x += to_dec(s)

    print(x)
    print(to_snafu(x))

if __name__ == '__main__':
    main(sys.argv)

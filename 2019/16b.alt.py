#!/usr/bin/env python3

# This does an honest computation of the Flawed Frequency Transmission
# that doesn't rely on the offset being large. It computes all of the digits
# of the FFT.
# On my laptop it ran in two minutes using pypy.

from __future__ import print_function

import sys
import time

def go(n, partials):
    """Compute one element value from the FFT.

    It is kind of uglified for performance."""
    step = 2 * n
    end = len(partials) - 1

    mode = 1
    lo = -1 + n
    hi = lo + n

    res = 0

    # We loop until hi is too big and then do a separate check for lo
    # so that we can avoid having to bound hi inside the loop each
    # iteration. This made things like 15% faster.
    while hi < end:
        res += mode * (partials[hi] - partials[lo])
        mode = -mode
        lo += step
        hi = lo + n

    if lo < end:
        hi = min(lo + n, end)
        res += mode * (partials[hi] - partials[lo])

    return abs(res) % 10


def fft(l):
    """Fucked Fourier Transform"""
    partials = [0]
    sum = 0
    for v in l:
        sum += v
        partials.append(sum)

    x = []
    for i, y in enumerate(l):
        x.append(go(i+1, partials))
    return x

def display(data, offset):
    return ''.join(str(x) for x in data[offset:offset+8])


def main(args):
    orig_data = [int(x) for x in [s.strip() for s in sys.stdin][0]]
    data = orig_data * 10000


    offset = int(''.join(str(x) for x in data[:7]))

    for i in range(10):
        print(i, display(data, 0), display(data, offset))
        data = fft(data)

    print(display(data, offset))


if __name__ == '__main__':
    main(sys.argv)

#!/usr/bin/env python3

"""
This does an honest computation of the Flawed Frequency Transmission
that doesn't rely on the offset being large. It computes all of the
digits of the FFT.  On my laptop it ran in two minutes using pypy.

The trick is that we compute a partial sums array,
where partials[0] = 0 and partials[i+1] = l[0]+...+l[i-1].

We can then quickly compute the sum l[i]+...+l[j]
as partials[j+1] - partials[i].

Then, for each output element `i`, for each run of `i` 1s or -1s in the
pattern, we can compute the sum of the corresponding input elements in
constant time, multiply it by 1 or -1, and add it to our running sum.

This means that computing output element `i` takes O(N/i) time.
Since I am told that 1/1 + 1/2 + 1/3 + ... + 1/N is O(lg N)
(https://en.wikipedia.org/wiki/Harmonic_number),
this FFT runs in O(N lg N) time.
"""

from __future__ import print_function

import sys
import time

def go(i, partials):
    """Compute one element value from the FFT.

    It is kind of uglified for performance."""
    step = 2 * i
    end = len(partials) - 1

    mode = 1
    lo = -1 + i
    hi = lo + i

    res = 0

    # We loop until hi is too big and then do a separate check for lo
    # so that we can avoid having to bound hi inside the loop each
    # iteration. This made things like 15% faster.
    while hi < end:
        res += mode * (partials[hi] - partials[lo])
        mode = -mode
        lo += step
        hi = lo + i

    if lo < end:
        hi = min(lo + i, end)
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

    for i in range(100):
        print(i, display(data, 0), display(data, offset))
        data = fft(data)

    print(i, display(data, 0), display(data, offset))
    print(display(data, offset))


if __name__ == '__main__':
    main(sys.argv)

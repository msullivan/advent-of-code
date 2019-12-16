#!/usr/bin/env python3

import sys
import time
import math


def go(l, n, partials):
    return (partials[-1] - partials[n]) % 10


def fft(l):
    """Fucked Fourier Transform"""
    partials = [0]
    sum = 0
    for v in l:
        sum += v
        partials.append(sum)

    x = []
    for i, y in enumerate(l):
        x.append(go(l, i, partials))
    return x


def main(args):
    orig_data = [int(x) for x in [s.strip() for s in sys.stdin][0]]
    data = orig_data * 10000

    offset = int(''.join(str(x) for x in data[:7]))
    assert offset*2 > len(data)
    data = data[offset:]


    for i in range(100):
        data = fft(data)

    print(''.join(str(x) for x in data[:8]))


if __name__ == '__main__':
    main(sys.argv)

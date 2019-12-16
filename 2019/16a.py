#!/usr/bin/env python3

import sys
import time
import math

def go(l, n):
    pattern = []
    for x in [0, 1, 0, -1]:
        pattern += [x] * n

    val = 0
    for i, v in enumerate(l):
        val += v * pattern[(i+1) % len(pattern)]

    return int(str(val)[-1])

def fft(l):
    """Fucked Fourier Transform"""
    x = []
    for i, y in enumerate(l):
        x.append(go(l, i+1))
    return x


def main(args):
    data = [int(x) for x in [s.strip() for s in sys.stdin][0]]

    for i in range(100):
        data = fft(data)

    print(''.join(str(x) for x in data))


if __name__ == '__main__':
    main(sys.argv)

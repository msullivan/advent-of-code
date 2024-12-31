#!/usr/bin/env python3

import sys
import numpy as np
import time

def compute(n, i):
    mask = 16777216 - 1
    for _ in range(i):
        n = (n ^ (n << 6)) & mask
        n = (n ^ (n >> 5)) & mask
        n = (n ^ (n << 11)) & mask
    return n


def main(args):
    t0 = time.monotonic()
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [int(s.rstrip('\n')) for s in file]

    # val = sum(compute(n, 2000) for n in data)

    ns = np.array(data, dtype=np.int64)
    val = sum(compute(ns, 2000))

    t1 = time.monotonic()
    print(f'{t1-t0:0.3f}s')
    print(val)



if __name__ == '__main__':
    main(sys.argv)

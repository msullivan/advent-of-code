#!/usr/bin/env python3

import sys

# From https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6
from functools import reduce
def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod

def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

def main(args):
    # data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    data = [s.strip() for s in sys.stdin]
    early = int(data[0])
    stamps = [int(x) if x != "x" else None for x in data[1].split(",")]

    i = early
    while True:
        matches = [x for x in stamps if x and i % x == 0]
        print("a", matches)
        if matches:
            break
        i += 1

    print(matches[0])
    print((i - early) * matches[0])

    crap = [(x,i) for i,x in enumerate(stamps) if x]
    # print(bs)
    # print(crap)
    # print(len(crap))
    a = max(crap)
    # print(a)
    step, offs = a

    bcrap = [(x,(x-i%x)) for i,x in enumerate(stamps) if x]
    ns, bs = zip(*bcrap)
    print(bs, ns)
    crt = chinese_remainder(ns, bs)
    print(crt)
    # print(crt/2)

    # cur = step
    # while True:
    #     match = True
    #     for x, i in crap:
    #         off = i - offs
    #         if (cur + off) % x != 0:
    #             match = False
    #             break
    #     if match:
    #         break
    #     cur += step
    # print(cur - offs)



if __name__ == '__main__':
    sys.exit(main(sys.argv))

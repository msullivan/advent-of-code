#!/usr/bin/env python3

import sys

from functools import reduce
import operator


def int2(s):
    return int(s, 2)


def read(s, i, n):
    return int2(s[i:i+n]), i + n


def parse(s, i):
    v, i = read(s, i, 3)
    tid, i = read(s, i, 3)

    if tid == 4:
        lit = 0
        while True:
            lit <<= 4
            frag, i = read(s, i, 5)
            lit |= frag & 0xf
            if not (frag & 0x10):
                break
        return (v, tid, lit), i

    # operator
    ltid, i = read(s, i, 1)
    args = []
    if ltid == 0:
        nbits, i = read(s, i, 15)
        end = i + nbits
        while i < end:
            el, i = parse(s, i)
            args.append(el)
        assert i == end, (args, i, end)
    else:
        npackets, i = read(s, i, 11)
        for _ in range(npackets):
            el, i = parse(s, i)
            args.append(el)

    return (v, tid, args), i


def calc_sum(packet):
    vsum = packet[0]
    if packet[1] != 4:
        vsum += sum(calc_sum(sub) for sub in packet[2])
    return vsum


def eval(packet):
    ver, tid, args = packet

    if tid == 0:
        return sum(eval(arg) for arg in args)
    elif tid == 1:
        return reduce(operator.mul, (eval(arg) for arg in args))
    elif tid == 2:
        return min(eval(arg) for arg in args)
    elif tid == 3:
        return max(eval(arg) for arg in args)
    elif tid == 4:
        return args
    elif tid == 5:
        return int(eval(args[0]) > eval(args[1]))
    elif tid == 6:
        return int(eval(args[0]) < eval(args[1]))
    elif tid == 7:
        return int(eval(args[0]) == eval(args[1]))


def main(args):
    data = [s.strip() for s in sys.stdin][0]
    bits = bin(int(data, 16))[2:]
    while len(bits) % 4 != 0:
        bits = '0' + bits

    val, _ = parse(bits, 0)
    print(calc_sum(val))
    print(eval(val))

if __name__ == '__main__':
    main(sys.argv)

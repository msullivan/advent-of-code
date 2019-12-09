#!/usr/bin/env python3

import sys
import re
import time
import itertools
from collections import defaultdict


def run(p, ip, input, output):
    if ip == -1:
        return -1

    relative_base = 0

    while True:
        instr = p[ip]

        def read(i):
            mode = (instr // (10**(1+i))) % 10
            if mode == 0:
                return p[p[ip+i]]
            elif mode == 1:
                return p[ip+i]
            else:
                return p[p[ip+i] + relative_base]

        def write(i, v):
            mode = (instr // (10**(1+i))) % 10
            if mode == 0:
                p[p[ip+i]] = v
            else:
                assert mode == 2
                p[p[ip+i] + relative_base] = v


        if instr % 100 == 1:
            write(3, read(1) + read(2))
            ip += 4
        elif instr % 100 == 2:
            write(3, read(1) * read(2))
            ip += 4
        elif instr % 100 == 3:
            if not input:
                return ip
            write(1, input.pop(0))
            ip += 2
        elif instr % 100 == 4:
            output.append(read(1))
            ip += 2
        elif instr % 100 == 5:
            if read(1) != 0:
                ip = read(2)
            else:
                ip += 3
        elif instr % 100 == 6:
            if read(1) == 0:
                ip = read(2)
            else:
                ip += 3
        elif instr % 100 == 7:
            if read(1) < read(2):
                write(3, 1)
            else:
                write(3, 0)
            ip += 4
        elif instr % 100 == 8:
            if read(1) == read(2):
                write(3, 1)
            else:
                write(3, 0)
            ip += 4
        elif instr % 100 == 9:
            relative_base += read(1)
            ip += 2
        elif instr % 100 == 99:
            break

    return -1

def main(args):
    data = [s.strip() for s in sys.stdin]
    lp = [int(x) for x in data[0].split(",")]
    p = defaultdict(int, [(i, x) for i, x in enumerate(lp)])

    outs = []
    run(p.copy(), 0, [1], outs)
    print(outs)

    outs = []
    run(p.copy(), 0, [2], outs)
    print(outs)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

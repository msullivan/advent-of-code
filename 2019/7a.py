#!/usr/bin/env python3

import sys
import re
import time
import itertools


def run(p, input):
    ip = 0
    output = []
    while True:
        instr = p[ip]

        def read(i):
            mode = (instr // (10**(1+i))) % 10
            return p[p[ip+i]] if mode == 0 else p[ip+i]

        if instr % 100 == 1:
            p[p[ip+3]] = read(1) + read(2)
            ip += 4
        elif instr % 100 == 2:
            p[p[ip+3]] = read(1) * read(2)
            ip += 4
        elif instr % 100 == 3:
            p[p[ip+1]] = input.pop(0)
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
                p[p[ip+3]] = 1
            else:
                p[p[ip+3]] = 0
            ip += 4
        elif instr % 100 == 8:
            if read(1) == read(2):
                p[p[ip+3]] = 1
            else:
                p[p[ip+3]] = 0
            ip += 4
        elif instr % 100 == 99:
            break

    # print("OUT", output)
    return output

def main(args):
    data = [s.strip() for s in sys.stdin]
    p = [int(x) for x in data[0].split(",")]
    op = list(p)
    outs = []
    for x in itertools.permutations([0,1,2,3,4]):
        input = 0
        for i in x:
            out = run(list(p), [i, input])
            input = out[0]
        outs += [out]
    print(outs)
    print(max(outs))

if __name__ == '__main__':
    sys.exit(main(sys.argv))

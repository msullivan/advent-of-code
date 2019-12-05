#!/usr/bin/env python3

import sys

def run(p):
    ip = 0
    while True:
        instr = p[ip]
        if instr == 1:
            p[p[ip+3]] = p[p[ip+1]] + p[p[ip+2]]
            ip += 4
        elif instr == 2:
            p[p[ip+3]] = p[p[ip+1]] * p[p[ip+2]]
            ip += 4
        elif instr == 99:
            break


def main(args):
    data = [s.strip() for s in sys.stdin]
    p = [int(x) for x in data[0].split(",")]
    op = list(p)

    for n in range(100):
        for v in range(100):
            p = list(op)
            p[1] = n
            p[2] = v
            run(p)
            if p[0] == 19690720:
                print(100*n + v)
                return

if __name__ == '__main__':
    sys.exit(main(sys.argv))

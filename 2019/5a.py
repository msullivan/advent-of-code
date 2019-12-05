#!/usr/bin/env python3

import sys

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
        elif instr % 100 == 99:
            break

    print(output)


def main(args):
    data = [s.strip() for s in sys.stdin]
    p = [int(x) for x in data[0].split(",")]
    op = list(p)
    run(p, [1])

if __name__ == '__main__':
    sys.exit(main(sys.argv))

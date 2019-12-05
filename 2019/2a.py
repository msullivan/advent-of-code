#!/usr/bin/env python3

import sys

def main(args):
    data = [s.strip() for s in sys.stdin]
    program = [int(x) for x in data[0].split(",")]

    program[1] = 12
    program[2] = 2

    ip = 0
    while True:
        instr = program[ip]
        if instr == 1:
            program[program[ip+3]] = program[program[ip+1]] + program[program[ip+2]]
        elif instr == 2:
            program[program[ip+3]] = program[program[ip+1]] * program[program[ip+2]]
        elif instr == 99:
            break

        ip += 4

    print(program[0])

if __name__ == '__main__':
    sys.exit(main(sys.argv))

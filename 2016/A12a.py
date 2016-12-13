#!/usr/bin/env python3

import sys, json
from collections import defaultdict

def val(regs, x):
    if x in regs:
        return regs[x]
    else:
        return int(x)


def main(args):
    program = [s.strip().split(" ") for s in sys.stdin]
    regs = {c: 0 for c in "abcd"}

    pc = 0

    while pc < len(program):
        cmd = program[pc]
        if cmd[0] == "cpy":
            regs[cmd[2]] = val(regs, cmd[1])
        elif cmd[0] == "inc":
            regs[cmd[1]] += 1
        elif cmd[0] == "dec":
            regs[cmd[1]] -= 1
        elif cmd[0] == "jnz":
            if val(regs, cmd[1]) != 0:
                pc += int(cmd[2]) - 1
        pc += 1

    print(regs["a"])


if __name__ == '__main__':
    sys.exit(main(sys.argv))

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
    regs['a'] = 7

    pc = 0

    while pc < len(program):
        try:
            cmd = program[pc]
#            print(pc, cmd)
            if cmd[0] == "cpy":
                regs[cmd[2]] = val(regs, cmd[1])
            elif cmd[0] == "inc":
                regs[cmd[1]] += 1
            elif cmd[0] == "dec":
                regs[cmd[1]] -= 1
            elif cmd[0] == "jnz":
                if val(regs, cmd[1]) != 0:
                    pc += val(regs, cmd[2]) - 1
            elif cmd[0] == "tgl":
                loc = pc + val(regs, cmd[1])
                if len(program[loc]) == 2:
                    if program[loc][0] == "inc":
                        program[loc][0] = "dec"
                    else:
                        program[loc][0] = "inc"
                elif len(program[loc]) == 3:
                    if program[loc][0] == "jnz":
                        program[loc][0] = "cpy"
                    else:
                        program[loc][0] = "jnz"
        except Exception as e:
            print(e)
            pass
        pc += 1

    print(regs["a"])


if __name__ == '__main__':
    sys.exit(main(sys.argv))

#!/usr/bin/env python3

import sys, json


def step(cmd, state):
    cmd = cmd.replace(",", "")
    parts = cmd.split(" ")
 #   print(parts)
    op = parts[0]
    reg = parts[1]

    if op == "hlf":
        state[reg] = int(state[reg] / 2)
    elif op == "tpl":
        state[reg] *= 3
    elif op == "inc":
        state[reg] += 1
    elif op == "jmp":
        return int(parts[1])
    elif op == "jie":
        if state[reg] % 2 == 0:
            return int(parts[2])
    elif op == "jio":
        # asdf. jump if *one*
        if state[reg] == 1:
            return int(parts[2])

    return 1


def main(args):
    prog = [s.strip() for s in sys.stdin]
    state = {"a": 1, "b": 0}
    ip = 0

    while ip >= 0 and ip < len(prog):
        ip += step(prog[ip], state)
#        print(ip, state)

    print(state)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

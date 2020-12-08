#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]


def main(args):
    # data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    data = [s.strip() for s in sys.stdin]

    prog = data
    acc = 0
    ip = 0

    seen = set()
    while True:
        print(ip)
        if ip in seen:
            break

        seen.add(ip)

        instr = prog[ip].split(" ")
        if instr[0] == "acc":
            acc += int(instr[1])
        elif instr[0] == "jmp":
            ip += int(instr[1]) - 1
        elif instr[0] == "nop":
            pass

        ip += 1


    print(acc)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

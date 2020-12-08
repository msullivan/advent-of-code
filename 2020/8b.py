#!/usr/bin/env python3

import sys

def run(prog):
    loop = False
    seen = set()
    acc = 0
    ip = 0

    while ip < len(prog):
        if ip in seen:
            loop = True
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

    return loop, acc


def main(args):
    data = [s.strip() for s in sys.stdin]

    prog = data

    print(run(prog)[1])

    for i in range(len(data)):
        prog2 = list(prog)
        if "nop" in prog2[i]:
            prog2[i] = prog2[i].replace("nop", "jmp")
        else:
            prog2[i] = prog2[i].replace("jmp", "nop")
        loop, acc = run(prog2)
        if not loop:
            break
    print(acc)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

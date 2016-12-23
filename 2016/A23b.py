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
    regs['a'] = 12

    pc = 0

    dummy = ["", 0, 0]
    while pc < len(program):
        try:
            cmd = program[pc]
            cmd1, cmd2 = dummy, dummy
            if pc+1 < len(program): cmd1 = program[pc+1]
            if pc+2 < len(program): cmd2 = program[pc+2]
#            print(pc, cmd)
            part = program[pc:pc+6]
            if [x[0] for x in part] == ["cpy", "inc", "dec", "jnz", "dec", "jnz"] and pc == 4:
                regs[cmd1[1]] += regs[cmd[1]]*regs[program[pc+4][1]]
                print(program[pc+4][1], cmd[2])
                regs[program[pc+4][1]] = 0
                regs[cmd[2]] = 0
                print("fuck", pc)
                print(part)
                pc += 6
                print(program[pc])
                continue

            if cmd[0] == "inc" and cmd1[0] == "dec" and cmd2[0] == "jnz":
                if cmd1[1] == cmd2[1] and cmd2[2] == "-2":
                    regs[cmd[1]] += regs[cmd1[1]]
                    regs[cmd1[1]] = 0
                    pc += 3
#                    print("taken!")
                    continue
            if cmd[0] == "dec" and cmd1[0] == "inc" and cmd2[0] == "jnz":
                if cmd[1] == cmd2[1] and cmd2[2] == "-2":
                    regs[cmd1[1]] += regs[cmd[1]]
                    regs[cmd[1]] = 0
                    pc += 3
                    print("taken2!")
                    continue


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
#            print(e)
            pass
        pc += 1

    print(regs["a"])
    print(regs)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

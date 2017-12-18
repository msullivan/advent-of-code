#!/usr/bin/env python3

import sys

def read(regs, s):
    if s.isalpha():
        if s not in regs:
            regs[s] = 0
        return regs[s]
    else:
        return int(s)


def main(args):
    data = [s.strip() for s in sys.stdin]

    regs = {}

    i = 0
    sound = None
    while True:
        cmd = data[i].split(" ")
        if cmd[0] == "snd":
            sound = read(regs, cmd[1])
        elif cmd[0] == "set":
            regs[cmd[1]] = read(regs, cmd[2])
        elif cmd[0] == "add":
            regs[cmd[1]] = read(regs, cmd[1]) + read(regs, cmd[2])
        elif cmd[0] == "mul":
            regs[cmd[1]] = read(regs, cmd[1]) * read(regs, cmd[2])
        elif cmd[0] == "mod":
            regs[cmd[1]] = read(regs, cmd[1]) % read(regs, cmd[2])
        elif cmd[0] == "rcv":
            if read(regs, cmd[1]):
                break
        elif cmd[0] == "jgz":
            if read(regs, cmd[1]) > 0:
                i += read(regs, cmd[2])
                continue
        i += 1

    print(sound)



if __name__ == '__main__':
    sys.exit(main(sys.argv))

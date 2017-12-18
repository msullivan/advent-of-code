#!/usr/bin/env python3

import sys

def read(regs, s):
    if s.isalpha():
        if s not in regs:
            regs[s] = 0
        return regs[s]
    else:
        return int(s)


def step(data, regs, ip, inq, outq):
    cmd = data[ip].split(" ")
    if cmd[0] == "snd":
        sound = read(regs, cmd[1])
        outq += [sound]
    elif cmd[0] == "set":
        regs[cmd[1]] = read(regs, cmd[2])
    elif cmd[0] == "add":
        regs[cmd[1]] = read(regs, cmd[1]) + read(regs, cmd[2])
    elif cmd[0] == "mul":
        regs[cmd[1]] = read(regs, cmd[1]) * read(regs, cmd[2])
    elif cmd[0] == "mod":
        regs[cmd[1]] = read(regs, cmd[1]) % read(regs, cmd[2])
    elif cmd[0] == "rcv":
        if not inq: return None
        regs[cmd[1]] = inq[0]
        inq.pop(0)
    elif cmd[0] == "jgz":
        if read(regs, cmd[1]) > 0:
            ip += read(regs, cmd[2])
            return ip
    ip += 1
    return ip

def main(args):
    data = [s.strip() for s in sys.stdin]

    regsa = {'p': 0}
    regsb = {'p': 1}
    ina = []
    inb = []
    ipa = 0
    ipb = 0
    snds = 0

    while True:
        while True:
            nextip = step(data, regsa, ipa, ina, inb)
            if nextip is None: break
            ipa = nextip
        while True:
            if data[ipb].split(" ")[0] == "snd": snds+=1
            nextip = step(data, regsb, ipb, inb, ina)
            if nextip is None: break
            ipb = nextip

        if not ina and not inb: break

    print(snds)



if __name__ == '__main__':
    sys.exit(main(sys.argv))

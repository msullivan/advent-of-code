#!/usr/bin/env python3

# I wrote this after the fact to experiment with the sort of tooling
# it would have been nice to have written.

import sys
from collections import defaultdict

def read(regs, s):
    return regs[s] if s.isalpha() else int(s)

def step(data, regs, ip):
    op, Rs, Rd = data[ip]
    Vs, Vd = read(regs, Rs), read(regs, Rd)

    if op == "snd":
        outq.append(Vs)
    elif op == "set":
        regs[Rs] = Vd
    elif op == "sub":
        regs[Rs] -= Vd
    elif op == "mul":
        regs[Rs] *= Vd
    elif op == "mod":
        regs[Rs] %= Vd
    elif op == "rcv":
        if not inq: return None
        regs[Rs] = inq.pop(0)
    elif op == "jnz":
        if Vs != 0:
            return ip + Vd
    return ip + 1

def find_targets(prog):
    # Find jump targets
    targets = set()
    for ip in range(len(prog)):
        op, Rs, Rd = prog[ip]
        if op == "jnz" and not Rd.isalpha():
            targets.add(ip + int(Rd))

    # Generate labels for them
    labels = {}
    for i, target in enumerate(sorted(targets)):
        labels[target] = "L" + str(i)
    return labels

def label(prog):
    targets = find_targets(prog)

    for ip, (op, Rs, Rd) in enumerate(prog):
        if ip in targets:
            print(targets[ip]+":")
        if op == "jnz" and not Rd.isalpha():
            Rd = targets[ip + int(Rd)]
        print("\t" + " ".join([op, Rs, Rd]))

    for ip, label in targets.items():
        if ip >= len(prog):
            print(label+":")

def run(prog):
    regsa, ina, ipa = defaultdict(int, {'p': 0}), [], 0
#    regsb, inb, ipb = defaultdict(int, {'p': 1}), [], 0
    snds = 0

    while True:
        if data[ipa][0] == "mul": snds+=1
        ipa = nextip = step(data, regsa, ipa)
        if ipa < 0 or ipa >= len(data): break
        print(ipa)

    print(regsa)
    print(snds)

def main(args):
    data = [tuple(s.strip().split(" ")+[''])[:3] for s in sys.stdin]

    label(data)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

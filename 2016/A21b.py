#!/usr/bin/env python3

import sys, json
from collections import defaultdict

def based(p, char):
    i = p.index(char)
    if i >= 4: i += 1
    i += 1
    i %= len(p) # XXX:
    return p[-i:] + p[:-i]

def step(p, s):
    p = [c for c in p]
    cmd = s.split(" ")
    if s.startswith("swap position"): # FINE
        i, j = int(cmd[2]), int(cmd[5])
        p[i], p[j] = p[j], p[i]
    elif s.startswith("swap letter"): # FINE
        i, j = p.index(cmd[2]), p.index(cmd[5])
        p[i], p[j] = p[j], p[i]
    elif s.startswith("rotate left"): # SWAP WITH RIGHT
        i = int(cmd[2])
        p = p[-i:] + p[:-i]
    elif s.startswith("rotate right"): # SWAP WITH LEFT
        i = int(cmd[2])
        p = p[i:] + p[:i]
    elif s.startswith("rotate based"): # WAS THERE A SMART WAY TO DO THIS
        for i in range(len(p)):
            p2 = p[-i:] + p[:-i]
            if based(p2, cmd[6]) == p:
                p = p2
                break
    elif s.startswith("reverse positions"): # FINE
        i, j = int(cmd[2]), int(cmd[4])
        p = p[:i] + list(reversed(p[i:j+1])) + p[j+1:]
    elif s.startswith("move position"):
        j, i = int(cmd[2]), int(cmd[5]) # SWAPPED
        x = p[i]
        del p[i]
        p.insert(j, x)
    else:
        print(s, "FUCK")

    return "".join(p)

def run(program, p):
    for s in reversed(program):
        p = step(p, s)
    return p

def main(args):
    program = [s.strip() for s in sys.stdin]
#    print(run(program, "abcdefgh"))
    print(run(program, "fbgdceah"))

if __name__ == '__main__':
    sys.exit(main(sys.argv))

#!/usr/bin/env python3

import sys, json
from collections import defaultdict

def step(p, s):
    p = [c for c in p]
    cmd = s.split(" ")
    if s.startswith("swap position"):
        i, j = int(cmd[2]), int(cmd[5])
        p[i], p[j] = p[j], p[i]
    elif s.startswith("swap letter"):
        i, j = p.index(cmd[2]), p.index(cmd[5])
        p[i], p[j] = p[j], p[i]
    elif s.startswith("rotate left"):
        i = int(cmd[2])
        p = p[i:] + p[:i]
    elif s.startswith("rotate right"):
        i = int(cmd[2])
        p = p[-i:] + p[:-i]
    elif s.startswith("rotate based"):
        i = p.index(cmd[6])
        if i >= 4: i += 1
        i += 1
        i %= len(p) # XXX:
        p = p[-i:] + p[:-i]
    elif s.startswith("reverse positions"):
        i, j = int(cmd[2]), int(cmd[4])
        p = p[:i] + list(reversed(p[i:j+1])) + p[j+1:]
    elif s.startswith("move position"):
        i, j = int(cmd[2]), int(cmd[5])
        x = p[i]
        del p[i]
        p.insert(j, x)
    else:
        print(s, "FUCK")

    return "".join(p)

def run(program, p):
    for s in program:
        p = step(p, s)
    return p

def main(args):
    program = [s.strip() for s in sys.stdin]
    print(run(program, "abcdefgh"))

if __name__ == '__main__':
    sys.exit(main(sys.argv))

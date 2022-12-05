#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def main(args):
    m, cmds = [x.strip().split('\n') for x in sys.stdin.read().split('\n\n')]

    N = extract(m[-1])[-1]
    stacks = [[] for _ in range(N)]
    for line in list(reversed(m))[1:]:
        for i in range(N):
            j = 1+i*4
            if line[j:j+1] not in (" ", ""):
                stacks[i].append(line[j])

    for cmd in cmds:
        cnt, from_, to = extract(cmd)
        moved = stacks[from_-1][-cnt:]
        del stacks[from_-1][-cnt:]
        stacks[to-1].extend(moved)

    s = "".join([s[-1] for s in stacks])
    print(s)

if __name__ == '__main__':
    main(sys.argv)

#!/usr/bin/env python3

import sys

def seq_list(l):
    a = list(range(l))
    return a + list(reversed(a))[1:-1]

def position(seqs, i, k):
    ass = seqs[i]
    return ass[k % len(ass)]

def go(depths, seqs, wait):
    for i in range(max(depths.keys())+1):
        if i in depths and position(seqs, i, wait+i) == 0:
            return False

    return True

def main(args):
    data = [s.strip() for s in sys.stdin]

    depths = {}
    for line in data:
        k, v = map(int, line.split(": "))
        depths[k] = v

    seqs = {k: seq_list(depths[k]) for k in depths.keys()}

    wait = 1
    while not go(depths, seqs, wait):
        wait += 1
    print(wait)




if __name__ == '__main__':
    sys.exit(main(sys.argv))

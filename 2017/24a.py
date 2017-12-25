#!/usr/bin/env python3

import sys
from collections import defaultdict

def other(pair, x): return pair[0] if x == pair[1] else pair[1]

def search(m, avail, cur):
    top = 0
    for choice in m[cur]:
        if choice not in avail: continue
        avail.remove(choice)
        val = search(m, avail, other(choice, cur)) + choice[0] + choice[1]
        top = max(top, val)
        avail.add(choice)
    return top

def main(args):
    data = [tuple(map(int, s.strip().split("/"))) for s in sys.stdin]
    print(len(data), len(set(data)))

    avail = set(data)
    m = defaultdict(list)
    for a in avail:
        m[a[0]] += [a]
        m[a[1]] += [a]

    print(search(m, avail, 0))



if __name__ == '__main__':
    sys.exit(main(sys.argv))

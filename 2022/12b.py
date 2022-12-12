#!/usr/bin/env python3

import sys
from collections import deque

def iord(c):
    return ord(c.lower()) - ord('a')

def vadd(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),

def main(args):
    data = [s.rstrip('\n') for s in sys.stdin]

    m = {}
    for r in range(len(data)):
        for c in range(len(data[0])):
            if data[r][c] == 'S':
                start = (r, c)
            if data[r][c] == 'E':
                end = (r, c)
            x = data[r][c]
            m[r,c] = 0 if x == 'S' else 25 if x == 'E' else iord(x)

    wl = deque([(end, 0)])
    seen = set()
    while wl:
        node, dist = wl.popleft()
        if node in seen:
            continue
        seen.add(node)
        if m[node] == 0:
            break
        for dir in VDIRS:
            nbr = vadd(dir, node)
            if nbr in m and m[node] <= m[nbr]+1:
                wl.append((nbr, dist+1))

    print(dist)

if __name__ == '__main__':
    main(sys.argv)

#!/usr/bin/env python3

import sys
from collections import defaultdict, deque

def vadd(v1, v2):
    return tuple([x + y for x, y in zip(v1, v2)])

def vsub(v1, v2):
    return tuple([x - y for x, y in zip(v1, v2)])

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),
DIRS = {'N': UP, 'E': RIGHT, 'S': DOWN, 'W': LEFT}
FLIP = {'N': 'S', 'E': 'W', 'S': 'N', 'W': 'E'}

def turn(v, d='left'):
    n = -1 if d == 'left' else 1
    return VDIRS[(VDIRS.index(v) + n + len(VDIRS))%len(VDIRS)]


conns = {
    '|': 'NS',
    '-': 'EW',
    'L': 'NE',
    'J': 'NW',
    '7': 'SW',
    'F': 'SE',
}


def bfs(sset, inside, start):
    q = deque([start])
    while q:
        n = q.popleft()
        if n in sset or n in inside:
            continue
        inside.add(n)

        if n == (-1, -1):
            print('ABORT')
            raise IndexError

        for d in DIRS.values():
            q.append(vadd(n, d))


def go(m, squares, dir):
    sset = set(squares)
    inside = set()
    for i in range(1, len(squares)):
        c = squares[i-1]
        n = squares[i]
        d = vsub(n, c)
        td = turn(d, dir)
        side1 = vadd(c, td)
        side2 = vadd(n, td)
        print(f'{c=} {n=} {d=} {td=} {side1=} {side2=}')
        bfs(sset, inside, side1)
        bfs(sset, inside, side2)

    return len(inside)


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    m = defaultdict(lambda: '.')
    for y, l in enumerate(data):
        for x, c in enumerate(l):
            m[x, y] = c
            if c == 'S':
                start = (x, y)

    # Find what direction to start in
    for dname, x in DIRS.items():
        n = vadd(start, x)
        if m[n] in conns:
            k = conns[m[n]]
            out = None
            for i in range(2):
                if vadd(n, DIRS[k[i]]) == start:
                    out = i-1
                    ldir = dname
            if out is not None:
                break

    # Trace the path
    cur = n
    squares = [start, cur]
    while cur != start:
        print('???', cur, m[cur], conns[m[cur]], ldir)
        ldir = conns[m[cur]].replace(FLIP[ldir], '')
        cur = vadd(cur, DIRS[ldir])

        squares.append(cur)

    # Try looking on the LHS of the path, then try the RHS
    try:
        res = go(m, squares, 'left')
    except IndexError:
        res = go(m, squares, 'right')
    print(len(squares)//2)
    print(res)


if __name__ == '__main__':
    main(sys.argv)

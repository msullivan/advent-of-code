#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque

def vadd(v1, v2):
    return tuple([x + y for x, y in zip(v1, v2)])

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),
DIRS = {'U': UP, 'R': RIGHT, 'D': DOWN, 'L': LEFT }
ALL_DIRS = [(x, y) for x in [-1,0,1] for y in [-1,0,1] if not x == y == 0]

def turn(v, d='left'):
    n = -1 if d == 'left' else 1
    return VDIRS[(VDIRS.index(v) + n + len(VDIRS))%len(VDIRS)]


##############################
def draw(painted):
    minx = min(x for x, y in painted)
    miny = min(y for x, y in painted)
    maxx = max(x for x, y in painted)
    maxy = max(y for x, y in painted)

    l = ""
    # XXX: add reversed if needed
    for y in list((range(miny, maxy+1))):
        for x in range(minx, maxx+1):
            l += painted.get((x,y), ".")
        l += "\n"
    print(l)


# This is super silly and not how I did it at competition time.
# (Which was I ran it, and it hung, and I switched the direction.)
import asyncio
async def bfs(m, start):
    q = deque([start])
    while q:
        # lol.
        await asyncio.sleep(0)

        n = q.popleft()
        if m.get(n) == '#':
            continue
        m[n] = '#'

        for d in DIRS.values():
            q.append(vadd(n, d))

    return m

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    m = defaultdict(lambda: '.')

    pos = (0, 0)
    m[pos] = '#'
    for line in data:
        d, n, _ = line.split(' ')
        n = int(n)
        for _ in range(n):
            lpos, ldir = pos, DIRS[d]
            pos = vadd(pos, DIRS[d])
            m[pos] = '#'

    async def bfs_both():
        ir = vadd(lpos, turn(ldir, 'right'))
        il = vadd(lpos, turn(ldir, 'left'))
        done, pending = await asyncio.wait(
            [
                asyncio.create_task(bfs(m.copy(), il)),
                asyncio.create_task(bfs(m.copy(), ir)),
            ],
            return_when='FIRST_COMPLETED',
        )
        return await list(done)[0]

    draw(m)
    m = asyncio.run(bfs_both())
    print(len(m))

if __name__ == '__main__':
    main(sys.argv)

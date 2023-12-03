#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque

def vadd(v1, v2):
    return tuple([x + y for x, y in zip(v1, v2)])

ALL_DIRS = [(x, y) for x in [-1,0,1] for y in [-1,0,1] if not x == y == 0]

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    m = defaultdict(lambda: '.')
    for y, l in enumerate(data):
        for x, c in enumerate(l):
            m[x, y] = c

    sum = 0
    gears0 = defaultdict(set)
    gears = defaultdict(list)
    for y, l in enumerate(data):
        x = 0
        while x < len(l):
            if l[x].isnumeric():
                i = x
                while i < len(l) and l[i].isnumeric():
                    i += 1
                num = l[x:i]
                ispart = False
                for j in range(x, i):
                    for d in ALL_DIRS:
                        p = vadd(d, (j, y))
                        c = m[p]
                        if c != '.' and not c.isnumeric():
                            ispart = True
                            if c == '*':
                                if (i, y) not in gears0[p]:
                                    gears0[p].add((i, y))
                                    gears[p].append(int(num))
                if ispart:
                    # print("NUM", num)
                    sum += int(num)
                # else:
                #     print("NOT", num)

                x = i
            else:
                x += 1

    sum2 = 0
    for v in gears.values():
        if len(v) == 2:
            sum2 += v[0]*v[1]

    # print(gears)
    # print(m)
    print(sum)
    print(sum2)

if __name__ == '__main__':
    main(sys.argv)

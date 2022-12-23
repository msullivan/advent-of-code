#!/usr/bin/env python3

import sys
from collections import defaultdict

def vadd(v1, v2):
    return tuple([x + y for x, y in zip(v1, v2)])

UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),
ALL_DIRS = [(x, y) for x in [-1,0,1] for y in [-1,0,1] if not x == y == 0]

def turn(v, d='left'):
    n = -1 if d == 'left' else 1
    return VDIRS[(VDIRS.index(v) + n + len(VDIRS))%len(VDIRS)]

def draw(painted):
    minx = min(x for x, y in painted)
    miny = min(y for x, y in painted)
    maxx = max(x for x, y in painted)
    maxy = max(y for x, y in painted)

    l = ""
    # XXX: add reversed if needed
    for y in list((range(miny, maxy+1))):
        for x in range(minx, maxx+1):
            l += "." if (x, y) not in painted else "#"
        l += "\n"
    print(l)


ORDER = [UP, DOWN, LEFT, RIGHT]

def samed(v, p):
    return (v[0] and v[0] == p[0]) or (v[1] and v[1] == p[1])

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    elves = set()
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c == '#':
                elves.add((x, y))

    E = len(elves)
    draw(elves)

    for i in range(10000000000000):
        print(i)
        if i == 10:
            elves10 = elves
        targets = defaultdict(list)
        for elf in elves:
            if not any(vadd(d, elf) in elves for d in ALL_DIRS):
                targets[elf].append(elf)
                continue

            for prop in ORDER:
                if not any(
                    vadd(d, elf) in elves for d in ALL_DIRS if samed(d, prop)
                ):
                    # print(elf, 'proposing', prop)
                    targets[vadd(prop, elf)].append(elf)
                    break
            else:
                targets[elf].append(elf)
        # print(elves)
        # print(targets)
        new_elves = set()
        for target, xelves in targets.items():
            if len(xelves) == 1:
                new_elves.add(target)
            else:
                new_elves.update(xelves)

        ORDER.append(ORDER.pop(0))
        if elves == new_elves:
            break
        elves = new_elves
        # print()
        # print('====', i)
        # draw(elves)
        assert len(elves) == E

    minx = min(x for x, y in elves10)
    miny = min(y for x, y in elves10)
    maxx = max(x for x, y in elves10)
    maxy = max(y for x, y in elves10)
    total = (maxx-minx+1)*(maxy-miny+1)
    print()
    print(total-len(elves10))
    print(i+1)



if __name__ == '__main__':
    main(sys.argv)

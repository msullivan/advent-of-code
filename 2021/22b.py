#!/usr/bin/env python3
from __future__ import annotations

import sys
import re
from dataclasses import dataclass
from typing import List, NamedTuple, Tuple, Set

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]


class Pos(NamedTuple):
    x: int
    y: int
    z: int

    def dist(self, y: Pos) -> int:
        x = self
        return abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2])


@dataclass(frozen=True, order=True)
class Box:
    bot: Pos
    top: Pos

    def split_at(self, axis, val):
        atop = self.top[axis]
        abot = self.bot[axis]
        mid = val - 1
        assert mid >= abot
        assert atop != abot
        axname = "xyz"[axis]
        return [
            Box(self.bot, self.top._replace(**{axname: mid})),
            Box(self.bot._replace(**{axname: mid+1}), self.top),
        ]

    def overlap(self, other):
        return (
            self.top.x >= other.bot.x and other.top.x >= self.bot.x
            and self.top.y >= other.bot.y and other.top.y >= self.bot.y
            and self.top.z >= other.bot.z and other.top.z >= self.bot.z
        )

    def volume(self):
        assert self.top.x-self.bot.x >= 0
        assert self.top.y-self.bot.y >= 0
        assert self.top.z-self.bot.z >= 0
        return (self.top.x-self.bot.x+1)*(self.top.y-self.bot.y+1)*(self.top.z-self.bot.z+1)


def splitoff(n, m):
    if not n.overlap(m):
        return [n], None

    on = n

    fns = []
    for axis in [0,1,2]:
        if n.bot[axis] < m.bot[axis] <= n.top[axis]:
            l, n = n.split_at(axis, m.bot[axis])
            fns.append(l)

        if n.bot[axis] <= m.top[axis] < n.top[axis]:
            n, l = n.split_at(axis, m.top[axis]+1)
            fns.append(l)

    assert sum(x.volume() for x in fns) + n.volume() == on.volume()

    check(fns, {m})
    return fns, n


def check(lhs, rhs):
    return
    for x in lhs:
        for y in rhs:
            assert x == y or not x.overlap(y), (x,y)


def main(args):
    data = [s.strip() for s in sys.stdin if s.strip() and not s.startswith('#')]

    cmds = [(s.split(" ")[0], extract(s)) for s in data]
    cmds = [(s, ((x[0], x[2], x[4]), (x[1], x[3], x[5]))) for s, x in cmds]

    on = set()
    for i, (cmd, (lo, hi)) in enumerate(cmds):
        box = Box(Pos(*lo), Pos(*hi))
        print(i, cmd, box)

        new_on = set()
        for x in on:
            splits, _ = splitoff(x, box)
            new_on.update(splits)
        check(new_on, {box})

        if cmd == "on":
            new_on |= {box}
        on = new_on

        check(on, on)

        print(i, sum(x.volume() for x in on), len(on))

    # just for fun, also compute part 1
    part1 = {
        z
        for x in on
        if (z := splitoff(x, Box(Pos(-50,-50,-50), Pos(50,50,50)))[1])
    }

    print(sum(x.volume() for x in part1))
    print(sum(x.volume() for x in on))

if __name__ == '__main__':
    main(sys.argv)

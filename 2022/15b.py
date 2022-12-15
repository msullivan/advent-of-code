#!/usr/bin/env python3

"""Day 15.

For the original solution, I basically just copied my "honest"
solution from 2018/23 and reversed it.

I'm not sure why I didn't start by basically doing my "dishonest" Z3
trick from 2018, which got me second place. Very frustrating.

This version is cleaned up from that: this version isn't an
optimization problem--we know the goal is to find a point with zero
overlaps, so the heap/ordering machinery from there isn't useful.

The algorithm then is: maintain a stack of bounding boxes that might
contain the correct point. Iteratively take the top bounding box,
split it into 4 subboxes, and keep all the subboxes that might also
contain the correct point. If we find such a box that is actually just
a point, we are done.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import NamedTuple
import re


def extract(s: str) -> list[int]:
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]


def furthest(lo: int, hi: int, val: int) -> int:
    return lo if abs(lo - val) >= abs(hi - val) else hi


class Pos(NamedTuple):
    x: int
    y: int

    def dist(self, y: Pos) -> int:
        x = self
        return abs(x[0] - y[0]) + abs(x[1] - y[1])


@dataclass(frozen=True)
class Box:
    bot: Pos
    top: Pos

    def furthest_from(self, p: Pos) -> Pos:
        """Find the furthest point in the box to p"""
        return Pos(
            *[furthest(lo, hi, val) for lo, hi, val in zip(self.bot, self.top, p)]
        )

    def is_valid(self) -> bool:
        return all(b <= t for b, t in zip(self.bot, self.top))

    def split(self) -> set[Box]:
        """Split a box into 4 sub boxes"""
        mid = Pos(*[(c1 + c2) // 2 for c1, c2 in zip(self.bot, self.top)])
        mid1 = Pos(*[c+1 for c in mid])
        opts = [(self.bot, mid), (mid1, self.top)]
        return {x for x in (
            Box(Pos(oxl.x, oyl.y), Pos(oxh.x, oyh.y))
            for oxl, oxh in opts
            for oyl, oyh in opts
        ) if x.is_valid()}


@dataclass(frozen=True)
class Sensor:
    r: int
    p: Pos

    def contains(self, p: Pos) -> bool:
        return self.p.dist(p) <= self.r

    def overlaps_box(self, box: Box) -> bool:
        return self.contains(box.furthest_from(self.p))


def main(args: list[str]) -> None:
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [extract(s) for s in file]

    spots = []
    for line in data:
        a, b, c, d = line
        p1, p2 = Pos(a, b), Pos(c, d)
        spots.append(Sensor(p1.dist(p2), Pos(*p1)))

    MAX = 4000000
    orig_box = Box(Pos(0, 0), Pos(MAX, MAX))

    stack = [orig_box]
    while True:
        box = stack.pop()
        # When the box has been shrunk to a point, then we've
        # found it.
        if box.bot == box.top:
            break
        # Split up the box
        for sbox in box.split():
            overlapping = sum(bot.overlaps_box(sbox) for bot in spots)
            if overlapping == 0:
                stack.append(sbox)

    print(box.bot, box.top)
    print(box.bot.x * 4000000 + box.bot.y)


if __name__ == '__main__':
    main(sys.argv)

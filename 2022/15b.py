#!/usr/bin/env python3

"""

I basically just copied my "honest" solution from 2018/23 and reversed it.

I'm not sure why I didn't start by basically doing my "dishonest" Z3
trick from 2018, which got me second place. Very frustrating.


"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import NamedTuple
import random
import heapq
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vadd(v1, v2):
    return tuple(x + y for x, y in zip(v1, v2))

def vsub(v1, v2):
    return (v1[0]-v2[0], v1[1]-v2[1])

def mag(v):
    return abs(v[0]) + abs(v[1])

def furthest(lo: int, hi: int, val: int) -> int:
    lod = abs(lo - val)
    hid = abs(hi - val)
    return lo if lod >= hid else hi


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

    def split(self) -> Set[Box]:
        """Split a box into 4 sub boxes"""
        mid = Pos(*[(c1 + c2) // 2 for c1, c2 in zip(self.bot, self.top)])
        mid1 = Pos(*[c+1 for c in mid])
        opts = [(self.bot, mid), (mid1, self.top)]
        return {x for x in (
            Box(Pos(oxl.x, oyl.y), Pos(oxh.x, oyh.y))
            for oxl, oxh in opts
            for oyl, oyh in opts
        ) if x.is_valid()} - {self}


@dataclass(frozen=True)
class Bot:
    r: int
    p: Pos

    def contains(self, p: Pos) -> bool:
        return self.p.dist(p) <= self.r

    def overlaps_box(self, box: Box) -> bool:
        return self.contains(box.furthest_from(self.p))


def key(box: Box, bots: List[Bot]) -> Tuple[int, int, float, Box]:
    """Compute the key for the priority queue.

    The key is (number of bots in range of box, closest distance, the box).
    Number of bots is negative so the min-heap picks the largest.

    We actually stick a random number in the 3rd spot, to ensure that
    we don't need to compare boxes.
    """
    overlapping = sum(bot.overlaps_box(box) for bot in bots)
    closest = 0
    return (overlapping, closest, random.random(), box)



def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [extract(s) for s in file]

    xmin = 1000000000000000000
    xmax = -100000000000000000
    maxsz = 0
    spots = []
    beacs = set()
    for line in data:
        a, b, c, d = line
        xmin = min(xmin, a)
        xmax = max(xmax, b)
        p1, p2 = (a, b), (c, d)
        beacs.add(p2)
        sz = mag(vsub(p2, p1))
        print(sz)
        maxsz = max(sz, maxsz)
        spots.append(Bot(sz, Pos(*p1)))

    orig_box = Box(Pos(0, 0), Pos(4000000, 4000000))

    heap = [key(orig_box, spots)]

    while True:
        # Select the box with the best potential solution.
        overlapping, dist, _, box = heapq.heappop(heap)
        print(box, overlapping, box.bot.dist(box.top), dist, len(heap))
        # When the box has been shrunk to a point, then the upper
        # bound must be tight and this must be the optimal
        # place. (Because the heap ensures we work in order.)
        if box.bot == box.top:
            break

        # Otherwise split the box up and keep looking.
        for sbox in box.split():
            heapq.heappush(heap, key(sbox, spots))

    print(box.bot, box.top)
    print(box.bot.x * 4000000 + box.bot.y)


if __name__ == '__main__':
    main(sys.argv)

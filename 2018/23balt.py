from __future__ import annotations

# This is an honest solution for 23b, as opposed to the Z3 solution
# that I did at the time that got me 2nd place.

# This is pretty directly adapted from
# https://github.com/sim642/adventofcode/blob/master/src/main/scala/eu/sim642/adventofcode2018/Day23.scala,
# which I read, thought about, then reimplemented in Python.

# I think this works? Maybe I'll document it.

import sys

import sys
import re
import heapq
from typing import *


def extract(s: str) -> List[int]:
    return [int(x) for x in re.findall(r'-?\d+', s)]


def clamp(lo: int, hi: int, val: int) -> int:
    return min(hi, max(lo, val))


class Pos(NamedTuple):
    x: int
    y: int
    z: int

    def dist(self, y: Pos) -> int:
        x = self
        return abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2])


class Box(NamedTuple):
    bot: Pos
    top: Pos

    def closest_to(self, p: Pos) -> Pos:
        return Pos(
            *[clamp(lo, hi, val) for lo, hi, val in zip(self.bot, self.top, p)]
        )


class Bot(NamedTuple):
    r: int
    p: Pos

    def contains(self, p: Pos) -> bool:
        return self.p.dist(p) <= self.r

    def overlaps_box(self, box: Box) -> bool:
        return self.contains(box.closest_to(self.p))


def compute_upper(bots: List[Bot], box: Box) -> int:
    return sum(bot.overlaps_box(box) for bot in bots)


def split_box(box: Box) -> Set[Box]:
    mid = Pos(*[(c1 + c2) // 2 for c1, c2 in zip(box.bot, box.top)])
    mid1 = Pos(*[c+1 for c in mid])
    opts = [(box.bot, mid), (mid1, box.top)]
    boxes = {
        Box(Pos(oxl.x, oyl.y, ozl.z), Pos(oxh.x, oyh.y, ozh.z))
        for oxl, oxh in opts
        for oyl, oyh in opts
        for ozl, ozh in opts
    }
    return boxes


ZERO = Pos(0,0,0)


def key(bots: List[Bot], box: Box) -> Tuple[int, int, Box]:
    closest = box.closest_to(ZERO).dist(ZERO)
    return (-compute_upper(bots, box), closest, box)


def main(args: List[str]) -> None:
    data = [extract(s.strip()) for s in sys.stdin]
    bots = [Bot(x[3], Pos(*x[:-1])) for x in data]

    coords = list(zip(*[x.p for x in bots]))
    mins = Pos(*[min(cs) for cs in coords])
    maxes = Pos(*[max(cs) for cs in coords])
    orig_box = Box(mins, maxes)

    heap = [key(bots, orig_box)]

    while True:
        nupper, dist, box = heapq.heappop(heap)
        upper = -nupper
        print(box, upper, len(heap))
        # When the box has been shrunk to a point, then the upper
        # bound must be tight and this must be the optimal
        # place. (Because the heap ensures we work in order.)
        if box.bot == box.top:
            print(box.bot)
            print(dist)
            break

        for sbox in split_box(box):
            heapq.heappush(heap, key(bots, sbox))


if __name__ == '__main__':
    main(sys.argv)

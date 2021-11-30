from __future__ import annotations

"""
This is an honest solution for 23b, as opposed to the Z3 solution
that I did at the time that got me 2nd place.

It runs in a little over a second on my machines.

The key concept in the algorithm is the bounding box, a cube that contains a region
of space, represented here by its "bottom" and "top" corners. For a bounding box,
it is easy to compute both the number of bots that are in range of *any point* inside
the box and the minimum distance from the origin in the box.

Those represent an upper bound on the best possible solution inside a box.
Then, we maintain a set of potential bounding boxes. At each step, we select
the potential bounding box that has the best potential solution. We then discard
that box and split it into 8 sub-boxes, and add them to the set.

It may be that none of the new boxes have a potential solution that is
as good the outer one, and this may result in the best available
solution in the next step not being one of the new boxes.

If the best potential bounding box is just a single point, then it
isn't "potential" anymore, and we have found our answer.

We represent the set of potential boxes using a priority queue/heap,
since that is the notionally right way to do it, since it allows us
to select the best element in log time. But also the heap never gets
very big and it is really just as fast to scan the whole list.

In practice, we settle on the correct number of bots after around 5
steps, and the whole thing takes a bit more than a hundred.

This is pretty directly adapted from
https://github.com/sim642/adventofcode/blob/master/src/main/scala/eu/sim642/adventofcode2018/Day23.scala,
which I read, thought about, then reimplemented in Python. That version also has
a notion of "lower" bounds, and searches until the lower and upper bounds coincide.
That isn't necessary, so I dropped it: we just search until the best candidate
bounding box is a point, which means the upper bound must be accurate.
"""

import sys

import random
import re
import heapq
from dataclasses import dataclass
from typing import List, NamedTuple, Tuple, Set


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


ZERO = Pos(0,0,0)


@dataclass(frozen=True)
class Box:
    bot: Pos
    top: Pos

    def closest_to(self, p: Pos) -> Pos:
        """Find the closest point in the box to p"""
        return Pos(
            *[clamp(lo, hi, val) for lo, hi, val in zip(self.bot, self.top, p)]
        )

    def split(self) -> Set[Box]:
        """Split a box into 8 sub boxes"""
        mid = Pos(*[(c1 + c2) // 2 for c1, c2 in zip(self.bot, self.top)])
        mid1 = Pos(*[c+1 for c in mid])
        opts = [(self.bot, mid), (mid1, self.top)]
        return {
            Box(Pos(oxl.x, oyl.y, ozl.z), Pos(oxh.x, oyh.y, ozh.z))
            for oxl, oxh in opts
            for oyl, oyh in opts
            for ozl, ozh in opts
        } - {self}


@dataclass(frozen=True)
class Bot:
    r: int
    p: Pos

    def contains(self, p: Pos) -> bool:
        return self.p.dist(p) <= self.r

    def overlaps_box(self, box: Box) -> bool:
        return self.contains(box.closest_to(self.p))


def key(box: Box, bots: List[Bot]) -> Tuple[int, int, float, Box]:
    """Compute the key for the priority queue.

    The key is (-number of bots in range of box, closest distance, the box).
    Number of bots is negative so the min-heap picks the largest.

    We actually stick a random number in the 3rd spot, to ensure that
    we don't need to compare boxes.
    """
    overlapping = sum(bot.overlaps_box(box) for bot in bots)
    closest = box.closest_to(ZERO).dist(ZERO)
    return (-overlapping, closest, random.random(), box)


def main(args: List[str]) -> None:
    data = [extract(s.strip()) for s in sys.stdin]
    bots = [Bot(x[3], Pos(*x[:-1])) for x in data]

    # Compute part 1 too, why not
    loudest = max(bots, key=lambda bot: bot.r)
    part_1 = sum(loudest.contains(bot.p) for bot in bots)

    # Create a bounding box that surrounds all the points. This works
    # because there's no way for the *closest* optimal point to be
    # outside all of the points.
    coords = list(zip(*[x.p for x in bots]))
    mins = Pos(*[min(cs) for cs in coords])
    maxes = Pos(*[max(cs) for cs in coords])
    orig_box = Box(mins, maxes)

    heap = [key(orig_box, bots)]

    while True:
        # Select the box with the best potential solution.
        neg_overlapping, dist, _, box = heapq.heappop(heap)
        print(box, -neg_overlapping, box.bot.dist(box.top), dist, len(heap))
        # When the box has been shrunk to a point, then the upper
        # bound must be tight and this must be the optimal
        # place. (Because the heap ensures we work in order.)
        if box.bot == box.top:
            break

        # Otherwise split the box up and keep looking.
        for sbox in box.split():
            heapq.heappush(heap, key(sbox, bots))

    print()
    print(box.bot)
    print(part_1)
    print(dist)


if __name__ == '__main__':
    main(sys.argv)

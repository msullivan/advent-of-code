#!/usr/bin/env python3

"""
Implementation of day 14 part 2 using Binary Decision Diagrams.

BDDs are an (often!) efficient representation of boolean functions---or,
equivalently, of sets of N-bit numbers (where a number x is a member of
the set if f(x) = 1).

BDDs are actually super sweet! I really enjoyed learning about them for this.

Capable of solving harder inputs with lots of Xs, like the part 1 example,
or the inputs from https://www.reddit.com/r/adventofcode/comments/kcybyr/2002_day_14_part_2_but_what_if_the_input_is_harder/.

(I skimmed the first few pages of the Knuth section describing them
and then put it away and figured out these versions of the
construction algorithms myself---though they aren't that hard, once
you have the data structure designed. I did read Knuth's Algorithm C for
counting. Knuth's algorithms seem to be mostly iterative and bottom up,
while my implementations are aggressively recursive and memoized.)

TODO: Real documentation
"""

from __future__ import annotations

from typing import Tuple, Callable, Set, Iterator, TypeVar

from dataclasses import dataclass
from functools import lru_cache
import sys
import re


T = TypeVar('T')

def memoize(x: T) -> T:
    """lru_cache wrapper to pass maxsize and give the right type"""
    return lru_cache(maxsize=None)(x)  # type: ignore


def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]


@dataclass(eq=False, frozen=True)
class Node:
    var: int
    false: Node
    true: Node

    @classmethod
    @memoize
    def new(cls, var: int, false: Node, true: Node) -> Node:
        if false is true:
            return false
        return Node(var, false, true)


class LeafNode(Node):
    def __init__(self, val: bool) -> None:
        object.__setattr__(self, 'var', 1000000000)
        self.val = val

    def __repr__(self) -> str:
        return f'<{self.val}>'


TrueLeaf = LeafNode(True)
FalseLeaf = LeafNode(False)


def addr_mask_to_bdd(addr: Tuple[int, int], nbits: int) -> Node:
    val_bits, mask_bits = addr

    node: Node = TrueLeaf
    for i in range(nbits-1, -1, -1):
        # generate no node if the bit is an X
        if not (mask_bits & (1 << i)):
            if val_bits & (1 << i):
                node = Node.new(var=i, false=FalseLeaf, true=node)
            else:
                node = Node.new(var=i, false=node, true=FalseLeaf)

    return node

# not actually used anymore (because I implemented andn directly)
@memoize
def negate_bdd(bdd: Node) -> Node:
    if bdd is TrueLeaf:
        return FalseLeaf
    elif bdd is FalseLeaf:
        return TrueLeaf
    else:
        return Node.new(
            bdd.var, false=negate_bdd(bdd.false), true=negate_bdd(bdd.true))


def merge_bdds(lhs: Node, rhs: Node, f: Callable[[Node, Node], Node]) -> Node:
    """Handle the non-base-case portion of common binary ops"""
    # If both nodes have the same variable, recurse on both of them
    if lhs.var == rhs.var:
        return Node.new(lhs.var,
                        false=f(lhs.false, rhs.false),
                        true=f(lhs.true, rhs.true))
    # If one variable is earlier than the other, only recurse on the
    # subtrees of the earlier node.
    elif lhs.var < rhs.var:
        return Node.new(lhs.var,
                        false=f(lhs.false, rhs),
                        true=f(lhs.true, rhs))
    else:
        return Node.new(rhs.var,
                        false=f(lhs, rhs.false),
                        true=f(lhs, rhs.true))


# not actually used anymore (because I implemented andn directly)
@memoize
def and_bdds(lhs: Node, rhs: Node) -> Node:
    if lhs is TrueLeaf and rhs is TrueLeaf:
        return TrueLeaf
    elif lhs is FalseLeaf or rhs is FalseLeaf:
        return FalseLeaf
    else:
        return merge_bdds(lhs, rhs, and_bdds)


@memoize
def andn_bdds(lhs: Node, rhs: Node) -> Node:
    if lhs is TrueLeaf and rhs is FalseLeaf:
        return TrueLeaf
    elif lhs is FalseLeaf or rhs is TrueLeaf:
        return FalseLeaf
    else:
        return merge_bdds(lhs, rhs, andn_bdds)


@memoize
def or_bdds(lhs: Node, rhs: Node) -> Node:
    if lhs is TrueLeaf or rhs is TrueLeaf:
        return TrueLeaf
    elif lhs is FalseLeaf and rhs is FalseLeaf:
        return FalseLeaf
    else:
        return merge_bdds(lhs, rhs, or_bdds)


def count_bdd(bdd: Node, nbits: int) -> int:
    def gvar(bdd: Node) -> int:
        return nbits if isinstance(bdd, LeafNode) else bdd.var

    @lru_cache(maxsize=None)
    def count(bdd: Node) -> int:
        if isinstance(bdd, LeafNode):
            return int(bdd.val)
        fsols, tsols = count(bdd.false), count(bdd.true)
        # if there are gaps in the variables, we need to scale up by powers of two
        fsols *= 1 << (gvar(bdd.false) - bdd.var - 1)
        tsols *= 1 << (gvar(bdd.true) - bdd.var - 1)
        return fsols + tsols

    return count(bdd) * (1 << gvar(bdd))


# eval and enum aren't actually used in the solution but I used them
# for testing and also they are cool
def eval_bdd(nobe: Node, bits: int) -> bool:
    if isinstance(nobe, LeafNode):
        return nobe.val

    if bits & (1 << nobe.var):
        return eval_bdd(nobe.true, bits)
    else:
        return eval_bdd(nobe.false, bits)


def enum_bdd(bdd: Node, nbits: int) -> Iterator[int]:
    def gvar(bdd: Node) -> int:
        return nbits if isinstance(bdd, LeafNode) else bdd.var

    def enum(bdd: Node, i: int) -> Iterator[int]:
        if bdd is FalseLeaf:
            return

        if i < gvar(bdd):
            for v in enum(bdd, i + 1):
                yield v
                yield v | (1 << i)
        else:
            if isinstance(bdd, LeafNode):
                if bdd.val:
                    yield 0
            else:
                for v in enum(bdd.false, i + 1):
                    yield v
                for v in enum(bdd.true, i + 1):
                    yield v | (1 << i)

    return enum(bdd, 0)


def bdd_nodes(bdd: Node) -> Set[Node]:
    nobes = set()
    def find(node: Node) -> None:
        if node in nobes:
            return
        nobes.add(node)
        if not isinstance(node, LeafNode):
            find(node.true)
            find(node.false)

    find(bdd)
    return nobes


def bdd_size(bdd: Node) -> int:
    return len(bdd_nodes(bdd))


def main(args):
    data = [s.strip() for s in sys.stdin]

    nbits = 0

    # Construct a list of instructions that have the mask information built in
    writes = []
    for line in data:
        if "mask" in line:
            smask = line.split(" = ")[1]
            mmask = int(smask.replace("1", "0").replace("X", "1"), 2)
            mval = int(smask.replace("X", "0"), 2)
            nbits = max(nbits, len(smask))
        else:
            addr, val = extract(line)
            addr |= mval
            addr &= ~mmask
            writes.append(((addr, mmask), val))

    # run backwards through the instructions updating the counts
    count = 0
    after_bdd: Node = FalseLeaf
    for i, (mask, val) in reversed(list(enumerate(writes))):
        # Compute a bdd representing the set of addresses written by this instruction
        bdd = addr_mask_to_bdd(mask, nbits)

        # Find all addresses written by the current write and *not*
        # by any subsequent write.
        andn_bdd = andn_bdds(bdd, after_bdd)
        # Score it
        size = count_bdd(andn_bdd, nbits)
        count += val * size

        # Update the bdd of all later addresses
        after_bdd = or_bdds(after_bdd, bdd)
        # I would like to spew the size of after_bdd but that actually
        # slows things down a fair bit!
        print(f'{i=} {size=:x} {count=} {bdd_size(bdd)=}')

    print(f'union size: {bdd_size(after_bdd)}, last and size: {bdd_size(andn_bdd)}')

    print(count)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

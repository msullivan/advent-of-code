#!/usr/bin/env python3

from __future__ import annotations

from typing import *

from dataclasses import dataclass
from functools import lru_cache
import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

@dataclass(eq=False, frozen=True)
class Node:
    var: int
    false: Node
    true: Node

    @classmethod
    @lru_cache(maxsize=None)
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


@lru_cache(maxsize=None)
def negate_bdd(bdd: Node) -> Node:
    if bdd is TrueLeaf:
        return FalseLeaf
    elif bdd is FalseLeaf:
        return TrueLeaf
    else:
        return Node.new(
            bdd.var, false=negate_bdd(bdd.false), true=negate_bdd(bdd.true))


@lru_cache(maxsize=None)
def and_bdds(lhs: Node, rhs: Node) -> Node:
    if lhs is TrueLeaf and rhs is TrueLeaf:
        return TrueLeaf
    elif lhs is FalseLeaf or rhs is FalseLeaf:
        return FalseLeaf
    elif lhs.var == rhs.var:
        return Node.new(lhs.var,
                        false=and_bdds(lhs.false, rhs.false),
                        true=and_bdds(lhs.true, rhs.true))
    elif lhs.var < rhs.var:
        return Node.new(lhs.var,
                        false=and_bdds(lhs.false, rhs),
                        true=and_bdds(lhs.true, rhs))
    else:
        return Node.new(rhs.var,
                        false=and_bdds(lhs, rhs.false),
                        true=and_bdds(lhs, rhs.true))


@lru_cache(maxsize=None)
def or_bdds(lhs: Node, rhs: Node) -> Node:
    if lhs is TrueLeaf or rhs is TrueLeaf:
        return TrueLeaf
    elif lhs is FalseLeaf and rhs is FalseLeaf:
        return FalseLeaf
    elif lhs.var == rhs.var:
        return Node.new(lhs.var,
                        false=or_bdds(lhs.false, rhs.false),
                        true=or_bdds(lhs.true, rhs.true))
    elif lhs.var < rhs.var:
        return Node.new(lhs.var,
                        false=or_bdds(lhs.false, rhs),
                        true=or_bdds(lhs.true, rhs))
    else:
        return Node.new(rhs.var,
                        false=or_bdds(lhs, rhs.false),
                        true=or_bdds(lhs, rhs.true))


# def or_bdds(lhs: Node, rhs: Node) -> Node:
#     # ... minus one point for each additional law
#     return negate_bdd(and_bdds(negate_bdd(lhs), negate_bdd(rhs)))


def count_bdd(bdd: Node, nbits: int) -> Node:
    def gvar(bdd: Node) -> int:
        return nbits if isinstance(bdd, LeafNode) else bdd.var

    @lru_cache(maxsize=None)
    def count(bdd: Node) -> Node:
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


def enum_bdd(bdd: Node, nbits: int) -> Node:
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

    writes = []
    for line in data:
        if "mask" in line:
            smask = line.split(" = ")[1]
            mmask = int(smask.replace("1", "0").replace("X", "1"), 2)
            mval = int(smask.replace("X", "0"), 2)
            nbits = max(nbits, len(smask))
            # print(hex(mmask), hex(mval))
        else:
            addr, val = extract(line)
            addr |= mval
            addr &= ~mmask
            writes.append(((addr, mmask), val))

    # nbits = 8  # hack!

    bdds = [addr_mask_to_bdd(mask, nbits) for mask, _ in writes]

    # run backwards through the list and progressively union them all up
    count = 0
    cur_union: Node = FalseLeaf
    for i, ((_, val), bdd) in enumerate(zip(writes, reversed(bdds))):
        andn_bdd = and_bdds(bdd, negate_bdd(cur_union))
        size = count_bdd(andn_bdd, nbits)
        count += val * size

        cur_union = or_bdds(cur_union, bdd)
        print("sizes", i, size, bdd_size(bdd)) #, bdd_size(cur_union))

    print(count)



if __name__ == '__main__':
    sys.exit(main(sys.argv))

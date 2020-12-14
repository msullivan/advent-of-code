#!/usr/bin/env python3

from __future__ import annotations

from typing import *

from dataclasses import dataclass
from collections import defaultdict
from functools import lru_cache
import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

from itertools import chain, combinations
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


@dataclass(eq=False, frozen=True)
class Node:
    var: int
    false: Node
    true: Node

    @classmethod
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


def negate_bdd(bdd: Node) -> Node:
    @lru_cache(maxsize=None)
    def neg(bdd: Node) -> Node:
        if bdd is TrueLeaf:
            return FalseLeaf
        elif bdd is FalseLeaf:
            return TrueLeaf
        else:
            return Node.new(bdd.var, false=neg(bdd.false), true=neg(bdd.true))
    return neg(bdd)


def and_bdds(lhs: Node, rhs: Node) -> Node:
    mk = lru_cache(maxsize=None)(Node.new)

    @lru_cache(maxsize=None)
    def band(lhs: Node, rhs: Node) -> Node:
        if lhs is TrueLeaf and rhs is TrueLeaf:
            return TrueLeaf
        elif lhs is FalseLeaf or rhs is FalseLeaf:
            return FalseLeaf
        elif lhs.var == rhs.var:
            return mk(lhs.var,
                      false=band(lhs.false, rhs.false),
                      true=band(lhs.true, rhs.true))
        elif lhs.var < rhs.var:
            return mk(lhs.var,
                      false=band(lhs.false, rhs),
                      true=band(lhs.true, rhs))
        else:
            return mk(rhs.var,
                      false=band(lhs, rhs.false),
                      true=band(lhs, rhs.true))
    return band(lhs, rhs)


def or_bdds(lhs: Node, rhs: Node) -> Node:
    # ... minus one point for each additional law
    return negate_bdd(and_bdds(negate_bdd(lhs), negate_bdd(rhs)))


def eval_bdd(nobe: Node, bits: int) -> bool:
    if isinstance(nobe, LeafNode):
        return nobe.val

    if bits & (1 << nobe.var):
        return eval_bdd(nobe.true, bits)
    else:
        return eval_bdd(nobe.false, bits)


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


def enum_bdd(bdd: Node, nbits: int) -> Node:
    def gvar(bdd: Node) -> int:
        return nbits if isinstance(bdd, LeafNode) else bdd.var

    def enum(bdd: Node, i: int) -> Iterator[int]:
        if bdd is FalseLeaf:
            return

        if i < gvar(bdd):
            for v in enum(bdd, i + 1):
                # print("double yield", i, gvar(bdd))
                yield v
                yield v | (1 << i)
        else:
            if isinstance(bdd, LeafNode):
                if bdd.val:
                    # print("yielding", i)
                    yield 0
            else:
                for v in enum(bdd.false, i + 1):
                    yield v
                for v in enum(bdd.true, i + 1):
                    yield v | (1 << i)

    return enum(bdd, 0)


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

    print(writes)
    print(nbits)
    bdd = addr_mask_to_bdd(writes[0][0], nbits)
    bdd2 = addr_mask_to_bdd(writes[1][0], nbits)
    print(bdd)
    # bdd1_vals = {i for i in range(1 << nbits) if eval_bdd(bdd, i)}
    # print(bdd1_vals)
    nbdd = negate_bdd(bdd)
    # print([i for i in range(1 << nbits) if eval_bdd(nbdd, i)])

    # bdd2_vals = {i for i in range(1 << nbits) if eval_bdd(bdd2, i)}
    # print(bdd2_vals)
    # print(bdd1_vals & bdd2_vals)

    andbdd = and_bdds(bdd, bdd2)
    # print(andbdd)
    # andbdd_vals = {i for i in range(1 << nbits) if eval_bdd(andbdd, i)}
    # print("brute forced", andbdd_vals)
    # print(len(andbdd_vals))
    # for x in enum_bdd(andbdd, nbits):
    #     print("got one", x)


    argh = list(enum_bdd(andbdd, nbits))
    andbdd_vals2 = set(enum_bdd(andbdd, nbits))
    print("enumed", andbdd_vals2)
    print("argh", sorted(argh))


    print(count_bdd(andbdd, nbits))



if __name__ == '__main__':
    sys.exit(main(sys.argv))

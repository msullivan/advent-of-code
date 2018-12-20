#!/usr/bin/env python3
"""A hashlife style solution for day 12.

TODO: document this!
"""

from __future__ import annotations

import sys
sys.excepthook = sys.__excepthook__  # I am so mad about ubuntu's excepthook

from collections import defaultdict, deque
from typing import Dict, Union, Tuple, Optional, Any
from dataclasses import dataclass

@dataclass(eq=False, frozen=True)
class Node:
    level: int
    left: Node
    right: Node
    plants: str
    live: int
    # The score if the left hand of the node was at 0
    score: int

    def centered_score(self) -> int:
        return self.score - self.live * (1 << (self.level - 1))

class EmptyLeafNode(Node):
    def __init__(self) -> None:
        pass
    def __repr__(self) -> str:
        return '<leaf>'

hashconser: Dict[Union[str, Tuple[Node, Node]], Node] = {}
update_rule: Dict[str, str] = {}

step_cache: Dict[Tuple[Node, int], Node] = {}

LEAF = EmptyLeafNode()

def new_plants(plants: str) -> Node:
    if plants not in hashconser:
        # NB must be a power of 2
        if len(plants) > 2:
            i = len(plants) // 2
            hashconser[plants] = new(new_plants(plants[:i]), new_plants(plants[i:]))
        else:
            real = [i for i, v in enumerate(plants) if v == '#']
            hashconser[plants] = Node(1, LEAF, LEAF, plants, len(real), sum(real))
    return hashconser[plants]

def new(left: Node, right: Node) -> Node:
    key = (left, right)
    if key not in hashconser:
        assert left.level == right.level
        plants = ""
        # cache plants in nodes up to size 8
        if left.level <= 2:
            plants = left.plants + right.plants
        score = left.score + right.score + (1 << left.level) * right.live
        hashconser[key] = Node(left.level + 1, left, right, plants,
                               left.live + right.live, score)
    return hashconser[key]

def step_leaf(leaf: Node) -> Node:
    """Evaluate a size 8 node, producing a size 4 node of the middle"""
    assert leaf.level == 3
    assert len(leaf.plants) == 8
    str = "".join(update_rule.get(leaf.plants[i-2:i+3], '.') for i in range(2, 6))
    assert len(str) == 4
    return new_plants(str)

def step_interior(node: Node, to_skip: int) -> Node:
    """Step an interior node of level n, producing a node of level n-1"""
    assert node.level > 3
    if (node, to_skip) in step_cache:
        return step_cache[node, to_skip]

    next = max(to_skip - 1, 0)
    left = step(node.left, next)
    right = step(node.right, next)
    mid = step(new(node.left.right, node.right.left), next)

    if to_skip > 0:
        val = new(
            new(left.right, mid.left),
            new(mid.right, right.left)
        )
    else:
        val = new(
            step(new(left, mid), 0),
            step(new(mid, right), 0)
        )
    step_cache[node, to_skip] = val

    return val

def step(node: Node, to_skip: int) -> Node:
    """Evaluate a node of level n, producing a node of level n-1"""
    if node.level == 3:
        res = step_leaf(node)
    else:
        res = step_interior(node, to_skip)
    return res

def empty(level: int) -> Node:
    if level == 1:
        return new_plants('..')
    else:
        x = empty(level - 1)
        return new(x, x)

def expand(node: Node) -> Node:
    x = empty(node.level - 1)
    return new(new(x, node.left), new(node.right, x))

def try_shrink(node: Node) -> Node:
    if node.left.left.live == 0 and node.right.right.live == 0:
        return new(node.left.right, node.right.left)
    else:
        return node

def next_power_2(x):
    return 1 << (x-1).bit_length()

def largest_power_2(n):
    return 1 << (n.bit_length() - 1)

def main(args):
    target = 50_000_000_000
    if args[1:]:
        target = int(args[1])

    data = [s.strip() for s in sys.stdin]
    stuff = [x.split(' ') for x in data[2:]]
    stuff = dict([(x, z) for x, _, z in stuff])
    update_rule.update(stuff)

    initial = data[0].split(" ")[2]
    size = max(next_power_2(len(initial)), 8)
    initial += '.' * (size - len(initial))

    state_0 = new_plants(initial)
    state = new(empty(state_0.level), state_0)

    steps = 0
    while steps < target:
        state = expand(expand(state))
        natural_amount = 1 << (state.level - 3)
        if steps + natural_amount <= target:
            print("stepping", natural_amount)
            steps += natural_amount
            state = step(state, 0)
        else:
            small_step = largest_power_2(target - steps)
            print("under stepping", small_step)
            steps += small_step
            idx = state.level - 2 - small_step.bit_length()
            state = step(state, idx)

        print('steps={}, score={}, live={}, table size={}'.format(
            steps, state.centered_score(), state.live, len(hashconser)))

    print(state.centered_score())

if __name__ == '__main__':
    sys.exit(main(sys.argv))

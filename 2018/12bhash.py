#!/usr/bin/env python3.7
"""A hashlife style solution for day 12.

TODO: document this!
"""

from __future__ import annotations

import sys

from collections import defaultdict, deque
from typing import Dict, List, Union, Tuple, Optional, Any
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
        hashconser[key] = Node(
            left.level + 1, left, right, plants, left.live + right.live, score
        )
    return hashconser[key]

def step_leaf(leaf: Node) -> Node:
    """Evaluate a size 8 node, producing a size 4 node of the middle"""
    assert leaf.level == 3
    assert len(leaf.plants) == 8
    str = "".join(update_rule.get(leaf.plants[i-2:i+3], '.') for i in range(2, 6))
    assert len(str) == 4
    return new_plants(str)

def step_interior(node: Node, steps_power: int) -> Node:
    """Step an interior node of level n, producing a node of level n-1.

    Evaluate for up to 2**steps_power steps.
    """
    assert node.level > 3
    if (node, steps_power) in step_cache:
        return step_cache[node, steps_power]

    left = step(node.left, steps_power)
    right = step(node.right, steps_power)
    mid = step(new(node.left.right, node.right.left), steps_power)

    if node.level - 2 > steps_power:
        val = new(
            new(left.right, mid.left),
            new(mid.right, right.left),
        )
    else:
        val = new(
            step(new(left, mid), node.level),
            step(new(mid, right), node.level),
        )
    step_cache[node, steps_power] = val

    return val

def step(node: Node, to_skip: int) -> Node:
    """Evaluate a node of level n, producing a node of level n-1"""
    if node.level == 3:
        res = step_leaf(node)
    else:
        res = step_interior(node, to_skip)
    return res

def empty(level: int) -> Node:
    """Create an empty node at level"""
    if level == 1:
        return new_plants('..')
    else:
        x = empty(level - 1)
        return new(x, x)

def expand(node: Node) -> Node:
    """Expand a node to be one level higher but have the same contents."""
    x = empty(node.level - 1)
    return new(new(x, node.left), new(node.right, x))

def try_shrink(node: Node) -> Node:
    """If possible, shrink a node to be one level lower but have the same contents."""
    if node.left.left.live == 0 and node.right.right.live == 0:
        return new(node.left.right, node.right.left)
    else:
        return node

def next_power_2(x: int) -> int:
    """Return the smallest power of 2 greater than or equal to x"""
    return 1 << (x-1).bit_length()

def last_power_2(n: int) -> int:
    """Return the largest power of 2 less than or equal to x"""
    return 1 << (n.bit_length() - 1)

def parse_input(data: List[str]) -> Tuple[Dict[str, str], str]:
    rule_parts = [x.split(' ') for x in data[2:]]
    update_rules = dict([(x, z) for x, _, z in rule_parts])

    initial = data[0].split(" ")[2]
    size = max(next_power_2(len(initial)), 8)
    initial += '.' * (size - len(initial))

    return update_rules, initial

def run(state: Node, target: int) -> Node:
    # Expand the node so that it can be immediately stepped as far as we need.
    while (1 << (state.level - 3)) < target:
        state = expand(state)

    # Evaluate until we hit it!
    steps = 0
    while steps < target:
        # step can only evaluate a power-of-two number of steps, so
        # find the largest power of two less than our distance to go.
        amount = last_power_2(target - steps)

        print("stepping", amount)
        steps += amount
        state = step(expand(state), amount.bit_length())

        print(
            'steps={}, score={}, live={}, table size={}'.format(
                steps, state.centered_score(), state.live, len(hashconser)
            )
        )

    return state

def main(args) -> None:
    target = 50_000_000_000
    if args[1:]:
        target = int(args[1])

    rules, initial = parse_input([s.strip() for s in sys.stdin])
    update_rule.update(rules)

    # The provided initial state starts at zero, but our node wants to
    # be centered on zero, so put an empty node to the left.
    state_0 = new_plants(initial)
    state = new(empty(state_0.level), state_0)

    state = run(state, target)

    print(state.centered_score())

if __name__ == '__main__':
    main(sys.argv)

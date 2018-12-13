#!/usr/bin/env python3

from __future__ import annotations

import sys
sys.excepthook = sys.__excepthook__

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

hashconser: Dict[Union[str, Tuple[Node, Node]], Node] = {}
update_rule: Dict[str, str] = {}
step_cache: Dict[Tuple[Node, int], Node] = {}

# XXX: do something more clever!
dummy: Any = None

def new_plants(plants: str) -> Node:
    if plants not in hashconser:
        print(plants)
        # NB must be a power of 2
        if len(plants) > 2:
            i = len(plants) // 2
            hashconser[plants] = new(new_plants(plants[:i]), new_plants(plants[i:]))
        else:
            real = [i for i, v in enumerate(plants) if v == '#']
            hashconser[plants] = Node(1, dummy, dummy, plants, len(real), sum(real))
    return hashconser[plants]

def new(left: Node, right: Node) -> Node:
    key = (left, right)
    if key not in hashconser:
        print(left.level, right.level)
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
    str = "".join(update_rule[leaf.plants[i-2:i+3]] for i in range(2, 6))
    assert len(str) == 4
    return new_plants(str)

def step_interior(node: Node, to_skip: int) -> Node:
    """Step an interior node of level n, producing a node of level n-1"""
    if (node, to_skip) in step_cache:
        return step_cache[node, to_skip]

    next = max(to_skip - 1, 0)
    left = step(node.left, next)
    right = step(node.right, next)
    mid = step(new(node.left.right, node.right.left), next)

    n0 = new(left.right, mid.left)
    n1 = new(mid.right, right.left)
    if to_skip == 0:
        n0 = step(n0, 0)
        n1 = step(n0, 1)

    step_cache[node, to_skip] = new(n0, n1)
    return step_cache[node, to_skip]

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
    return 1<<(x-1).bit_length()

def main(args):
    data = [s.strip() for s in sys.stdin]
    stuff = [x.split(' ') for x in data[2:]]
    stuff = dict([(x, z) for x, _, z in stuff])
    update_rule.update(stuff)

    initial = data[0].split(" ")[2]
    print(len(initial))
    initial += '.' * (next_power_2(len(initial)) - len(initial))
    print(len(initial))

    state_0 = new_plants(initial)
    state = new(empty(state_0.level), state_0)
    print(state)
    print(len(hashconser))

    # TEST
    plants = defaultdict(lambda: '.')
    for i, x in enumerate(initial):
        plants[i] = x
    real = tuple(k for k, v in plants.items() if v == '#')
    print(i, len(real), real, sum(real))

    for i in range(20):
        state = expand(expand(state))
        state = step(state, state.level)
        state = try_shrink(state)

    # ASDF
    print(state.score - state.live * (1 << (state.level - 1)) , state.live)

    # return
    # stuff = [x.split(' ') for x in data[2:]]
    # stuff = dict([(x, z) for x, _, z in stuff])
    # update_rule.update(stuff)

    # seen = {}

    # for i in range(50000000000):
    #     if i % 10000 == 0: print(i)
    #     new = defaultdict(lambda: '.')
    #     bottom = min(plants.keys())
    #     top = max(plants.keys())
    #     for j in range(bottom-3, top+3):
    #         key = "".join(plants[k] for k in range(j-2, j+3))
    #         assert len(key) == 5
    #         new[j] = stuff[key]
    #     plants = new
    #     real = tuple(k for k, v in plants.items() if v == '#')
    #     print(i, len(real), real, sum(real))
    #     if real in seen:
    #         break
    #     seen[real] = i

    # print(i, seen[real])

# #    print([k for k, v in stuff.items() if v == '#'])
#     print(sum(k for k, v in plants.items() if v == '#'))

    # print(initial)
    # print(stuff)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

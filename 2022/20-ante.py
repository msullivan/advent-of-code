#!/usr/bin/env python3

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Optional, Any

Dir = int
LEFT, RIGHT = 0, 1

def node_height(nobe: Optional[Node]) -> int:
    return nobe.height if nobe else 0
def node_size(nobe: Optional[Node]) -> int:
    return nobe.size if nobe else 0

@dataclass(slots=True)
class Node:
    _parent: Optional[Node] = None
    pdir: Dir = -1
    height: int = 1
    size: int = 1
    children: list[Optional[Node]] = field(default_factory=lambda: [None, None])

    payload: Any = None

    @property
    def is_dummy(self) -> bool:
        return self._parent is None
    @property
    def parent(self) -> Node:
        assert self._parent
        return self._parent
    @parent.setter
    def parent(self, new: Node) -> None:
        self._parent = new

    @property
    def left(self) -> Optional[Node]:
        return self.children[LEFT]
    @property
    def right(self) -> Optional[Node]:
        return self.children[RIGHT]

    def set_child(self, dir: Dir, child: Optional[Node]) -> None:
        # assert child is not self
        self.children[dir] = child
        if child:
            child.parent = self
            child.pdir = dir
        # assert self.left is not self.right
        # self.update()

    def update(self) -> None:
        self.height = max(node_height(self.left), node_height(self.right)) + 1
        self.size = node_size(self.left) + node_size(self.right) + 1


def flip_dir(dir: Dir) -> Dir:
    return 1 - dir


def rotate(node: Node, dir: Dir) -> Node:
    odir = flip_dir(dir)
    replacement = node.children[odir]
    assert replacement
    node.set_child(odir, replacement.children[dir])
    node.update()
    replacement.set_child(dir, node)
    replacement.update()
    return replacement


def lookup(tree: Node, idx: int) -> Node:
    node: Optional[Node] = tree.right

    while node:
        ls = node_size(node.left)
        if ls == idx:
            return node
        elif ls > idx:
            node = node.left
        else:
            idx = idx - ls - 1
            node = node.right

    raise LookupError


def node_repair(node: Node) -> None:
    node.update()
    bal = node_height(node.left) - node_height(node.right)
    if abs(bal) <= 1:
        return

    pdir = node.pdir
    parent = node.parent

    dir = LEFT if bal >= 1 else RIGHT
    odir = flip_dir(dir)
    subtree = node.children[dir]
    assert subtree

    if node_height(subtree.children[odir]) + 1 == subtree.height:
        node.set_child(dir, rotate(subtree, dir))
    parent.set_child(pdir, rotate(node, odir))


def chain_repair(node: Node) -> None:
    while not node.is_dummy:
        parent = node.parent
        node_repair(node)
        node = parent


def insert_after(existing: Node, new: Node) -> None:
    new.children[0] = new.children[1] = None

    if existing.right is None:
        existing.set_child(RIGHT, new)
        chain_repair(new)
        return

    existing = existing.right

    while existing.left is not None:
        existing = existing.left
    existing.set_child(LEFT, new)
    chain_repair(new)


def traverse(tree: Node) -> list[Any]:
    out = []

    def go(node: Optional[Node]) -> None:
        if node:
            go(node.left)
            out.append(node.payload)
            go(node.right)

    go(tree.right)
    return out


def node_end(node: Node, dir: Dir) -> Node:
    while (nobe := node.children[dir]):
        node = nobe
    return node


def node_step(node: Node, dir: Dir) -> Optional[Node]:
    odir = flip_dir(dir)
    if (child := node.children[dir]):
        return node_end(child, odir)
    # Climb up...
    while True:
        if node.parent.is_dummy:
            return None
        if dir != node.pdir:
            return node.parent
        node = node.parent


def swap_nodes(node1: Node, node2: Node) -> None:
    # ugh need to swap in place
    tl, tr, tp, tpd = node1.left, node1.right, node1.parent, node1.pdir
    node1.set_child(LEFT, node2.left)
    node1.set_child(RIGHT, node2.right)
    node2.set_child(LEFT, tl)
    node2.set_child(RIGHT, tr)

    # Need to update the parents also
    node2.parent.set_child(node2.pdir, node1)
    tp.set_child(tpd, node2)


def delete(node: Node) -> None:
    while True:
        if not node.left:
            replacement = node.right
            break
        elif not node.right:
            replacement = node.left
            break
        else:
            r = node_step(node, RIGHT)
            assert r
            swap_nodes(node, r)

    parent = node.parent
    node.parent.set_child(node.pdir, replacement)
    chain_repair(parent)

    node.parent = None  # type: ignore


def get_index(node: Node) -> int:
    idx = node_size(node.left)

    while not (parent := node.parent).is_dummy:
        pdir = node.pdir
        if pdir == RIGHT:
            idx += node_size(parent.left) + 1
        node = parent
    return idx

K = 811589153


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    odata = [int(s.rstrip('\n')) for s in file]
    data = []
    for k in range(200):
        data.extend([i*K + k for i in odata])
    idx0 = data.index(0)

    import time

    tree = Node()
    t0 = time.time()
    nobes = [Node(payload=i) for i in data]
    t1 = time.time()
    print(f'{t1-t0:.3f}')

    N = len(data)

    last = tree
    for nobe in nobes:
        insert_after(last, nobe)
        last = nobe
    t2 = time.time()
    print(f'{t2-t1:.3f}')

    for _ in range(1):
        for j, nobe in enumerate(nobes):
            if j % 100 == 0:
                print(j)
            idx = get_index(nobe)
            # -1 because we always insert *after*
            nidx = (idx + nobe.payload - 1) % (N-1)

            delete(nobe)
            after = lookup(tree, nidx)
            insert_after(after, nobe)

    nidx0 = get_index(nobes[idx0])
    print(sum(lookup(tree, (nidx0+k)%N).payload for k in (1000, 2000, 3000)))


if __name__ == '__main__':
    main(sys.argv)

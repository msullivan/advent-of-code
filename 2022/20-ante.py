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

@dataclass
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
        self.children[dir] = child
        if child:
            child.parent = self
            child.pdir = dir
        self.update()

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
    replacement.set_child(dir, node)
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
    if existing.right is None:
        existing.set_child(RIGHT, new)
        chain_repair(new)
        return

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


def get_index(node: Node) -> int:
    idx = node_size(node.left)

    while not (parent := node.parent).is_dummy:
        pdir = node.pdir
        if pdir == RIGHT:
            idx += node_size(parent.left) + 1
        node = parent
    return idx


def main(args):
    # file = open(args[1]) if len(args) > 1 else sys.stdin
    # # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # # data = [int(s.rstrip('\n')) for s in file]
    # data = [s.rstrip('\n') for s in file]

    tree = Node()
    nobes = []

    last = tree
    for i in range(10):
        nobe = Node(payload=str(i))
        nobes.append(nobe)
        insert_after(last, nobe)
        last = nobe
        print(traverse(tree))

    for nobe in nobes:
        print(get_index(nobe))


    delete(nobes[5])
    print(traverse(tree))


if __name__ == '__main__':
    main(sys.argv)

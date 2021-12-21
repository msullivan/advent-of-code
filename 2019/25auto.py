#!/usr/bin/env python3

import os
import copy
import sys
import time
from collections import defaultdict, deque
from intcode import IntCode
import re
import pickle
from itertools import chain, combinations

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

DIRS = ['north', 'south', 'east', 'west']
def flip(s):
    return DIRS[DIRS.index(s) ^ 1]


def room_name(msg):
    lines = msg.split("\n")
    return [s for s in lines if s.startswith('==')][0].replace('==', '').strip()

def run(interp, s, max=None):
    l = interp.run([ord(x) for x in s+"\n"], max)
    return "".join([chr(x) for x in l])


def explore(interp, map, room, msg):
    print("***", room)
    print(msg)
    lines = msg.split("\n")
    # this is a super hokey parsing.
    stuff = [s.replace('- ', '') for s in lines if s.startswith('- ')]
    dirs = [x for x in stuff if x in DIRS]
    items = [x for x in stuff if x not in DIRS]
    # print(dirs)

    for dir in dirs:
        if dir in map[room]:
            continue
        print(dir)
        out = run(interp, dir)

        # doing this in unnecessary generality. IRL it is a tree, right?
        newroom = room_name(out)
        existed = newroom in map
        map[room][dir] = newroom
        map[newroom][flip(dir)] = room
        if existed:
            print("===== SKIPPING", newroom, "FROM", room)
        if not existed:
            explore(interp, map, newroom, out)

        # go back
        out = run(interp, flip(dir))
        print(out)

    for item in items:
        s = "take " + item
        print(s)
        backup = copy.deepcopy(interp)

        out = '<TIMED OUT>'
        try:
            out = run(backup, s, 10000)
            assert not backup.done
            assert 'Items in your inventory' in run(backup, 'inv')
        except (ValueError, AssertionError):
            print(out)
            print("ROLLING BACK")
            continue
        run(interp, s)


def pathfind(cur, target, map, seen):
    seen.add(cur)
    if cur == target:
        return ()

    for dir, nbr in map[cur].items():
        if nbr not in seen:
            if (path := pathfind(nbr, target, map, seen)) is not None:
                return (dir,) + path

    return None


def main(args):
    data = [s.strip() for s in open("25.input")]
    p = [int(x) for x in data[0].split(",")]

    interp = IntCode(p)

    # game
    map = defaultdict(dict)
    out = run(interp, "")
    start_room = room_name(out)
    explore(interp, map, start_room, out)

    inv = run(interp, "inv")
    inv = [s.replace('- ', '') for s in inv.split("\n") if s.startswith('- ')]

    print(inv)
    print(map)

    path = pathfind(start_room, "Security Checkpoint", map, set())
    print(path)
    for step in path:
        print(step)
        print(run(interp, step))

    for drop in powerset(inv):
        go = copy.deepcopy(interp)
        cmd = "".join(["drop {}\n".format(x) for x in drop]) + "west"
        out_msg = run(go, cmd)
        print(out_msg)
        if "Alert!" not in out_msg:
            break
    else:
        assert False

    print(extract(out_msg)[0])


if __name__ == '__main__':
    sys.exit(main(sys.argv))

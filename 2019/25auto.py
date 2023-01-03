#!/usr/bin/env python3

import os
import copy
import sys
import time
from collections import defaultdict, deque
from intcode import IntCode
import re
from itertools import permutations

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

DIRS = ['north', 'south', 'east', 'west']
def flip(s):
    return DIRS[DIRS.index(s) ^ 1]


def room_name(msg):
    lines = msg.split("\n")
    return [s for s in lines if s.startswith('==')][0].replace('==', '').strip()

def run(interp, s, max=None):
    l = interp.run([ord(x) for x in s+"\n"], max)
    return "".join([chr(x) for x in l])


def explore(interp, map, item_rooms, room, msg):
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

        if 'Alert!' in out:
            continue

        if not existed:
            explore(interp, map, item_rooms, newroom, out)

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
        # XXX: Is this better?
        # interp.ip, interp.relative_base, interp.program = (
        #     backup.ip, backup.relative_base, backup.program)
        run(interp, s)
        item_rooms[item] = room


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
    data = [s.strip() for s in sys.stdin]
    p = [int(x) for x in data[0].split(",")]

    interp = IntCode(p)

    # game
    map = defaultdict(dict)
    item_rooms = {}
    out = run(interp, "")
    start_room = room_name(out)
    explore(interp, map, item_rooms, start_room, out)

    # ... we get a faster ordering with inv...!
    inv = run(interp, "inv")
    inv = [s.replace('- ', '') for s in inv.split("\n") if s.startswith('- ')]
    # inv = list(item_rooms.keys())

    print(inv)
    print(map)

    path = pathfind(start_room, "Security Checkpoint", map, set())
    print(path)
    for step in path:
        print(step)
        print(run(interp, step))

    checkpoint_dir = [
        k for k, v in map["Security Checkpoint"].items()
        if v == "Pressure-Sensitive Floor"
    ][0]

    cnt = 0
    last = set(inv)
    for bin in range(1 << len(inv)):
        grey = bin ^ (bin >> 1)
        cur = {inv[i] for i in range(len(inv)) if grey & (1 << i)}
        # cur = set(cur)
        cnt += 1

        cmds = []
        cmds.extend(f'drop {x}' for x in last - cur)
        cmds.extend(f'take {x}' for x in cur - last)
        cmds.append(checkpoint_dir)
        cmd = '\n'.join(cmds)

        print(cmd)
        out_msg = run(interp, cmd)
        print(out_msg)
        if "Alert!" not in out_msg:
            break

        last = cur
    else:
        assert False

    print("final items", sorted(cur))
    print(f"tried {cnt} sets")
    print(extract(out_msg)[0])


if __name__ == '__main__':
    sys.exit(main(sys.argv))

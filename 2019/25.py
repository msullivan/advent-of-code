#!/usr/bin/env python3

# I solved this with programming but like not *correct* programming?
# It works for the input I gave and was developed while looking at the map.

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

crap = [
    "klein bottle",
    "loom",
    "mutex",
    "pointer",
    "polygon",
    "hypercube",
    "mug",
    "manifold",
]

def main(args):
    data = [s.strip() for s in open("25.input")]
    p = [int(x) for x in data[0].split(",")]

    interp = IntCode(p)

    if args[1:]:
        with open(os.path.join("saves", args[1]), "rb") as f:
            interp = pickle.load(f)

    if args[2:] == ["-h"]:
        for drop in powerset(crap):
            go = copy.deepcopy(interp)
            cmd = "".join(["drop {}\n".format(x) for x in drop]) + "west\n"
            out = go.run([ord(x) for x in cmd+"\n"])
            out_msg = "".join([chr(x) for x in out])
            print(out_msg)
            if "Alert!" not in out_msg:
                break
        else:
            assert False
        print("Dropped", drop)
        interp = go


    # game
    out = interp.run([])
    print("".join([chr(x) for x in out]))
    i = 0
    while True:
        inp = input()
        backup = copy.deepcopy(interp)
        with open(os.path.join("saves", str(i)), "wb") as f:
            pickle.dump(backup, f)
        out = interp.run([ord(x) for x in inp+"\n"])
        print("".join([chr(x) for x in out]))
        if interp.done:
            print("RESTORING")
            interp = backup
        i += 1


#    board = defaultdict(lambda: " ")




if __name__ == '__main__':
    sys.exit(main(sys.argv))

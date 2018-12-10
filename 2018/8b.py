#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
from dataclasses import dataclass

@dataclass
class Nobe:
    children: object
    metadata: object

argh = 0

def parse(data):
    global argh
    children = data.popleft()
    metadata = data.popleft()
    nobe = Nobe([], [])
    for x in range(children):
        nobe.children.append(parse(data))
    for x in range(metadata):
        y = data.popleft()
        nobe.metadata.append(y)
        argh += y

    return nobe

def eval(nobe):
    if not nobe.children:
        return sum(nobe.metadata)

    children_values = [eval(x) for x in nobe.children]
    z = 0
    for x in nobe.metadata:
        if x != 0 and x - 1 < len(children_values):
            #z += children_values[x - 1]
            z += eval(nobe.children[x - 1])
    return z

def main(args):
    data = [s.strip() for s in sys.stdin][0]
    data = deque([int(x) for x in data.split(' ')])

    print(eval(parse(data)))

if __name__ == '__main__':
    sys.exit(main(sys.argv))

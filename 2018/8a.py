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
    print(children, metadata)
    nobe = Nobe([], [])
    for x in range(children):
        nobe.children.append(parse(data))
    for x in range(metadata):
        argh += data.popleft()

def main(args):
    data = [s.strip() for s in sys.stdin][0]
    data = deque([int(x) for x in data.split(' ')])

    print(data)
    print(len(data))
    parse(data)
    print(argh)



if __name__ == '__main__':
    sys.exit(main(sys.argv))

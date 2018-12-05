#!/usr/bin/env python3

from collections import defaultdict
import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

def main(args):
    data = list([s.strip() for s in sys.stdin][0])
    print(data)

    changed = True
    while changed:
        changed = False
        new = []
        i = 0
        while i < len(data):
            if i + 1 < len(data) and data[i] != data[i+1] and data[i].upper() == data[i+1].upper():
                changed = True
                i += 2
            else:
                new.append(data[i])
                i += 1
        data = new

    print(len(data))

if __name__ == '__main__':
    sys.exit(main(sys.argv))

#!/usr/bin/env python3

import sys
from parse import parse
import re


def extract(s, pos=False):
    p = '' if pos else '-?'
    return [int(x) for x in re.findall(fr'{p}\d+', s)]

def main(args):
    data = [s.strip() for s in sys.stdin]

    x, y = 0, 0
    aim = 0
    for line in data:
        cmd, num = parse('{} {:d}', line)
        if cmd == 'forward':
            x += num
            y += aim*num
        elif cmd == 'down':
            aim += num
        else:
            aim -= num

    print(x*y)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

#!/usr/bin/env python3

from collections import defaultdict, deque
import sys
import re
#from dataclasses import dataclass

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

def draw(m):
    xs, ys = zip(*m.keys())
    for y in range(0, max(ys)):
        s = ''.join(m[x,y] for x in range(min(xs), max(xs)+1))
        print(s)

    print(min(xs), max(xs), min(ys), max(ys))

def main(args):
    m = defaultdict(lambda: ' ')
    data = [(s[0], extract(s.strip())) for s in sys.stdin]
    munged = []
    for (dir, (a, b, c)) in data:
        if dir == 'x':
            for y in range(b, c+1):
                m[a,y] = '#'
        else:
            for x in range(b, c+1):
                m[x,a] = '#'


    draw(m)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

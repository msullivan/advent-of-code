#!/usr/bin/env python3

from collections import defaultdict, deque
import sys
import re
import time
#from dataclasses import dataclass

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

def trace(m):
    xs, ys = zip(*m.keys())
    minx = min(xs)
    maxx = max(xs)
    t0 = time.time()
    maxy = max(y for (x, y), v in m.items() if v in "|~")
    t1 = time.time()
    lurr = "\n\n\n"
    for y in range(maxy-70, maxy+10):
        s = ''.join(m[x,y] for x in range(minx, maxx+1))
        lurr += "{:4} {}\n".format(y, s)
    t2 = time.time()

    print(lurr)
    print("{:.3} {:.3}".format(t1 - t0, t2 - t1))

def draw(m):
    xs, ys = zip(*m.keys())
    minx = min(xs)
    maxx = max(xs)
    for y in range(0, max(ys)+1):
        s = ''.join(m[x,y] for x in range(minx, maxx+1))
        print("{:4}".format(y), s)
        #print(s.replace(" ", "."))

    print(min(xs), max(xs), min(ys), max(ys))

def find_edge(m, x, y, dx):
    pipe_seen = False
    while True:
        if m[x+dx,y] == '|':
            pipe_seen = True
        if m[x,y+1] in ' |':
            if pipe_seen:
                return x-dx, False
            return x, False
        if m[x+dx,y] == '#':
            return x, True
        x += dx

def step(m, flowing, ymax):
    for x, y in list(flowing):
        if m[x,y] != '|':
            flowing.discard((x,y))

        if y+1 <= ymax and m[x,y+1] == ' ':
            i = 1
            while y+i <= ymax and m[x,y+i] == ' ':
                m[x,y+i] = '|'
                flowing.add((x,y+i))
                i += 1

            flowing.discard((x,y))  # XXX
        elif m[x,y+1] in '#~':
            lx, ledge = find_edge(m, x, y, -1)
            rx, redge = find_edge(m, x, y, +1)
            state = '~' if ledge and redge else '|'
            for i in range(lx, rx+1):
                if state == '|' and m[i,y] != state:
                    flowing.add((i,y))
                else:
                    flowing.discard((i,y))
                    if m[(i,y-1)] == '|' and m[i,y] != state:
                        flowing.add((i,y-1))  # XXX
                m[i,y] = state



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
    xs, ys = zip(*m.keys())
    ymin = min(ys)
    ymax = max(ys)

    m[500,0] = '+'
    m[500,1] = '|'


    flowing = {k for k in m if m[k] == '|'}

    i = 0
    while True:
        m2 = dict(m)
        # if i % 100 == 0:
        #     draw(m)
        #trace(m)
        step(m, flowing, ymax)

        #print(i, len(m), len(flowing))

        if m == m2:
            # The flowing tracking is "approximate", so when we stop,
            # find all the flowing squares and try again before
            # calling it a day.
            flowing = {k for k in m if m[k] == '|'}
            step(m, flowing, ymax)
            if m == m2:
                break
        i += 1

    draw(m)

    # I wasted a huge amount of time on the 2 extra dropping waters out of scan range
    count = sum(v in "~|" for (x, y), v in m.items() if ymin <= y <= ymax)
    print(count)
    rest = sum(v in "~" for (x, y), v in m.items() if ymin <= y <= ymax)
    print(rest)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

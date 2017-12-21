#!/usr/bin/env python3

import sys
from collections import defaultdict
def flip(s): return "|" if s == "-" else "-"

def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]

def dchunks(l, n):
#    print(l)
#    return list(chunks(list(list(chunks(x, n)) for x in l), n))
    s = len(l)//n
    grid = [[None]*s for i in range(s)]
#    print(s, grid)
    for i in range(s):
        for j in range(s):
            part = [[None]*n for i in range(n)]
            for x in range(n):
                for y in range(n):
#                    print(part, i, j, x, y)
                    part[x][y] = l[i*n + x][j*n + y]
            grid[i][j] = part
    return grid

def unchunks(l, n):
#    print(l)
#    return list(chunks(list(list(chunks(x, n)) for x in l), n))
    s = len(l)*n
    grid = [[None]*s for i in range(s)]
#    print(s, grid)
    for i in range(len(l)):
        for j in range(len(l)):
            part = l[i][j]
            for x in range(n):
                for y in range(n):
                    grid[i*n + x][j*n + y] = part[x][y]
#                    print(part, i, j, x, y)
    return grid


def rotate(l):
    outs = ["" for x in l]
    for i in range(len(l)):
        for j in range(len(l)):
            outs[j] = l[i][j] + outs[j]
    return tuple([tuple(x) for x in outs])

def xflip(l):
    return [tuple(reversed(x)) for x in l]
def yflip(l):
    return list(reversed(l))

def rotations(i):
    for j in range(4):
        i = rotate(i)
        yield i
        yield xflip(i)
        yield yflip(i)

def match(rules, square):
#    print("asdf:\n" + "\n".join((square)) + "\n")
#    print("asdf:" + str(square))
    for s in rotations(square):
#        print(s)
        if tuple(s) in rules:
            return rules[tuple(s)]

def flatten(l): return sum(map(tuple, l), ())

def step(rules, grid):
    if len(grid) % 2 == 0:
        n = 2
    else:
        n = 3
    cgrid = dchunks(grid, n)
#    print(cgrid)
#    print(cgrid[0])
#    print(cgrid[0][0])
    for i in range(len(cgrid)):
        for j in range(len(cgrid)):
            cgrid[i][j] = match(rules, cgrid[i][j])

    return unchunks(cgrid, n+1)

def main(args):
    srules = [s.strip() for s in sys.stdin]

    rules = {}
    for s in srules:
        l,r = s.split(" => ")
        ls = l.split("/")
        rs = r.split("/")
        rules[tuple(map(tuple, ls))] = tuple(map(tuple, rs))

    print(rules)
    grid = list(map(tuple, [".#.", "..#", "###"]))


    for i in range(18):
        print(i)
        grid = step(rules, grid)
#        print("stepped: ", grid)
        x = flatten(list(map(list, grid)))
        n = len([c for c in x if c =='#'])
        print("COUNT: ", n)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

#!/usr/bin/env python3

import sys
import math
import ast
import copy


def idx(p, path):
    for i in path:
        p = p[i]
    return p


def write_idx(p, path, x):
    for i in path[:-1]:
        p = p[i]
    p[path[-1]] = x


def left(path, p):
    while path and path[-1] == 0:
        path = path[:-1]
    if not path:
        return None
    path = path[:-1]
    path += (0,)
    while isinstance(idx(p, path), list):
        path += (1,)
    return path


def right(path, p):
    while path and path[-1] == 1:
        path = path[:-1]
    if not path:
        return None
    path = path[:-1]
    path += (1,)
    while isinstance(idx(p, path), list):
        path += (0,)
    return path


def explode(top, p, n, path):
    if isinstance(p, list) and n == 4:
        l = left(path + (0,), top)
        r = right(path + (1,) , top)
        x, y = p
        if l:
            write_idx(top, l, idx(top, l) + x)
        if r:
            # print("RP", path + (1,), r)
            # print("R", r, idx(top, r), y, idx(top, r) + y)
            write_idx(top, r, idx(top, r) + y)

        write_idx(top, path, 0)

        return True

    if isinstance(p, list):
        for i in range(2):
            if explode(top, p[i], n+1, path + (i,)):
                return True

    return False

def split(top, p, path):
    if isinstance(p, int) and p >= 10:
        l = p // 2
        r = int(math.ceil(p / 2))
        write_idx(top, path, [l, r])
        return True

    if isinstance(p, list):
        for i in range(2):
            if split(top, p[i], path + (i,)):
                return True

    return False

def reduce(n):
    n = copy.deepcopy(n)
    while True:
        if explode(n, n, 0, ()):
            continue
        if split(n, n, ()):
            continue
        break
    return n

def magnitude(p):
    if isinstance(p, list):
        return 3*magnitude(p[0]) + 2*magnitude(p[1])
    return p


def main(args):
    data = [ast.literal_eval(s.strip()) for s in sys.stdin]


    n = data[0]
    for m in data[1:]:
        n = reduce([n, m])

    print(magnitude(n))

    m = 0
    for i in range(len(data)):
        for j in range(len(data)):
            if i == j:
                continue
            n = [data[i], data[j]]
            n = reduce(n)
            m = max(magnitude(n), m)

    print(m)


if __name__ == '__main__':
    main(sys.argv)

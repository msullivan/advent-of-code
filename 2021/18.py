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


def move(path, p, dir):
    odir = 1 - dir
    while path and path[-1] == dir:
        path = path[:-1]
    if not path:
        return None
    path = path[:-1]
    path += (dir,)
    while isinstance(idx(p, path), list):
        path += (odir,)
    return path


def explode(top, p, n, path):
    if isinstance(p, list) and n == 4:
        l = move(path, top, 0)
        r = move(path, top, 1)
        x, y = p
        if l:
            write_idx(top, l, idx(top, l) + x)
        if r:
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
            n = reduce([data[i], data[j]])
            m = max(magnitude(n), m)

    print(m)


if __name__ == '__main__':
    main(sys.argv)

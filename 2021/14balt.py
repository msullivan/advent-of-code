#!/usr/bin/env python3

"""
Find characters deep in the expanded string, for fun.

"""

import sys

from collections import Counter


def real_step(s, rules):
    out = ""
    for i in range(len(s)):
        out += s[i]
        k = s[i:i+2]
        if k in rules:
            out += rules[k]
    return out


def step(cnt, rules):
    ncnt = Counter()
    for k, v in cnt.items():
        if k in rules:
            c = rules[k]
            ncnt[k[0] + c] += v
            ncnt[c + k[1]] += v
        else:
            ncnt[k] += v
    return ncnt


def size(s, n, rules):
    cnt = Counter(s[i:i+2] for i in range(len(s)-1))
    for _ in range(n):
        cnt = step(cnt, rules)

    lcnt = Counter(s[0])
    for k, v in cnt.items():
        lcnt[k[1]] += v
    return sum(lcnt.values())


def get_char(s, idx, iters, rules):
    for i in range(iters):
        h = len(s) // 2
        first = s[:h+1]
        sz = size(first, iters - i, rules)
        if idx < sz:
            s = real_step(first, rules)
        else:
            s = real_step(s[h:], rules)
            idx -= sz - 1

    return s[idx]


def main(args):
    data = [s.strip() for s in sys.stdin]
    s = data[0]
    rules = dict(x.split(" -> ") for x in data[2:])

    # Make sure it works
    t = s
    for i in range(4):
        t = real_step(t, rules)

    for idx in range(len(t)):
        c = get_char(s, idx, 4, rules)
        assert t[idx] == c

    # find some random characters deep into it
    print(size(s, 40, rules))
    start = 7311752324710
    out = ""
    for i in range(10):
        out += get_char(s, start + i, 40, rules)
    print(out)


if __name__ == '__main__':
    main(sys.argv)

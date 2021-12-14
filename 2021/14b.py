#!/usr/bin/env python3

import sys

from collections import Counter


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


def main(args):
    data = [s.strip() for s in sys.stdin]
    s = data[0]
    rules = dict(x.split(" -> ") for x in data[2:])

    cnt = Counter(s[i:i+2] for i in range(len(s)-1))
    for _ in range(40):
        cnt = step(cnt, rules)

    lcnt = Counter(s[0])
    for k, v in cnt.items():
        lcnt[k[1]] += v

    print(max(lcnt.values()) - min(lcnt.values()))


if __name__ == '__main__':
    main(sys.argv)

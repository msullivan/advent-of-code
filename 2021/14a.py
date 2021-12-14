#!/usr/bin/env python3

import sys

from collections import Counter

def step(s, rules):
    out = ""
    for i in range(len(s)):
        out += s[i]
        k = s[i:i+2]
        if k in rules:
            out += rules[k]
    return out

def main(args):
    data = [s.strip() for s in sys.stdin]
    target = data[0]
    rules = [x.split(" -> ") for x in data[2:]]
    rules = {k: v for k, v in rules}

    s = target
    for _ in range(10):
        s = step(s, rules)

    cnt = Counter(s)
    print(max(cnt.values()) - min(cnt.values()))



if __name__ == '__main__':
    main(sys.argv)

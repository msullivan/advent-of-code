#!/usr/bin/env python3

import sys
import re
import time
from typing import Set


def extract(s):
    return [int(x) for x in re.findall(r'\d+', s)]



def main(args):
    data = [tuple(s.strip().split(")")) for s in sys.stdin]
    m = {k: v for v, k in data}
    s = set(m.items())
    for k in list(m.keys()):
        p = k
        while p in m:
            s.add((k, p))
            p = m[p]

    print(len(s) - 1)

    cnt = 0
    p = m["YOU"]
    while True:
        if ("SAN", p) in s:
            break
        p = m[p]
        cnt += 1
    pp = p
    p = m["SAN"]
    while p != pp:
        p = m[p]
        cnt += 1

    print(cnt)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

#!/usr/bin/env python3

# This version runs in like 8 seconds when compiled with mypyc, while
# the regular version would run in 30 seconds under mypyc. (And 90s
# under cpython).
# It also runs in like 4s in pypy vs. 30s for the regular version.
# This version is actually like 20s slower in cpython!

import sys
from typing import List, Optional

def upper(c: int) -> int:
    return c - 0x20 if 0x61 <= c <= 0x7a else c

def doit(data: List[int]) -> int:
    changed = True
    while changed:
        changed = False
        new = []
        i = 0
        while i < len(data):
            if i + 1 < len(data) and data[i] != data[i+1] and upper(data[i]) == upper(data[i+1]):
                changed = True
                i += 2
            else:
                new.append(data[i])
                i += 1
        data = new

    return (len(data))

def main() -> None:
    data = [s.strip() for s in sys.stdin][0]

    lol = []
    for i in range(26):
        c = chr(ord('a') + i)
        n = list(data.replace(c, '').replace(c.upper(), ''))
        a = doit([ord(x) for x in n])
        # This print got me on the leaderboard early: about 60% of the way
        # through, one of the results was like 40% lower than the rest,
        # so I submitted it before the program finished and it was right.
        print(a)
        lol.append(a)
    print(min(lol))

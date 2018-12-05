#!/usr/bin/env python3

from collections import defaultdict
import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

def doit(data):
    changed = True
    while changed:
        changed = False
        new = []
        i = 0
        while i < len(data):
            if i + 1 < len(data) and data[i] != data[i+1] and data[i].upper() == data[i+1].upper():
                changed = True
                i += 2
            else:
                new.append(data[i])
                i += 1
        data = new

    return (len(data))

def main(data):
    data = [s.strip() for s in sys.stdin][0]

    lol = []
    for i in range(26):
        c = chr(ord('a') + i)
        n = list(data.replace(c, '').replace(c.upper(), ''))
        a = doit(n)
        # This print got me on the leaderboard early: about 60% of the way
        # through, one of the results was like 40% lower than the rest,
        # so I submitted it before the program finished and it was right.
        print(a)
        lol.append(a)
    print(min(lol))


if __name__ == '__main__':
    sys.exit(main(sys.argv))

#!/usr/bin/env python3

import sys
from collections import Counter
FUCK = 0

def thing(s):
    global FUCK
    thing, cksum = s.split("[")
    cksum = cksum.replace("]", "")
    stuff, sector = thing.rsplit("-", 1)
    stuff = stuff.replace("-", "")
    nus = Counter()
    for c in stuff:
        nus[c] += 1

    def key(x): return (-nus[x], x)
    things = list(nus.keys())
    thingss = list(sorted(things, key=key))

    s = "".join(thingss[0:5])
    print(s, cksum)
    if s == cksum[0:5]: FUCK += int(sector)

    print(nus)


    print(stuff, sector)

def main(args):
    names = [s.strip() for s in sys.stdin]
    for x in names:
        thing(x)

    print(FUCK)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

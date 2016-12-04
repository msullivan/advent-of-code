#!/usr/bin/env python3

# I wasn't sure what

import sys
from collections import Counter
FUCK = 0

def add(c, n):
    if c == "-": return " "
    i = ord(c) - ord('a')
    i = (i + n) % 26
    return chr(i + ord('a'))

def thing(s):
    global FUCK
    thing, cksum = s.split("[")
    cksum = cksum.replace("]", "")
    stuff, sector = thing.rsplit("-", 1)
    butt = stuff
    stuff = stuff.replace("-", "")
    nus = Counter()
    for c in stuff:
        nus[c] += 1

    def key(x): return (-nus[x], x)
    things = list(nus.keys())
    thingss = list(sorted(things, key=key))

    s = "".join(thingss[0:5])
    if s == cksum[0:5]: FUCK += int(sector)
    else: return

    s = "".join(add(c, int(sector)) for c in butt)
    print(s, sector)

def main(args):
    names = [s.strip() for s in sys.stdin]
    for x in names:
        thing(x)

    print(FUCK)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

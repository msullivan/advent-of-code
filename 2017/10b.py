#!/usr/bin/env python3

import sys

def hash(lens):
    l = list(range(256))
    cur = 0
    skip = 0

    for i in range(64):
        for ln in lens:
            lurr = l+l
            sub = list(reversed(lurr[cur:cur+ln]))
            for i in range(ln):
                l[(cur+i)%len(l)] = sub[i]
            cur = (cur + ln + skip) % len(l)
            skip += 1

    return l

def main(args):
    data = [s.strip() for s in sys.stdin]
    lens = list(map(ord, data[0]))+[17, 31, 73, 47, 23]

    h = hash(lens)
    sparse = []
    for i in range(16):
        x = 0
        for j in range(16):
            x ^= h[i*16+j]
        sparse += [x]

    print("".join("%02x" % x for x in sparse))

if __name__ == '__main__':
    sys.exit(main(sys.argv))

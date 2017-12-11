#!/usr/bin/env python3

import sys

def main(args):
    data = [s.strip() for s in sys.stdin]
    lens = map(int, data[0].split(","))

    l = list(range(256))
    cur = 0
    skip = 0

    for ln in lens:
        lurr = l+l
        sub = list(reversed(lurr[cur:cur+ln]))
        for i in range(ln):
            l[(cur+i)%len(l)] = sub[i]
        cur = (cur + ln + skip) % len(l)
        skip += 1

    print(l[0]*l[1])


if __name__ == '__main__':
    sys.exit(main(sys.argv))

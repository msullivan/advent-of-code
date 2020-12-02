#!/usr/bin/env python3

import sys

def main(args):
    data = [s.strip() for s in sys.stdin]
    data = [x.split(" ") for x in data]
    data = [(x.split('-'), y[0], z) for x,y,z in data]

    cnt = 0
    for (lo, hi), l, s in data:
        x = 0
        if s[int(lo)-1] == l: x += 1
        if s[int(hi)-1] == l: x += 1
        if x == 1:
            cnt += 1

    print(cnt)




if __name__ == '__main__':
    sys.exit(main(sys.argv))

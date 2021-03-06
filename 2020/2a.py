#!/usr/bin/env python3

import sys

def main(args):
    data = [s.strip() for s in sys.stdin]
    data = [x.split(" ") for x in data]
    data = [(x.split('-'), y[0], z) for x,y,z in data]

    cnt = 0
    for (lo, hi), l, s in data:
        n = s.count(l)
        if int(lo) <= n <= int(hi):
            cnt += 1

    print(cnt)




if __name__ == '__main__':
    sys.exit(main(sys.argv))

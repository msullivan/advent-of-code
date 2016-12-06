#!/usr/bin/env python3

import sys
from collections import Counter

def main(args):
    names = [s.strip() for s in sys.stdin]
    n = len(names[0])
    spots = [Counter() for x in range(n)]
    for name in names:
        for i in range(n):
            spots[i][name[i]] += 1

    print("".join(x.most_common()[-1][0] for x in spots))

if __name__ == '__main__':
    sys.exit(main(sys.argv))

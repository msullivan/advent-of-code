#!/usr/bin/env python3

import sys

def main(args):
    data = [int(s.strip()) for s in sys.stdin]

    cnt = 0
    last = data[0]
    for cur in data[1:]:
        if cur > last:
            cnt += 1
        last = cur

    print(cnt)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

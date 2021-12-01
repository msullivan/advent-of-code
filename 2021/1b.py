#!/usr/bin/env python3

import sys

def main(args):
    data = [int(s.strip()) for s in sys.stdin]

    cnt = 0
    last = sum(data[0:2])
    for i in range(1, len(data)):
        cur = sum(data[i:i+3])
        if cur > last:
            cnt += 1
        last = cur

    print(cnt)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

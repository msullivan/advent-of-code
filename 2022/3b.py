#!/usr/bin/env python3

import sys

def iord(c):
    return ord(c.lower()) - ord('a')

def main(args):
    data = [s.strip() for s in sys.stdin]

    cnt = 0
    for i in range(0, len(data), 3):
        parts = data[i:i+3]
        same = set(parts[0]) &  set(parts[1]) & set(parts[2])
        same = list(same)[0]
        if same.islower():
            val = 1 + iord(same)
        else:
            val = 27 + iord(same)

        cnt += val

    print(cnt)

if __name__ == '__main__':
    main(sys.argv)

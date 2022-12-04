#!/usr/bin/env python3

import sys

def iord(c):
    return ord(c.lower()) - ord('a')


def main(args):
    data = [s.strip() for s in sys.stdin]

    cnt = 0
    for line in data:
        mid = len(line)//2
        a, b = line[:mid], line[mid:]
        same = list(set(a) & set(b))[0]
        if same.islower():
            val = 1 + iord(same)
        else:
            val = 27 + iord(same)

        cnt += val

    print(cnt)

if __name__ == '__main__':
    main(sys.argv)

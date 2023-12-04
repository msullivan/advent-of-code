#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    copies = [1 for _ in data]
    tscore = 0
    tot = 0

    for i, line in enumerate(data):
        n, r = line.split(':')
        win, have = r.split('|')

        win = extract(win)
        have = extract(have)

        score = cnt = 0
        for n in have:
            if n in win:
                cnt += 1

                if score == 0:
                    score = 1
                else:
                    score *= 2


        for j in range(i + 1, i + 1 + cnt):
            copies[j] += copies[i]

        tscore += score
        tot += copies[i]

    print(tscore)
    print(tot)


if __name__ == '__main__':
    main(sys.argv)

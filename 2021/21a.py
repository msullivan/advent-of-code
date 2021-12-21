#!/usr/bin/env python3

import sys
import re
import math

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def main(args):
    data = [s.strip() for s in sys.stdin]
    p1 = extract(data[0])[1]
    p2 = extract(data[1])[1]

    die = 1
    nrolls = 0

    def roll():
        nonlocal die, nrolls
        nrolls += 1
        x = die
        die = (die + 1)
        if die == 101:
            die = 1
        return x

    s1 = s2 = 0
    while s1 < 1000 and s2 < 1000:
        print(p1)
        for _ in range(1):
            rolls = [roll(), roll(), roll()]
            print(rolls)
            move = sum(rolls)
            p1 = p1 + move
            while p1 > 10:
                p1 -= 10
            s1 += p1
        print(move, p1, s1)
        if s1 >= 1000:
            break
        for _ in range(1):
            move = roll() + roll() + roll()
            p2 = p2 + move
            while p2 > 10:
                p2 -= 10
            s2 += p2

    print(min(s1, s2), s1, s2, nrolls)
    print(min(s1, s2) * nrolls)

if __name__ == '__main__':
    main(sys.argv)

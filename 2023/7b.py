#!/usr/bin/env python3

import sys
from collections import Counter

ORDERS = reversed('AKQT98765432J')
ORDER = {v: k for k, v in enumerate(ORDERS)}

def characterize2(s):
    cnts = Counter(s)
    vals = sorted(cnts.values())
    if vals[-1] == 5:
        return 10
    elif vals[-1] == 4:
        return 9
    elif vals == [2, 3]:
        return 8
    elif vals == [1, 1, 3]:
        return 7
    elif vals == [1, 2, 2]:
        return 6
    elif vals == [1, 1, 1, 2]:
        return 5
    elif vals == [1, 1, 1, 2]:
        return 4
    else:
        return 3


def characterize(s):
    if 'J' not in s:
        return characterize2(s)

    m = -1
    for c in ORDER:
        if c == 'J': continue
        s2 = s.replace('J', c, 1)
        m = max(m, characterize(s2))
    return m


def key(s):
    return (characterize(s), tuple(ORDER[c] for c in s))


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    data = [x.split(' ') for x in data]
    data = [(s, int(x)) for s, x in data]

    data2 = sorted(data, key=lambda k: key(k[0]))

    sum = 0
    for i, (_, k) in enumerate(data2):
        sum += (i+1)*k
    print(sum)

if __name__ == '__main__':
    main(sys.argv)

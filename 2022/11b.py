#!/usr/bin/env python3

import sys
import re
from collections import deque

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def main(args):
    data = [x.rstrip('\n').split('\n') for x in sys.stdin.read().split('\n\n')]

    ms = []
    for ls in data:
        ml, items, op, test, true, false = ls
        op = op.split('= ')[1]
        ms.append((deque(extract(items)), op, extract(test)[0], extract(true)[0], extract(false)[0]))

    asdf = 1
    for m in ms:
        asdf *= m[2]

    maxbits = 0
    mcounts = [0 for _ in ms]
    for i in range(10000):
        # print(i)
        for j, monkey in enumerate(ms):
            # print('MONKEY', j)
            items, op, test, true, false = monkey
            while items:
                item = items.popleft()
                mcounts[j] += 1
                # XXX: DON'T DO THIS AT HOME!
                new = eval(op, None, dict(old=item))
                new2 = new % asdf
                if new2 % test == 0:
                    idx = true
                else:
                    idx = false
                # print(item, '->', new, '->', new2, 'goes to', idx)
                ms[idx][0].append(new2)

        # print("ROUND")
        # for m in ms:
        #     print(m[0])

    mcounts.sort()
    print(mcounts[-1]*mcounts[-2])


if __name__ == '__main__':
    main(sys.argv)

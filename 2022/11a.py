#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def main(args):
    data = [x.rstrip('\n').split('\n') for x in sys.stdin.read().split('\n\n')]

    ms = []
    for ls in data:
        ml, items, op, test, true, false = ls
        op = op.split('= ')[1]
        ms.append((extract(items), op, extract(test)[0], extract(true)[0], extract(false)[0]))

    mcounts = [0 for _ in ms]
    for i in range(20):
        for j, monkey in enumerate(ms):
            # print('MONKEY', j)
            items, op, test, true, false = monkey
            while items:
                item = items.pop(0)
                mcounts[j] += 1
                # print(item)
                op2 = op.replace('old', str(item))
                # print(op2)
                # XXX: DON'T DO THIS AT HOME!
                new = eval(op2)
                new2 = new // 3
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

#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
#from dataclasses import dataclass

def main(args):
    seen = deque(map(int, '598701'))
    num = 100000000
    things = [3, 7]
    n1 = 0
    n2 = 1
    d = deque(things[-6:])
    i = 2
    while True:
        new = list(map(int, str(things[n1] + things[n2])))
        for c in new:
            i += 1
            if len(d) == len(seen):
                d.popleft()
            d.append(c)
            if i % 10000 == 0:
                print(i, d, seen)
            if d == seen:
                print(i - len(seen))
                return
        things.extend(new)
        n1 = (n1 + 1 + things[n1]) % len(things)
        n2 = (n2 + 1 + things[n2]) % len(things)


    lol = ''.join(str(i) for i in things)
    print(lol.index(seen))

    print(''.join(str(i) for i in things[num:num+10]))




if __name__ == '__main__':
    sys.exit(main(sys.argv))

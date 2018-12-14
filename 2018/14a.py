#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
#from dataclasses import dataclass

def main(args):
    num = 598701
    things = [3, 7]
    n1 = 0
    n2 = 1
    while len(things) < num + 10:
        things += list(map(int, str(things[n1] + things[n2])))
        n1 = (n1 + 1 + things[n1]) % len(things)
        n2 = (n2 + 1 + things[n2]) % len(things)

    print(''.join(str(i) for i in things[num:num+10]))




if __name__ == '__main__':
    sys.exit(main(sys.argv))

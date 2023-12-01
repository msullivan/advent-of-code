#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque
from parse import parse
import re
import math


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    v = 0
    for line in data:
        s = ''.join(x for x in line if x.isdigit())
        print(s)
        num = int(s[0] + s[-1])
        print(line, num)
        v += num


    print(v)

if __name__ == '__main__':
    main(sys.argv)

#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque
from parse import parse
import re
import math


asdf = ['----', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]

    v = 0
    for line in data:
        first = None
        last = None
        for i in range(len(line)):
            if line[i].isdigit():
                last = int(line[i])
                if not first: first = last
            else:
                for j, k in enumerate(asdf):
                    if line[i:].startswith(k):
                        last = j
                        if not first: first = last
                        break

        num = int(first*10 + last)
        print(line, num)
        v += num


    print(v)

if __name__ == '__main__':
    main(sys.argv)

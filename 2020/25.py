#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

def xform(loop, subject):
    return pow(subject, loop, 20201227)

def main(args):
    data = [s.strip() for s in sys.stdin]

    d1 = int(data[0])
    d2 = int(data[1])

    for i in range(1000000000):
        if xform(i, 7) == d2:
            print(i)
            break
    else:
        print("fuck")

    p2 = i

    print(xform(p2, d1))



if __name__ == '__main__':
    sys.exit(main(sys.argv))

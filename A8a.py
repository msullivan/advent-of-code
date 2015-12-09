#!/usr/bin/env python3

import sys

def main(args):
    cmds = [s.strip() for s in sys.stdin]

    sum = 0
    for i in cmds:
        diff =  len(i) - len(eval(i))
        sum += diff
    print(sum)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

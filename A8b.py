#!/usr/bin/env python3

import sys

def main(args):
    cmds = [s.strip() for s in sys.stdin]

    sum = 0
    for i in cmds:
        a = i
        a = a.replace('\\', '\\\\')
        a = a.replace("\"", '\\"')
        a = '"' + a + '"'
        sum += len(a) - len(i)
    print(sum)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

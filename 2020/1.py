#!/usr/bin/env python3

import sys

def p1(data):
    for x in data:
        for y in data:
            if x + y == 2020:
                print(x*y)
                return


def p2(data):
    for x in data:
        for y in data:
            for z in data:
                if x + y +z == 2020:
                    print(x*y*z)
                    return


def main(args):
    data = [s.strip() for s in sys.stdin]
    data = [int(x) for x in data]
    p1(data)
    p2(data)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

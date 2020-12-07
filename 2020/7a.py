#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]


def search(bags, x):
    if x == 'shiny gold':
        return True
    # print("A", x, bags[x][1])
    return any(search(bags, y[1])
               for y in bags[x])


def main(args):
    data = [s.strip() for s in sys.stdin]
    # data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]

    bags = {}
    for line in data:
        bx,y = line.split(" bags contain ")
        # print(x, y)
        y = y.replace("bags", "").replace("bag", "").replace(".", "")
        ys = y.split(", ")
        nys = []
        for y in ys:
            x = y.strip().split(" ")
            if x[0] == 'no': break
            nys.append((int(x[0]), " ".join(x[1:])))

        print((bx, nys))
        bags[bx] = nys


    print(bags)
    n = 0
    for k in bags:
        if search(bags, k) and k != 'shiny gold':
            n += 1

    print(len(bags))
    print(n)

    # print(data)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

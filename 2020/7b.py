#!/usr/bin/env python3

import sys

def search(bags, x):
    if x == 'shiny gold':
        return True
    return any(search(bags, y[1])
               for y in bags[x])

def collect(bags, x):
    return 1+sum(k*collect(bags, y)
                 for k,y in bags[x])


def main(args):
    data = [s.strip() for s in sys.stdin]

    bags = {}
    for line in data:
        bx,y = line.split(" bags contain ")
        y = y.replace("bags", "").replace("bag", "").replace(".", "")
        ys = y.split(", ")
        nys = []
        for y in ys:
            x = y.strip().split(" ")
            if x[0] == 'no': break
            nys.append((int(x[0]), " ".join(x[1:])))

        bags[bx] = nys


    n = 0
    for k in bags:
        if search(bags, k) and k != 'shiny gold':
            n += 1

    print(n)
    print(collect(bags, 'shiny gold')-1)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

#!/usr/bin/env python3

import sys


def main(args):
    nubs = [s.strip() for s in sys.stdin]
    for i in range(len(nubs)):
        for j in range(10):
            nubs[i] = nubs[i].replace("  ", " ")


    wrong = 0

    for nub in nubs:
        butts = nub.split(" ")
        butts = [int(x) for x in butts]
#        print(butts)
        lol = sum(butts)
        for x in butts:
            other = lol - x
#            print(other, x)
            if other <= x:
                wrong += 1
                break
    print(len(nubs) - wrong)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

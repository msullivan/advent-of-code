#!/usr/bin/env python3

import sys


def main(args):
    nubs = [s.strip() for s in sys.stdin]
    for i in range(len(nubs)):
        for j in range(10):
            nubs[i] = nubs[i].replace("  ", " ")
        nubs[i] = nubs[i].split(" ")
        nubs[i] = [int(x) for x in nubs[i]]
    print(nubs)


    wrong = 0

    fuckup = []
    i = 0
    while i < len(nubs):
        fuckup += [[nubs[i][0], nubs[i+1][0], nubs[i+2][0]]]
        fuckup += [[nubs[i][1], nubs[i+1][1], nubs[i+2][1]]]
        fuckup += [[nubs[i][2], nubs[i+1][2], nubs[i+2][2]]]
        i += 3


    for butts in fuckup:
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

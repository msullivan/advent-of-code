#!/usr/bin/env python3

from collections import defaultdict
import sys


def main(args):
    # data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    data = [s.strip() for s in sys.stdin]

    lines = []
    for x in data:
        y, z = x.split(" (")
        ingreds = y.split(" ")
        allegs = z.replace("contains ", "").replace(",", "").replace(")", "").split(" ")
        lines.append((ingreds, allegs))

    all_ingreds = {x for ig, _ in lines for x in ig}

    poss = defaultdict(list)
    for igs, allegs in lines:
        for al in allegs:
            poss[al].append(set(igs))

    ig_map = {}
    while True:
        for al, apps in poss.items():
            ints = set.intersection(*apps)
            if len(ints) == 1:
                ig = list(ints)[0]
                ig_map[ig] = al
                break
        else:
            break

        for al, apps in poss.items():
            for bit in apps:
                bit.discard(ig)

    non = all_ingreds - set(ig_map.values())
    cnt = 0
    for igs, _ in lines:
        for ig in non:
            cnt += igs.count(ig)

    print(cnt)
    l = sorted(ig_map.keys(), key=lambda k: ig_map[k])
    print(','.join(l))

if __name__ == '__main__':
    sys.exit(main(sys.argv))

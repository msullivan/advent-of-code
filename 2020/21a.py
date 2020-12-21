#!/usr/bin/env python3

from collections import defaultdict
import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]


def main(args):
    # data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    data = [s.strip() for s in sys.stdin]

    lines = []
    for x in data:
        y, z = x.split(" (")
        ingreds = y.split(" ")
        allegs = z.replace("contains ", "").replace(",", "").replace(")", "").split(" ")
        lines.append((ingreds, allegs))

    all_allegs = {x for _, als in lines for x in als}
    print(all_allegs)
    all_ingreds = {x for ig, _ in lines for x in ig}

    poss = defaultdict(list)
    poss2 = defaultdict(list)
    for igs, allegs in lines:
        for al in allegs:
            poss[al].append(set(igs))
        for ig in igs:
            poss2[ig].append(set(allegs))

    print(poss2)
    non = {x for x in all_ingreds if x not in poss2}
    #print(non)

    ig_map = {}
    while True:
        for al, apps in poss.items():
            int = set.intersection(*apps)
            # print(al, apps, int)
            # print(len(int))
            if len(int) == 1:
                ig = list(int)[0]
                ig_map[al] = ig
                print("FUCK YOU", al, int)
                break

        else:
            break

        for al, apps in poss.items():
            for bit in apps:
                bit.discard(ig)

    print(ig_map)
    non = all_ingreds - set(ig_map.values())
    print(non)

    cnt = 0
    for igs, _ in lines:
        for ig in non:
            cnt += igs.count(ig)

    print(cnt)

    # non = set()
    # for ig, apps in poss2.items():
    #     ints = set.intersection(*apps)
    #     print(ig, apps, ints)
    #     print(len(ints))
    #     if not ints:
    #         non.add(ig)

    # print(non)





if __name__ == '__main__':
    sys.exit(main(sys.argv))

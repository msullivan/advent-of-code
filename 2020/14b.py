#!/usr/bin/env python3

from collections import defaultdict
import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]


from itertools import chain, combinations

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def main(args):
    # data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    data = [s.strip() for s in sys.stdin]

    mem = defaultdict(int)

    for line in data:
        if "mask" in line:
            smask = line.split(" = ")[1]
            mmask = int(smask.replace("1", "0").replace("X", "1"), 2)
            mval = int(smask.replace("X", "0"), 2)
            # print(hex(mmask), hex(mval))
        else:
            addr, val = extract(line)
            addr |= mval
            addr &= ~mmask

            idxes = [i for i, x in enumerate(reversed(smask)) if x == "X"]
            print(smask, idxes)
            for bits in powerset(idxes):
                nval = addr
                for bit in bits:
                    nval |= 1 << bit
                # print(addr, val)
                mem[nval] = val

    # print(mem)
    print(sum(mem.values()))


if __name__ == '__main__':
    sys.exit(main(sys.argv))

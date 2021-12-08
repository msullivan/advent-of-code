#!/usr/bin/env python3

import sys

import itertools


CS = [
    "abcefg", "cf", "acdeg", "acdfg", "bcdf",
    "abdfg", "abdefg", "acf", "abcdefg", "abcdfg",
]
MCS = {k: i for i, k in enumerate(CS)}

def get(s):
    l = list(s)
    assert len(l) == 1, s
    return l[0]

def solve(codes, nums):
    LETS = "abcdefg"
    for perm in itertools.permutations(LETS):
        m = {k: v for k, v in zip(perm, LETS)}
        pcodes = ["".join(sorted(m[c] for c in code)) for code in codes]
        matches = {MCS.get(pcode) for pcode in pcodes}
        if len(matches) == 10 and None not in matches:
            break
    else:
        raise ValueError

    snum = ""
    for num in nums:
        numk = "".join(sorted(m[c] for c in num))
        snum += str(MCS[numk])
    print(snum)
    return int(snum)


def main(args):
    data = [s.strip() for s in sys.stdin]
    data = [x.split(" | ") for x in data]
    data = [(x.split(" "), y.split(" ")) for x, y in data]

    # solve(*data[0])
    print(sum(solve(*ent) for ent in data))

if __name__ == '__main__':
    main(sys.argv)

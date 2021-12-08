#!/usr/bin/env python3

import sys

CS = [
    "abcefg", "cf", "acdeg", "acdfg", "bcdf",
    "abdfg", "abdefg", "acf", "abcdefg", "abcdfg",
]
LENS = set(len(x) for x in CS)
RCS = {l: [(i, x) for i, x in enumerate(CS) if len(x) == l] for l in LENS}
MCS = {k: i for i, k in enumerate(CS)}

def get(s):
    l = list(s)
    assert len(l) == 1, s
    return l[0]

# easy 1,4, 7, 8
def solve(codes, nums):
    print(RCS)
    mapping = {}
    rmap = {}
    for code in codes:
        opts = RCS[len(code)]
        if len(opts) == 1:
            mapping[code] = opts[0]
            rmap[opts[0][0]] = code

    print(rmap)
    la = get(list(set(rmap[7]) - set(rmap[1])))
    bd = (set(rmap[4]) - (set(rmap[1])|set(rmap[7])))

    cf = (set(rmap[1])&set(rmap[7])&set(rmap[4]))

    # 2, 3, 5
    fives = [set(x) for x in codes if len(x) == 5]
    three = get([x for x in fives if cf.issubset(x)])
    print("THREE", three)
    ld = get(bd & three)
    lb = get(set(rmap[4]) - {la, ld, *cf})
    lg = get(three - {la, ld, *cf})

    sixes = [set(x) for x in codes if len(x) == 6]
    nine = get([x for x in sixes if (cf|{ld}).issubset(x)])
    print("NINE", nine)
    le = get(set("abcdefg") - nine)

    # just c, f
    five = get([x for x in fives if le not in x and lb in x])
    lf = get((five & cf))
    lc = get(cf - {lf})

    m = {"a": la, "b": lb, "c": lc, "d": ld, "e": le, "f": lf, "g": lg}
    lm = {v: k for k, v in m.items()}
    print(lm)

    snum = ""
    for num in nums:
        numk = "".join(sorted(lm[c] for c in num))
        snum += str(MCS[numk])
    rnum = int(snum)
    print(rnum)
    return rnum
    # print(la, lb, ld, le, lg, cf)



def main(args):
    # data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    # data = [int(s.strip()) for s in sys.stdin]
    data = [s.strip() for s in sys.stdin]
    data = [x.split(" | ") for x in data]
    data = [(x.split(" "), y.split(" ")) for x, y in data]

    # solve(*data[0])
    print(sum(solve(*ent) for ent in data))

    # print(RCS)

if __name__ == '__main__':
    main(sys.argv)

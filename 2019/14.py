#!/usr/bin/env python3

import sys

def parse(s):
    a, b = s.split(" ")
    return int(a), b


def go(producers, num):
    required = {"FUEL": num}
    produced = {}
    while True:
        pending = {k for k, v in required.items() if v > produced.get(k, 0)}
        if pending == {'ORE'}: break
        to_try = next(x for x in pending if x != 'ORE')

        rule = producers[to_try]
        # print(rule)
        num_produced, _ = rule[1]
        # print(produced)
        times = (required[to_try] - produced.get(to_try, 0) + (num_produced-1)) // num_produced
        for v, e in rule[0]:
            required[e] = required.get(e, 0) + times*v
        produced[to_try] = produced.get(to_try, 0) + times*num_produced

        # print(required, produced)

    return required['ORE']


def main():
    data = [s.strip() for s in sys.stdin]
    rxns = []
    for line in data:
        l, r = line.split(" => ")
        rxns.append(([parse(x) for x in l.split(", ")], parse(r)))

    elements = {y for _, (x, y) in rxns}

    producers = {rxn[1][1]: rxn for rxn in rxns}
    part1 = go(producers, 1)

    # binary search for it
    n = 1
    x = part1
    while x < 1000000000000:
        n *= 2
        x = go(producers, n)
        # print(n, x)

    lo = n // 2
    hi = n
    while lo < hi:
        mid = (lo + hi) // 2
        n = mid
        x = go(producers, n)
        # print(n, x)
        if x < 1000000000000:
            lo = mid + 1
        else:
            hi = mid

    part2 = lo - 1
    print(part1)
    print(part2)


if __name__ == '__main__':
    main()

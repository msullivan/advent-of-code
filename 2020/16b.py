#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'\d+', s)]


def valid(n, r):
    (a,b),(c,d) = r
    return (a <= n <= b) or (c <= n <= d)

def main(args):
    # data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    data = [s.strip() for s in sys.stdin]

    fields = {}
    for i,x  in enumerate(data):
        if x == "": break
        thing = x.split(":")[0]
        a,b,c,d = extract(x)
        fields[thing] = ((a,b),(c,d))

    print(fields)

    tickets = []
    for x in data[i:]:
        if ',' not in x: continue
        z = [int(y) for y in x.split(',')]
        tickets.append(z)

    my_ticket = tickets[0]
    tickets = tickets[1:]

    print(tickets)
    cnt = 0
    fucked = []
    good = []
    for t in tickets:
        if not [
            v
            for v in t
            if all(not valid(v, r) for r in fields.values())
        ]:
            good.append(t)


    options = [set(fields.keys()) for _ in range(len(good[0]))]
    print(len(good[0]))
    for t in good:
        for i, f in enumerate(t):
            print(fields)
            opts = set(name for name, range in fields.items()
                       if valid(f, range))
            options[i] &= opts

    picks = {}
    while True:
        for i, thing in enumerate(options):
            if len(thing) == 1:
                break
        else:
            assert False
        pick = list(thing)[0]
        picks[pick] = i
        for x in options:
            x.discard(pick)

        if not any(x for x in options):
            break

    print(picks)

    departuresf = [x for x in fields if x.startswith('departure')]
    depts = [my_ticket[picks[f]] for f in departuresf]
    print(depts)
    prod = 1
    for x in depts: prod *= x
    print(prod)


    # print(data)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

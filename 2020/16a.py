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
    for t in tickets:
        fucked += [
            v
            for v in t
            if all(not valid(v, r) for r in fields.values())
        ]

    print(sum(fucked))


    # print(data)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

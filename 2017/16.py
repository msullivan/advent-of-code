#!/usr/bin/env python3

import sys

def round(things, data):
    for move in data:
        if move[0] == 's':
            amt = int(move[1:])
            things = things[-amt:] + things[:-amt]
        elif move[0] == 'x':
            a,b = map(int, move[1:].split("/"))
            things[a], things[b] = things[b], things[a]
        else:
            x, y = move[1], move[3]
            a = things.index(x)
            b = things.index(y)
            things[a], things[b] = things[b], things[a]
    return things


def main(args):
    data = [s.strip() for s in sys.stdin]
    data = data[0].split(",")

    seen = {}
    things = [chr(ord('a')+i) for i in range(16)]

    print(''.join(round(list(things), data)))

    n = 0
    while True:
        s = ''.join(things)
        if s in seen: break
        seen[s] = n
        things = round(things, data)
        n += 1

    loop = n - seen[s]
    k = (1000000000 - seen[s]) % loop + seen[s]
    print([k2 for k2,v in seen.items() if k == v][0])


if __name__ == '__main__':
    sys.exit(main(sys.argv))

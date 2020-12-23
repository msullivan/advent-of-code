#!/usr/bin/env python3

import sys

class Nobe:
    def __init__(self, val):
        self.val = val
        self.next = None

def go(cur, map, N):
    start3 = cur.next
    last3 = start3.next.next
    end3 = last3.next
    cur.next = end3
    up = [start3.val, start3.next.val, start3.next.next.val]

    dest = cur.val - 1
    if dest == 0:
        dest = N
    while dest in up:
        dest -= 1
        if dest == 0:
            dest = N

    dnode = map[dest]
    last3.next = dnode.next
    dnode.next = start3

    return cur.next


def main(args):
    data = [s.strip() for s in sys.stdin]
    cups = [int(x) for x in data[0]]

    print(cups)

    lcups = len(cups)
    N = 1000000
    map = [None]*(N+1)

    last = dummy = Nobe(-1)
    for i in range(1000000):
        val = cups[i] if i < lcups else i+1
        nobe = Nobe(val)
        map[val] = nobe
        last.next = nobe
        last = nobe
    cur = last.next = dummy.next

    for i in range(10000000):
        if i % 10000 == 0:
            print(i)
        cur = go(cur, map, N)

    cup1 = map[1]
    x1 = cup1.next.val
    x2 = cup1.next.next.val
    print(x1, x2)
    print(x1*x2)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

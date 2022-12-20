#!/usr/bin/env python3

import sys

K = 811589153

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [K*int(s.rstrip('\n')) for s in file]
    idx0 = data.index(0)
    data = list(enumerate(data))
    order = list(data)

    N = len(data)
    for _ in range(10):
        for pos, i in order:
            j = data.index((pos, i))
            del data[j]
            idx = (j+i) % (N-1)
            data[idx:idx] = [(pos, i)]

    nidx0 = data.index((idx0, 0))
    print(sum(data[(nidx0+k)%N][1] for k in (1000, 2000, 3000)))


if __name__ == '__main__':
    main(sys.argv)

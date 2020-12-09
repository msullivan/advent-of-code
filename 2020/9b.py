#!/usr/bin/env python3

import sys

def match(pre, n):
    for x in pre:
        for y in pre:
            if x != y and x + y == n:
                return (x, y)
    return None

def main(args):
    # data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    data = [int(s.strip()) for s in sys.stdin]

    N = 25
    last = data[:N]
    rest = data[N:]

    prev = None
    for num in rest:
        if not match(last, num):
            break
        last = last[1:] + [num]
        prev = num

    print(num)
    part1 = num

    for i in range(len(data)):
        for j in range(len(data)):
            if sum(data[i:j]) == part1:
                print(min(data[i:j]) + max(data[i:j]))
                return

if __name__ == '__main__':
    sys.exit(main(sys.argv))

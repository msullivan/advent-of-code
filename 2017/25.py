#!/usr/bin/env python3

import sys
from collections import defaultdict

L = -1
R = 1
# I was just a bum and typed in the turing machine diagram of course.
machine = {
    'A': [(1, R, 'B'), (0, R, 'C')],
    'B': [(0, L, 'A'), (0, R, 'D')],
    'C': [(1, R, 'D'), (1, R, 'A')],
    'D': [(1, L, 'E'), (0, L, 'D')],
    'E': [(1, R, 'F'), (1, L, 'B')],
    'F': [(1, R, 'A'), (1, R, 'E')],
}


def main(args):
    tape = defaultdict(int)
    size = 12399302
    pos = 0
    state = 'A'
    for i in range(size):
        val, dir, new = machine[state][tape[pos]]
        tape[pos] = val
        pos += dir
        state = new
    print(len([x for x in tape.values() if x == 1]))



if __name__ == '__main__':
    sys.exit(main(sys.argv))

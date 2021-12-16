#!/usr/bin/env python3

import copy
import sys
import time
from collections import defaultdict, deque
from intcode import IntCode

# !(b&c) =

# (!b and d) | (!a)
# ! (!(!b and d) & a)


PROGRAM = """
NOT B T
NOT T T
AND C T
NOT T J
AND D J
NOT J J
AND A J
NOT J J
WALK
""".lstrip()


def main(args):
    data = [s.strip() for s in sys.stdin]
    p = [int(x) for x in data[0].split(",")]
    board = defaultdict(lambda: " ")

    # Part 1
    interp = IntCode(p)
    out = interp.run([ord(c) for c in PROGRAM])

    answer = None
    if out[-1] > 255:
        answer = out.pop()

    s = "".join(chr(x) for x in out)
    print(s)
    m = s.split("\n")
    print(answer)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

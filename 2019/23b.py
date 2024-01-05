#!/usr/bin/env python3

import array
import sys
from intcode import IntCode

# My competition version of this I copied and hacked up the
# interpreter specifically for the problem. Much later, after I added
# a maxsteps feature, I made it able to use the C interpreter.

class ilist:
    def __init__(self):
        self.l = []
        self.idle = False

    def pop(self, i):
        if not self.l:
            self.idle = True
            return -1
        self.idle = False
        return self.l.pop(i)


def main(args):
    data = [s.strip() for s in sys.stdin]
    p = array.array('q', [int(x) for x in data[0].split(",")])

    N = 50

    computers = [IntCode(p, input=ilist()) for i in range(N)]
    for i in range(N):
        computers[i].input.l.append(i)

    nat = None
    firsty = None
    lasty = -1

    while True:
        for i, c in enumerate(computers):
            c.execute(maxsteps=100)
            while len(c.output) >= 3:
                target, x, y = c.output[:3]
                # print(target, x, y, i)
                del c.output[0:3]
                if target == 255:
                    if firsty is None:
                        firsty = y
                    nat = x, y
                else:
                    computers[target].input.l.extend([x, y])

        if nat and all(c.input.idle and not c.input.l for c in computers):
            if lasty == nat[1]:
                print(firsty)
                print(lasty)
                return
            lasty = nat[1]
            computers[0].input.l.extend(nat)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

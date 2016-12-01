#!/usr/bin/env python3

import sys

def process(cmd, lights):
    cmd = cmd.replace("turn ", "")
    cmd, c1, _, c2 = cmd.split(" ")
    x1, y1 = (int(x) for x in c1.split(","))
    x2, y2 = (int(x) for x in c2.split(","))

#    print(x1, y1, x2, y2)
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            if cmd == "on":
                lights[x][y] += 1
            elif cmd == "off":
                if lights[x][y] > 0:
                    lights[x][y] -= 1
            elif cmd == "toggle":
                lights[x][y] += 2


def main(args):
    cmds = [s.strip() for s in sys.stdin]

    lights = [[0 for i in range(1000)] for j in range(1000)]

    for c in cmds:
        process(c, lights)

    count = 0
    for row in lights:
        for light in row:
            count += light

    print(count)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

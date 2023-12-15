#!/usr/bin/env python3

import sys

def hash(s):
    val = 0
    for c in s:
        val += ord(c)
        val *= 17
        val %= 256
    return val


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = file.read().replace('\n', '').split(',')

    boxes = [{} for _ in range(256)]

    for node in data:
        if '-' in node:
            s = node[:-1]
            box = hash(s)
            boxes[box].pop(s, None)
        else:
            s, n = node.split('=')
            box = hash(s)
            n = int(n)
            # don't try this on python3.5 or earlier ;)
            boxes[box][s] = n

    sum = 0
    for i, box in enumerate(boxes):
        i += 1
        for j, val in enumerate(box.values()):
            j += 1
            sum += i*j*val

    print(sum)

if __name__ == '__main__':
    main(sys.argv)

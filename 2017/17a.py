#!/usr/bin/env python3

import sys

def main(args):
    cnt = 2017
    n = 3
    n = 345
    buf = [0]
    pos = 0

    for i in range(cnt):
        #for j in range(n):
        #    pos = (pos + 1) % len(buf)
        pos = (pos + n) % len(buf)
        #print(pos)
        buf = buf[:pos+1] + [i+1] + buf[pos+1:]
        pos += 1

    print(buf[buf.index(2017)+1])


if __name__ == '__main__':
    sys.exit(main(sys.argv))

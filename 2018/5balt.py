#!/usr/bin/env python3

import sys

def doit(data):
    out = []
    for c in data:
        if out and c != out[-1] and c.upper() == out[-1].upper():
            out.pop()
        else:
            out.append(c)

    return len(out)

def main(data):
    data = [s.strip() for s in sys.stdin][0]

    lol = []
    for i in range(26):
        c = chr(ord('a') + i)
        n = list(data.replace(c, '').replace(c.upper(), ''))
        a = doit(n)
        lol.append(a)
    print(min(lol))


if __name__ == '__main__':
    sys.exit(main(sys.argv))

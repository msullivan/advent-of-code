#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]


def main(args):
    data = [s.strip() for s in sys.stdin]
    data.append('')

    crap = []
    cur = []
    for x in data:
        if not x:
            crap.append(list(cur))
            cur = []
        else:
            cur.extend(x.split(" "))

    data = crap

    total = 0
    for group in data:
        seen = set()
        for person in group:
            seen.update(person)

        total += len(seen)

    print(total)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

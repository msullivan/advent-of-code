#!/usr/bin/env python3

# Obviously this is how I should have done it but did not.

import sys


def main(args):
    data = [s.strip() for s in sys.stdin]

    seen = set()
    for row in data:
        row = row.replace("F", "0").replace("B", "1")
        row = row.replace("L", "0").replace("R", "1")
        id = int(row, 2)
        seen.add(id)

    print(max(seen))
    for x in range(max(seen)):
        if x not in seen and x+1 in seen and x-1 in seen:
            print(x)

    # print(data)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

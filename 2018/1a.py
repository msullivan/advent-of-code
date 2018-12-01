#!/usr/bin/env python3

import sys

def main(args):
    data = [s.strip() for s in sys.stdin]
    print(sum(int(x) for x in data))

if __name__ == '__main__':
    sys.exit(main(sys.argv))

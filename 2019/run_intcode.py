#!/usr/bin/env python3

import sys
from intcode import IntCode

def main(args):
    data = ''.join([s.strip() for s in open(args[1]) if not s.startswith('#')])
    p = [int(x) for x in data.split(",")]

    inp = [int(x) for x in args[2:]]

    interp = IntCode(p)
    print(interp.run(inp))

if __name__ == '__main__':
    sys.exit(main(sys.argv))

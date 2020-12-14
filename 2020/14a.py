#!/usr/bin/env python3

from collections import defaultdict
import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]


def main(args):
    # data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    data = [s.strip() for s in sys.stdin]

    mem = defaultdict(int)

    for line in data:
        if "mask" in line:
            smask = line.split(" = ")[1]
            mmask = int(smask.replace("1", "0").replace("X", "1"), 2)
            mval = int(smask.replace("X", "0"), 2)
            print(hex(mmask), hex(mval))
        else:
            addr, val = extract(line)
            print(addr, val)
            write = val & mmask
            new = write | mval
            print("write", addr, new)
            mem[addr] = new

    print(mem)
    print(sum(mem.values()))



    # print(data)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

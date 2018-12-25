#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

def main(args):
    data = [extract(s.strip())[0] for s in sys.stdin]
    seen = set()
    for i in range(len(data)):
        if data[i] in seen:
            print(data[i-1])
            return
        seen.add(data[i])

if __name__ == '__main__':
    sys.exit(main(sys.argv))

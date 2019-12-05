#!/usr/bin/env python3

import sys

def extract(s):
    import re
    return [int(x) for x in re.findall(r'\d+', s)]

def go(input):
    lo, hi = extract(input)
    count = 0
    for i in range(lo, hi+1):
        s = str(i)
        if sorted(s) != list(s): continue
        if not any(s[j] == s[j+1] for j in range(5)): continue
        count += 1
    print(count)

def main(args):
    go("256310-732736")

if __name__ == '__main__':
    sys.exit(main(sys.argv))

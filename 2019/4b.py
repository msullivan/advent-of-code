#!/usr/bin/env python3

import sys

def extract(s):
    import re
    return [int(x) for x in re.findall(r'\d+', s)]

def matches(i):
    s = str(i)
    if sorted(s) != list(s): return False
    if not any(s[j] == s[j+1] and (j == 4 or s[j] != s[j+2])
                                   and (j == 0 or s[j] != s[j-1]) for j in range(5)): return False
    return True

def go(input):
    lo, hi = extract(input)
    count = 0
    for i in range(lo, hi+1):
        #if not any(s[j] == s[j+1] == s[j+2] for j in range(4)): continue
        if matches(i):
            count += 1
    print(count)

def main(args):
    go("256310-732736")

if __name__ == '__main__':
    sys.exit(main(sys.argv))

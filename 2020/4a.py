#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

bs = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]
bs2 = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

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

    valid = 0
    for pp in crap:
        things = [x.split(":")[0] for x in pp]
        assert all(x in bs for x in things)
        print(things)
        if all(x in things for x in bs2):
            valid += 1



    print(crap)
    print(valid)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

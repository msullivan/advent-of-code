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
        things = dict(x.split(":") for x in pp)
        assert all(x in bs for x in things)
        print(things)
        if not all(x in things for x in bs2): continue

        x = things['byr']
        if not (len(x) == 4 and int(x) >= 1920 and int(x) <= 2002): continue
        x = things['iyr']
        if not (len(x) == 4 and int(x) >= 2010 and int(x) <= 2020): continue
        x = things['eyr']
        if not (len(x) == 4 and int(x) >= 2020 and int(x) <= 2030): continue

        x = things['hgt']
        unit = x[-2:]
        try:
            amt = int(x[:-2])
        except Exception:
            continue
        if unit == 'cm':
            if not (amt >= 150 and amt <= 193): continue
        elif unit == 'in':
            if not (amt >= 59 and amt <= 76): continue
        else:
            continue

        x = things['hcl']
        if x[0] != '#': continue
        if len(x) != 7: continue
        if any(c not in "01234567890abcdef" for c in x[1:]): continue

        x = things['ecl']
        if x not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]: continue

        x = things['pid']
        if len(x) != 9: continue
        if any(c not in "01234567890" for c in x): continue

        valid += 1

    print(valid)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

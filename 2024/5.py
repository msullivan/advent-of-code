#!/usr/bin/env python3

import sys
import re
import functools

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]

    deps = {}
    for x in data[0]:
        pre, post = extract(x)
        deps.setdefault(post, []).append(pre)

    def compare(x, y):
        if x == y:
            return 0
        elif y in deps.get(x, []):
            return -1
        else:
            return 1

    s = 0
    s2 = 0
    for line in data[1]:
        nums = extract(line)
        seen = set()
        ok = True
        for num in nums:
            for other in deps.get(num, []):
                if other in nums and other not in seen:
                    ok = False
            seen.add(num)
        if ok:
            s += nums[len(nums)//2]

        if not ok:
            nums2 = sorted(nums, key=functools.cmp_to_key(compare))
            s2 += nums2[len(nums)//2]


    print(s)
    print(s2)


if __name__ == '__main__':
    main(sys.argv)

#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

NUMS = {'x': 0, 'm': 1, 'a': 2, 's': 3}

def apply(rules, obj):
    r = 'in'
    while True:
        if r == 'R':
            return False
        if r == 'A':
            return True
        rx = rules[r]
        cmds = rx.split(',')
        for cmd in cmds:
            if ':' not in cmd:
                r = cmd
                break
            op, tgt = cmd.split(':')
            num = extract(op)[0]
            key = op[0]
            objv = obj[NUMS[key]]
            if '<' in op:
                res = objv < num
            else:
                res = objv > num
            if res:
                r = tgt
                break

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]

    rules, objs = data
    drules = {}
    for r in rules:
        n, x = r.split('{')
        drules[n] = x[:-1]

    rules = drules

    sobjs = objs
    objs = []
    for s in sobjs:
        objs.append(extract(s))

    print(rules)

    ans = 0
    for obj in objs:
        if apply(rules, obj):
            ans += sum(obj)

    print(ans)


if __name__ == '__main__':
    main(sys.argv)

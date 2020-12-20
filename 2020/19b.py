#!/usr/bin/env python3

import sys
import re
import functools

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

def match(grammar, inp):
    # I think this is actually a recursive version of the CYK
    # algorithm.
    @functools.lru_cache(maxsize=None)
    def m(nr, t, s):
        if nr == -1:
            return t == s
        rule = grammar[nr]
        if isinstance(rule, str):
            return rule == inp[t:s]

        for p1, p2 in rule:
            for i in range(t, s):
                if m(p1, t, i) and m(p2, i, s):
                    return True
        return False

    return m(0, 0, len(inp))


def main(args):
    data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    sgrammar = data[0]
    lines = data[1] if len(data) > 1 else []

    grammar = {}
    for line in sgrammar:
        if not line: continue
        ns = extract(line)
        k = ns[0]

        if len(ns) == 1:
            grammar[k] = line.split('"')[1]
        else:
            asdf = line.split(":")[1]
            res = []
            for part in asdf.split("|"):
                xs = extract(part)
                if len(xs) == 1:
                    xs = [-1] + xs
                assert len(xs) == 2
                res.append(xs)
            grammar[k] = res

    grammar[8] = [[-1, 42], [42, 8]]
    # lol I can't handle 3-ary productions
    grammar[1000] = [[11, 31]]
    grammar[11] = [[42, 31], [42, 1000]]

    cnt = 0
    for x in lines:
        b = match(grammar, x)
        if b: cnt += 1
        print(x, b)

    print(cnt)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

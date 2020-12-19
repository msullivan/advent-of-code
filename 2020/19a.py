#!/usr/bin/env python3

import sys
import re
import functools

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

def match(grammar, inp):
    @functools.lru_cache(maxsize=None)
    def m(nr, t, s):
        rule = grammar[nr]
        if isinstance(rule, str):
            return rule == inp[t:s]

        # print(nr, rule)
        for asdf in rule:
            if len(asdf) == 1:
                if m(asdf[0], t, s):
                    return True
                continue
            p1, p2 = asdf

            for i in range(t, s):
                if m(p1, t, i) and m(p2, i, s):
                    return True
        return False

    return m(0, 0, len(inp))


def main(args):
    data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    # data = [s.strip() for s in sys.stdin]
    sgrammar = data[0]
    lines = data[1] if len(data) > 1 else []

    grammar = {}
    for line in sgrammar:
        if not line: continue
        ns = extract(line)
        print(line, ns)
        k = ns[0]


        if len(ns) == 1:
            grammar[k] = line.split('"')[1]
        else:
            asdf = line.split(":")[1]
            res = []
            for part in asdf.split("|"):
                res.append(extract(part))
            grammar[k] = res

        # elif len(ns) == 5:
        #     grammar[k] = [ns[1:3], ns[3:5]]
        # else:
        #     assert len(ns) in (2, 3), line
        #     grammar[k] = [ns[1:3]]

    print(grammar)
    cnt = 0
    for x in lines:
        b = match(grammar, x)
        if b: cnt += 1
        print(x, b)
#    cnt = len([x for x in lines if match(grammar, x)])


    print(cnt)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

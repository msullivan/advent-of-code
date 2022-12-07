#!/usr/bin/env python3

import sys

def main(args):
    data = [s.rstrip('\n') for s in sys.stdin]

    cmds = []
    i = 0
    while i < len(data):
        s = data[i]
        i += 1
        ls = []
        while i < len(data) and not data[i][0] == '$':
            ls.append(data[i])
            i += 1
        cmds.append((s[2:], ls))

    tree = {}
    sizes = {}
    cur = ()
    for cmd, out in cmds:
        if cmd.startswith('cd'):
            x, arg = cmd.split(' ')
            if arg == '/':
                cur = ()
            elif arg == '..':
                cur = cur[:-1]
            else:
                cur += (arg,)
        else:
            subs = [l.split(' ')[1] for l in out]
            tree[cur] = subs
            for l in out:
                sz, name = l.split(' ')
                if sz != 'dir':
                    sizes[cur + (name,)] = int(sz)

    dsizes = {}

    def go(node):
        if node in sizes:
            return sizes[node]
        sz = 0
        for sub in tree[node]:
            sz += go(node + (sub,))
        dsizes[node] = sz
        return sz

    go(())

    # Part 1
    sz = sum(v for v in dsizes.values() if v <= 100000)
    print(sz)

    # Part 2
    avail = 70000000 - dsizes[()]
    need = 30000000 - avail
    print(min(x for x in dsizes.values() if x > need))



if __name__ == '__main__':
    main(sys.argv)

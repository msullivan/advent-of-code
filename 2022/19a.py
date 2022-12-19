#!/usr/bin/env python3

import sys
import re
import functools

def extract(s):
    return [int(x) for x in re.findall(r'(-?\d+).?', s)]

def vadd(v1, v2):
    # return tuple(x + y for x, y in zip(v1, v2))
    return (v1[0]+v2[0], v1[1]+v2[1], v1[2]+v2[2], v1[3]+v2[3])
def vsub(v1, v2):
    return (v1[0]-v2[0], v1[1]-v2[1], v1[2]-v2[2], v1[3]-v2[3])
def scale(c, v2):
    return (c*v2[0], c*v2[1], c*v2[2], c*v2[3])
def vpos(v1):
    return all(x >= 0 for x in v1)

def one_spot(i, n=4):
    return tuple(int(j == i) for j in range(n))

def possible(robots, cost):
    return all(robots[i] or not cost[i] for i in range(4))


def step(bprint, state):
    opts = []
    robots, stuff = state

    nothing = robots, stuff
    opts.append(nothing)

    for i, opt in enumerate(bprint):
        sub = vsub(stuff, opt)
        if vpos(sub):
            opts.append((vadd(robots, one_spot(i)), sub))

    print(len(opts))

    return [(r, vadd(robots, s)) for r, s in opts]


MTIME = 24

def step(bprint, state, time):
    opts = []
    robots, stuff = state

    # nothing = robots, stuff
    # opts.append(nothing)

    for i, opt in enumerate(bprint):

        sub = vsub(stuff, opt)
        nrobots = vadd(robots, one_spot(i))
        if possible(robots, opt):
            # XXX
            for j in range(20):
                nstuff = vadd(stuff, scale(j, robots))
                sub = vsub(nstuff, opt)
                if vpos(sub):
                    break
            nt = time + j + 1
            if nt <= MTIME:
                opts.append((nrobots, vadd(robots, sub), nt))


    # print('OPTS', opts)
    if not opts:
        opts = [(robots, stuff, time+1)]

    return opts

def search(bprint, state, time):
    if time < 15:
        print(state, time)
    if state[0][0] > 5 or state[0][1] > 10:
        return -1
    if time >= MTIME:
        return state[1][-1]

    opts = []
    for (x, y, dt) in step(bprint, state, time):
        n = (x, y)
        opts.append(search(bprint, n, dt))
    return max(opts)


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
    # data = [int(s.rstrip('\n')) for s in file]
    data = [s.rstrip('\n') for s in file]

    bprints = {}
    starting = (1, 0, 0, 0), (0, 0, 0, 0)
    for line in data:
        nbr, o, c, obs_o, obs_clay, ge_o, ge_obs = extract(line)
        bprints[nbr] = (
            (o, 0, 0, 0),
            (c, 0, 0, 0),
            (obs_o, obs_clay, 0, 0),
            (ge_o, 0, ge_obs, 0),
        )

    opts = {}
    for nbr, bprint in bprints.items():
        print('==================', nbr)
        opts[nbr] = search(bprint, starting, 0)

    print(opts)
    print(sum(k*v for k, v in opts.items()))


if __name__ == '__main__':
    main(sys.argv)

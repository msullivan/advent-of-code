#!/usr/bin/env python3

# also b

import sys, json
from collections import defaultdict

def main(args):
    shit = [s.strip() for s in sys.stdin]

    state = defaultdict(list)
    outputs = defaultdict(list)
    lol = {"bot": state, "output": outputs}
    cmds = dict()


    for line in shit:
        parts = line.split(" ")
        if parts[0] == "value":
            state[int(parts[5])] += [int(parts[1])]
        else:
            bot = int(parts[1])
            cmd = ((parts[5], int(parts[6])),
                   (parts[-2], int(parts[-1])))
            cmds[bot] = cmd

    while True:
        stuff = [x for x in list(state.keys()) if len(state[x]) == 2]
        for x in stuff:
            nus = sorted(state[x])
            state[x] = []
            ((low_t, low_n), (hi_t, hi_n)) = cmds[x]
            lol[low_t][low_n] += [nus[0]]
            lol[hi_t][hi_n] += [nus[1]]
            if nus == [17, 61]:
                print(x)
                break
        if not stuff: break

    print(outputs[0][0] * outputs[1][0] * outputs[2][0])


if __name__ == '__main__':
    sys.exit(main(sys.argv))

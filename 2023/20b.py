#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import math
import itertools

# Obviously doesn't work in "general", though it might work on other
# inputs if they are fairly similar, since it doesn't hardcode names
# at least.
# Who knows though.


def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    data = [s.rstrip('\n') for s in file]


    inputs = defaultdict(list)
    nodes = {}
    flops = {}
    conjs = {}


    for line in data:
        l, r = line.split(' -> ')
        outs = r.split(', ')
        if l[0] == '%':
            n = l[1:]
            c = '%'
            flops[n] = False
        elif l[0] == '&':
            n = l[1:]
            c = '&'
        else:
            n = l
            c = 'b'

        nodes[n] = (c, outs)
        for out in outs:
            inputs[out].append(n)

    for name, (typ, outs) in nodes.items():
        if typ == '&':
            outs = inputs[name]
            conjs[name] = {k: False for k in outs}

    # print(inputs)
    # print(nodes)
    # print(flops)

    feeders = inputs[inputs['rx'][0]]
    print(feeders)

    nsent = [0, 0]

    first = {}
    diffs = {}
    diffs2 = {k: {} for k in nodes}
    flopped = {k: {k2: 0 for k2 in inputs[k]} for k in nodes}
    conjed = {}

    evs = deque()
    for cnt in itertools.count(1):
        # if cnt % 1 == 0:
        #     print('==================')
        #     # print(cnt)
        #     # sv = ''.join(str(int(b)) for b in flops.values())
        #     # # print(sv, int(sv, 2))
        #     # print()
        #     # print(conjs['zr'])
        #     # for inp in inputs['zr']:
        #     #     print(conjs[inp])
        #     print(sum(flops.values()))
        #     # print(conjs)
        #     print({k: sum(v.values()) for k, v in conjs.items()})

        if len(conjed) == len(feeders):
            break

        evs.append(('broadcaster', False, 'button'))
        while evs:
            node, val, sender = evs.popleft()
            # print(sender, val, node)
            nsent[val] += 1
            if node not in nodes:
                continue
            typ, outs = nodes[node]

            send = None
            if typ == 'b':
                send = val
            elif typ == '%':
                if val == False:
                    send = flops[node] = not flops[node]

                    if send:
                        if node not in first:
                            first[node] = cnt
                            diff = None
                        else:
                            diff = cnt - flopped[node][sender]
                            # if node in diffs:
                            #     if node not in {'jk'}:
                            #         assert (
                            #             diff == diffs[node]), (
                            #             (node, diff, diffs[node]),
                            #         )
                            diffs[node] = diff

                        flopped[node][sender] = cnt

            elif typ == '&':
                conjs[node][sender] = val
                send = not all(conjs[node].values())

                if node in feeders and send:
                    if send:
                        # KEY PRINT RIGHT HERE
                        print(node, cnt - conjed.get(node, 0))
                        conjed[node] = cnt

                # if not send:
                #     if node not in flopped:
                #         print('FIRST NAND', node, cnt)
                #         flopped.add(node)

            if send is not None:
                for out in outs:
                    evs.append((out, send, node))

    print(math.lcm(*conjed.values()))



if __name__ == '__main__':
    main(sys.argv)

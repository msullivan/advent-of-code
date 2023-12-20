#!/usr/bin/env python3

import sys
from collections import defaultdict, Counter, deque

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

    nsent = [0, 0]

    evs = deque()
    for cnt in range(1000):
        evs.append(('broadcaster', False, 'button'))
        while evs:
            node, val, sender = evs.pop()
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
            elif typ == '&':
                conjs[node][sender] = val
                send = not all(conjs[node].values())

            if send is not None:
                for out in outs:
                    evs.append((out, send, node))

    print(nsent)
    print(nsent[0]*nsent[1])



if __name__ == '__main__':
    main(sys.argv)

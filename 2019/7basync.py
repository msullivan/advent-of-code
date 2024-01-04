#!/usr/bin/env python3

# This is stupid, and not easier than anything else.
# Maybe I should rewrite this all in Haskell so I can do it that way.

import asyncio
import sys
import re
import time
import itertools


async def run(p, input, outputs):
    ip = 0
    while True:
        instr = p[ip]

        def read(i):
            mode = (instr // (10**(1+i))) % 10
            return p[p[ip+i]] if mode == 0 else p[ip+i]

        if instr % 100 == 1:
            p[p[ip+3]] = read(1) + read(2)
            ip += 4
        elif instr % 100 == 2:
            p[p[ip+3]] = read(1) * read(2)
            ip += 4
        elif instr % 100 == 3:
            val = await input.get()
            print("got input", ip, id(input), val)
            p[p[ip+1]] = val
            ip += 2
        elif instr % 100 == 4:
            for output in outputs:
                print("writing to", ip, id(output))
                await output.put(read(1))
            ip += 2
        elif instr % 100 == 5:
            if read(1) != 0:
                ip = read(2)
            else:
                ip += 3
        elif instr % 100 == 6:
            if read(1) == 0:
                ip = read(2)
            else:
                ip += 3
        elif instr % 100 == 7:
            if read(1) < read(2):
                p[p[ip+3]] = 1
            else:
                p[p[ip+3]] = 0
            ip += 4
        elif instr % 100 == 8:
            if read(1) == read(2):
                p[p[ip+3]] = 1
            else:
                p[p[ip+3]] = 0
            ip += 4
        elif instr % 100 == 99:
            break

async def go(p, perm):
    inputs = [asyncio.Queue() for _ in perm]
    outputs = [None] * len(perm)
    for i, x in enumerate(perm):
        inputs[i].put_nowait(x)
        outputs[(i-1)%5] = [inputs[i]]

    inputs[0].put_nowait(0)
    finalq = asyncio.Queue()
    outputs[-1].append(finalq)

    coros = [run(list(p), input, output) for input, output in zip(inputs, outputs)]
    await asyncio.gather(*coros)

    while not finalq.empty():
        res = finalq.get_nowait()

    return res


def main(args):
    data = [s.strip() for s in sys.stdin]
    p = [int(x) for x in data[0].split(",")]
    op = list(p)
    outs = []
    for perm in itertools.permutations([5,6,7,8,9]):
        outs.append(asyncio.run(go(p, perm)))
    print(outs)
    print(max(outs))

if __name__ == '__main__':
    sys.exit(main(sys.argv))

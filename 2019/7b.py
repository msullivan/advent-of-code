#!/usr/bin/env python3

import sys
import re
import time
import itertools


def run(p, ip, input, output):
    if ip == -1:
        return -1

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
            if not input:
                print("yielding at", ip, id(input))
                return ip
            print("got input", ip, id(input), input[0])
            p[p[ip+1]] = input.pop(0)
            ip += 2
        elif instr % 100 == 4:
            print("writing to", ip, id(output))
            output.append(read(1))
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


    return -1

def main(args):
    data = [s.strip() for s in sys.stdin]
    p = [int(x) for x in data[0].split(",")]
    op = list(p)
    outs = []
    for perm in itertools.permutations([5,6,7,8,9]):
        code = [list(p) for x in perm]
        inputs = [[x] for x in perm]
        outputs = [None] * 5
        for i in range(5):
            outputs[(i-1)%5] = inputs[i]
        inputs[0].append(0)
        print(inputs)

        ips = [0 for x in range(5)]

        while ips != [-1] * 5:
            print(inputs, outputs)
            for i in range(5):
                ips[i] = run(code[i], ips[i], inputs[i], outputs[i])
        outs.append(outputs[-1][0])
    print(outs)
    print(max(outs))

if __name__ == '__main__':
    sys.exit(main(sys.argv))

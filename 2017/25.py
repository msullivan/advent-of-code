#!/usr/bin/env python3

import sys
from collections import defaultdict

# This is the second version.
# The original version I wrote for leaderboard contention I just
# manually transcribed the turning machine transition function
# into a dictionary, of course.
# That was the obviously faster thing for N=6.
# At N=50 I would have definitely been better parsing it. At N=20
# I am not sure which would be better but I would have lost a bunch
# of time waffling about it.

def parse_thing(data):
    dir = -1 if data[1] == "left" else +1
    return (int(data[0]), dir, data[2])

def parse(data):
    machine = {}
    odata = [s.replace(".", "").replace(":", "").split(" ") for s in data]
    data = [x[-1] for x in odata]

    start = data[0]
    steps = int(odata[1][-2])
    i = 3
    while i < len(data):
        state = data[i]
        machine[state] = (parse_thing(data[i+2:i+5]),
                          parse_thing(data[i+6:i+9]))
        print(machine)
        i += 10
    return (start, steps, machine)

def main(args):
    data = [s.strip() for s in sys.stdin]

    tape = defaultdict(int)
    state, size, machine = parse(data)
    pos = 0
    for i in range(size):
        val, dir, new = machine[state][tape[pos]]
        tape[pos] = val
        pos += dir
        state = new
    print(len([x for x in tape.values() if x == 1]))



if __name__ == '__main__':
    sys.exit(main(sys.argv))

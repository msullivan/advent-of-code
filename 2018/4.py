#!/usr/bin/env python3

from collections import defaultdict
import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'\d+', s)]

def main(args):
    data = [s.strip() for s in sys.stdin]
    data = sorted([(extract(s), s.split(" ")[3]) for s in data])
    guard = -1
    i = 0

    sleep_time = defaultdict(int)
    most_common = defaultdict(lambda: defaultdict(int))

    while i < len(data):
        times, thing = data[i]
        guard = times[-1]
        i += 1
        while True:
            if i >= len(data) or len(data[i][0]) == 6:
                break

            start = data[i][0][4]
            stop = data[i+1][0][4]
            sleep_time[guard] += (stop - start)
            for j in range(start, stop):
                most_common[guard][j] += 1
            i += 2

    amount, sleepy = max(((v, k) for k, v in sleep_time.items()))
    amount, minute = max(((v, k) for k, v in most_common[sleepy].items()))
    print(minute * sleepy)

    amount, sleepy, minute = max((v, guard, minute) for guard, d in most_common.items() for minute, v in d.items())
    print(minute * sleepy)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

#!/usr/bin/env python3

import sys
from collections import Counter
import re
import numpy as np


def extract(s, pos=False):
    p = '' if pos else '-?'
    return [int(x) for x in re.findall(fr'{p}\d+', s)]


def main(args):
    # Make a transformation matrix
    mat = np.zeros((9,9), dtype=int)
    for i in range(8):
        mat[i+1,i] = 1
    mat[0,8] = 1
    mat[0,6] = 1
    print(mat)

    cs = Counter(extract(sys.stdin.read()))
    fish = np.array([cs[i] for i in range(9)])

    print(sum(fish @ np.linalg.matrix_power(mat, 80)))
    print(sum(fish @ np.linalg.matrix_power(mat, 256)))

if __name__ == '__main__':
    sys.exit(main(sys.argv))

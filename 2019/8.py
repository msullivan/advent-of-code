#!/usr/bin/env python3

import sys
import time
import math

HEIGHT=6
WIDTH=25


def main(args):
    data = [s.strip() for s in sys.stdin][0]
    layers = []
    i = 0
    while i < len(data):
        layers.append(data[i:i+HEIGHT*WIDTH])
        i += HEIGHT*WIDTH

    # Part 1
    m = min(x.count('0') for x in layers)
    layer = next(x for x in layers if x.count('0') == m)
    print(layer.count('1') * layer.count('2'))

    # Part 2
    image = []
    for i in range(len(layers[0])):
        cur = '2'
        for layer in layers:
            if cur == '2':
                cur = layer[i]
        image.append(cur)

    i = 0
    while i < len(image):
        print(''.join(image[i:i+WIDTH]).replace('0', ' '))
        i += WIDTH


if __name__ == '__main__':
    main(sys.argv)

#!/usr/bin/env python3

import sys

def main(args):
    data = [s.rstrip('\n') for s in sys.stdin][0]

    for i in range(len(data)):
        if len(set(data[i:i+4])) == 4:
            print(i+4)
            break

if __name__ == '__main__':
    main(sys.argv)

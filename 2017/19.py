#!/usr/bin/env python3

import sys
from collections import defaultdict
def flip(s): return "|" if s == "-" else "-"


def look(grid, y, x):
    if x < 0 or y < 0: return ' '
    if y >= len(grid): return ' '
    if y >= len(grid[y]): return ' '
    return grid[y][x]

def main(args):
    grid = [s[:-1] for s in sys.stdin]

    y = 0
    x = grid[0].index('|')

    dx,dy = (0,1)
    char = '|'

    g = grid

    path = []
    i = 0
    while True:
        i += 1
        if look(g, y, x) == ' ':
            break
        if look(g, y, x).isalpha():
            path.append(look(g, y, x))
        if look(g, y, x) == '+':
            ndx,ndy = dy,dx
            char = flip(char)
            if look(g, y+ndy, x+ndx) != ' ':
                dx,dy = ndx,ndy
            elif look(g, y-ndy, x-ndx) != ' ':
                dx,dy = -ndx,-ndy
            else:
                break
        x += dx
        y += dy

    print("".join(path))
    print(i-1)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

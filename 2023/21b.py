#!/usr/bin/env python3

import sys

def vadd(v1, v2):
    return tuple([x + y for x, y in zip(v1, v2)])


UP, RIGHT, DOWN, LEFT = VDIRS = (0, -1), (1, 0), (0, 1), (-1, 0),

def draw(painted, fuck, lu):
    minx = min(x for x, y in painted)
    miny = min(y for x, y in painted)
    maxx = max(x for x, y in painted)
    maxy = max(y for x, y in painted)

    l = ""
    maxx *= 1
    maxy *= 1
    # XXX: add reversed if needed
    for y in list((range(miny, maxy+1))):
        for x in range(minx, maxx+1):
            # x += 131
            # y += 131
            if (x,y) in fuck:
                l += "O"
            else:
                # l += painted.get((x,y), ".")
                l += lu((x,y))
        l += "\n"
    print(l)


def amod(x, n):
    return ((x % n) + n) % n


def run(data, m, start, open=True):

    def lu(p):
        x, y = p
        x = amod(x, len(data[0]))
        y = amod(y, len(data))
        return m[x, y]

    cnt = []
    spots = {start}
    back = None

    nums = []
    i = 0
    while len(nums) < 3:
        if (i - 65) % 131 == 0:
            print(i, len(spots))
            nums.append(len(spots))
        i += 1

        cnt.append(len(spots))
        # draw(m, spots, lu)
        nxt = set()
        for n in spots:
            for dnbr in VDIRS:
                nbr = vadd(n, dnbr)
                if lu(nbr) == '.' and (open or nbr in m):
                    nxt.add(nbr)
        # print(len(cnt)-1, len(nxt), len(nxt) - len(spots))
        if nxt == back:
            break
        back = spots
        spots = nxt

    return nums
    # return cnt

# https://stackoverflow.com/questions/19175037/determine-a-b-c-of-quadratic-equation-using-data-points
def coefficient(x,y):
    x_1 = x[0]
    x_2 = x[1]
    x_3 = x[2]
    y_1 = y[0]
    y_2 = y[1]
    y_3 = y[2]

    a = y_1/((x_1-x_2)*(x_1-x_3)) + y_2/((x_2-x_1)*(x_2-x_3)) + y_3/((x_3-x_1)*(x_3-x_2))

    b = (-y_1*(x_2+x_3)/((x_1-x_2)*(x_1-x_3))
         -y_2*(x_1+x_3)/((x_2-x_1)*(x_2-x_3))
         -y_3*(x_1+x_2)/((x_3-x_1)*(x_3-x_2)))

    c = (y_1*x_2*x_3/((x_1-x_2)*(x_1-x_3))
        +y_2*x_1*x_3/((x_2-x_1)*(x_2-x_3))
        +y_3*x_1*x_2/((x_3-x_1)*(x_3-x_2)))

    return a,b,c

def main(args):
    file = open(args[1]) if len(args) > 1 else sys.stdin
    # data = [x.rstrip('\n').split('\n') for x in file.read().split('\n\n')]
     # data = [int(s.rstrip('\n')) for s in file]
    data = [s.rstrip('\n') for s in file]

    m = {}
    for y, l in enumerate(data):
        for x, c in enumerate(l):
            if c == 'S':
                start = (x,y)
                c = '.'
            m[x, y] = c

    print(len(data[0]), len(data))
    print(start)

    N = len(data)
    S = start[0]

    # print(S)
    things = run(data, m, start)
    # print(cnts)
    # print(len(cnts))

    # things = [3703, 32712, 90559]
    a, b, c = coefficient([0,1,2], things)
    print(a,b,c)
    x = 3

    x = (26501365 - S) / N
    print(x)

    y = a*x*x + b*x + c
    print(int(y))

    # fcnts = []
    # flat = [(0, S), (N-1, S), (S, 0), (S, N-1)]
    # for s in flat:
    #     cnts = run(data, m, s)
    #     fcnts.append(cnts)
    #     print(cnts)
    #     print(len(cnts))

    # print()
    # dcnts = []
    # diag = [(0, 0), (N-1, 0), (0, N-1), (N-1, N-1)]
    # for s in diag:
    #     cnts = run(data, m, s)
    #     dcnts.append(cnts)
    #     print(cnts)
    #     print(len(cnts))


if __name__ == '__main__':
    main(sys.argv)

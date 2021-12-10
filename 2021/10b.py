#!/usr/bin/env python3

import sys


def main(args):
    data = [s.strip() for s in sys.stdin]

    LS = "([{<"
    RS = ")]}>"
    m = {k: v for k, v in zip(LS, RS)}

    scores = [3, 57, 1197, 25137]

    incomplete = []
    score = 0
    score2 = []
    for line in data:
        stack = []
        busted = False
        for i, c in enumerate(line):
            if c in LS:
                stack.append(c)
            else:
                l = stack.pop()
                if m[l] != c:
                    busted = True
                    break
        if busted:
            score += scores[RS.index(c)]
        else:
            lscore = 0
            for c in reversed(stack):
                lscore *= 5
                r = RS.index(m[c]) + 1
                lscore += r
            score2 += [lscore]


    print(score)
    print(score2[len(score2)//2])

if __name__ == '__main__':
    main(sys.argv)

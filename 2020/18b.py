#!/usr/bin/env python3

import sys
import re

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]


# seriously this is so bad.
def ev(s):
    s = s.replace(" ", "")
    s = list(reversed(s))

    while len(s) > 1:
        print("stack", s)
        if s[-1] == '(':
            cnt = 1
            i = len(s)-2
            cnt = 1
            while cnt > 0:
                if s[i] == '(': cnt += 1
                if s[i] == ')': cnt -= 1
                i -= 1

            i += 1

            shit = s[i:]
            s = s[:i]
            n = ev(''.join(reversed(shit))[1:-1])
            s = s + [n]
        elif s[-3] == '(':
            i = len(s)-4
            a = s.pop()
            b = s.pop()

            cnt = 1
            while cnt > 0:
                if s[i] == '(': cnt += 1
                if s[i] == ')': cnt -= 1
                i -= 1
            i += 1

            shit = s[i:]
            s = s[:i]
            n = ev(''.join(reversed(shit))[1:-1])
            s = s + [n, b, a]


        elif s[-2] == '+':
            n = int(s[-3]) + int(s[-1])
            s.pop()
            s.pop()
            s.pop()
            s += [str(n)]
        elif s[-2] == '*':
            n = int(s[-3]) * int(s[-1])
            s.pop()
            s.pop()
            s.pop()
            s += [str(n)]

    return s[-1]


def atom(s):
    if s[-1] == '(':
        s.pop()
        x = expr(s)
        s.pop()
        return x
    a = s.pop()
    return int(a)

def term(s):
    n = atom(s)
    while s and s[-1] == '+':
        s.pop()
        n += atom(s)
    return n

def expr(s):
    n = term(s)
    while s and s[-1] == '*':
        s.pop()
        n *= term(s)
    return n


def main(args):
    # data = [x.split('\n') for x in sys.stdin.read().split('\n\n')]
    data = [s.strip() for s in sys.stdin]

    sum = 0
    for x in data:
        sum += int(ev(x))

    print(sum)

    sum = 0
    for x in data:
        x = x.replace(" ", "")
        x = list(reversed(x))
        sum += int(expr(x))

    print(sum)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

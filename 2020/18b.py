#!/usr/bin/env python3

import sys

# This has is a version of my p2 solution backported to p1. My p1 one
# is in 18a.py and is some nasty stack stuff somehow still mixed with
# recursion.
#
# I'm kind of embarassed that I peaked at the wikipedia article for
# recursive descent parser for this. I have a phd in this stuff.

def p1_atom(s):
    if s[-1] == '(':
        s.pop()
        x = p1_expr(s)
        s.pop()
        return x
    a = s.pop()
    return int(a)

def p1_expr(s):
    n = p1_atom(s)
    while True:
        if s and s[-1] == '+':
            s.pop()
            n += p1_atom(s)
        elif s and s[-1] == '*':
            s.pop()
            n *= p1_atom(s)
        else:
            break
    return n

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
    data = [s.strip() for s in sys.stdin]

    sum = 0
    for x in data:
        x = list(reversed(x.replace(" ", "")))
        sum += int(p1_expr(x))

    print(sum)

    sum = 0
    for x in data:
        x = list(reversed(x.replace(" ", "")))
        sum += int(expr(x))

    print(sum)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

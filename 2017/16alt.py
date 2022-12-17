#!/usr/bin/env python3

"""
An alternate solve of 16 part 2 based on decomposing and
exponentiating permutations.

The insight here is that Spin and Exchange are permutations and can be
reordered at will and that Partner, while not a permutation on the
order of the dancers, commutes with the permutation also (it's just a
relabelling of the elements).

This means that we can split up the problem, and do all of the
Spin/Exchange operations and then all of the Partner operations.

Moreover, Partner *is* actually a permutation on the "index sequence".
If we define the index sequence of a sequence of dancers to be:
  for each letter, in order, the index of that letter in the dancer sequence
then Partner just swaps the indexes at its two letters.

Thus, we can decompose the dance instructions into:
 * A permutation of the values defined by the S and X operations
 * A permutation of the indexes defined by the P operations

These permutations can be represented as sequences of ints, and
applied to other sequences. Applying a permutation to a another
permutation computes a composition. We can then compose it a billion
times by using exponentiation by squaring.

"""

import sys

def round(things, data):
    for move in data:
        if move[0] == 's':
            amt = int(move[1:])
            things = things[-amt:] + things[:-amt]
        elif move[0] == 'x':
            a,b = map(int, move[1:].split("/"))
            things[a], things[b] = things[b], things[a]
        else:
            x, y = move[1], move[3]
            a = things.index(x)
            b = things.index(y)
            things[a], things[b] = things[b], things[a]
    return things

def apply(xs, perm):
    return [xs[perm[i]] for i in range(len(xs))]

def pow(xs, n):
    if n == 0:
        return list(range(len(xs)))
    sub = pow(xs, n // 2)
    sub = apply(sub, sub)
    if n % 2 == 1:
        sub = apply(xs, sub)
    return sub

def indexes(letters):
    return [letters.index(chr(ord('a')+i)) for i in range(len(letters))]

def main(args):
    data = [s.strip() for s in sys.stdin]
    data = data[0].split(",")
    Xdata = [x for x in data if x[0] != 'p']
    Pdata = [x for x in data if x[0] == 'p']

    X = round(list(range(16)), Xdata)
    things = [chr(ord('a')+i) for i in range(16)]
    P = indexes(round(list(things), Pdata))

    things = apply(things, pow(X, 1000000000))
    idxs = apply(indexes(things), pow(P, 1000000000))
    letters = [chr(ord('a')+idxs.index(i)) for i in range(16)]
    print(''.join(letters))

if __name__ == '__main__':
    sys.exit(main(sys.argv))

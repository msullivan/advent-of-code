#!/usr/bin/env python3

# For the original solution, I made this take a command line arugment
# for the attack power and I manually binary searched

from collections import deque
import sys
from dataclasses import dataclass

@dataclass(eq=False)
class Noob:
    type: str
    loc: object
    hp: int = 200
    atk: int = 3

INF = float('inf')

dirs = [(-1, 0), (0, -1), (0, 1), (1, 0)]

def other(s): return 'G' if s == 'E' else 'E'

def distances(map, y, x):
    d = deque([(y, x)])
    dists = [[INF for i in range(len(map[0]))] for j in range(len(map))]
    dists[y][x] = 0
    while d:
        y, x = d.popleft()
        for i, j in dirs:
            if map[y+i][x+j] == '.' and dists[y+i][x+j] == INF:
                dists[y+i][x+j] = dists[y][x] + 1
                d.append((y+i, x+j))
    return dists

def get_targets(map, noob, asdf='.'):
    y, x = noob.loc
    return [(y+i, x+j) for i, j in dirs if map[y+i][x+j] == asdf]

def go(data, power):
    map = data = [list(x) for x in data]

    elves = 0
    # y, X!
    noobs = set()
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] in 'GE':
                noob = Noob(data[y][x], (y, x))
                if noob.type == 'E':
                    noob.atk = power
                    elves += 1
                noobs.add(noob)

    print(data)
    print(noobs)

    rounds = 0
    done = False

    while True:
        print('\n'.join(''.join(s) for s in data))

        order = sorted(noobs, key=lambda x: x.loc)

        for noob in order:
            if noob.hp <= 0: continue
            if all(n.type == noob.type for n in noobs):
                done = True
                print("DONE!", noobs)
                print('\n'.join(''.join(s) for s in data))
                break

            y, x = noob.loc
            targets = []
            for dude in noobs:
                if dude.type == other(noob.type):
                    targets.extend(get_targets(map, dude))

            if not any(data[y+i][x+j] == other(noob.type) for i, j in dirs):

                if targets:
                    # try moving!
                    dists = distances(data, y, x)
                    dist, target = min((dists[dy][dx], (dy, dx)) for dy, dx in targets)

                    if dist < INF:
                        # Search back from the target to pick the first
                        # place to go back to.
                        rdists = distances(data, target[0], target[1])
                        for i, j in dirs:
                            if rdists[y+i][x+j] == dist-1:
                                next = y+i, x+j
                                break

                        ny, nx = next
                        map[ny][nx] = noob.type
                        map[y][x] = '.'
                        noob.loc = next
                        y, x = next

            # OK NOW WE ATTACK???
            vulnerable = get_targets(map, noob, other(noob.type))
            really_vulnerable = [x for x in noobs if x.loc in vulnerable]
            if really_vulnerable:
                fucked = min(really_vulnerable, key=lambda x: (x.hp, x.loc))
                fucked.hp -= noob.atk
                if fucked.hp <= 0:
                    map[fucked.loc[0]][fucked.loc[1]] = '.'
                    noobs.remove(fucked)

        if done:
            break

        rounds += 1

    print('round', rounds)
    hp = sum(x.hp for x in noobs)
    print('hp', hp)
    score = rounds * hp
    passed = len([x for x in noobs if x.type == 'E']) == elves
    print(score)
    print(passed)
    return score, passed


def main(args):
    data = [list(s.strip()) for s in sys.stdin]

    part1, _ = go(data, 3)

    # Really we should binary search but whatever
    power = 3
    passed = False
    while not passed:
        power += 1
        score, passed = go(data, power)

    print()
    print(part1)
    print(score)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

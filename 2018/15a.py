#!/usr/bin/env python3

from collections import defaultdict, deque
import sys
sys.excepthook = sys.__excepthook__  # I am so mad about ubuntu's excepthook
import re
from dataclasses import dataclass

@dataclass(eq=False)
class Noob:
    type: str
    loc: object
    hp: int = 200
    atk: int = 3

def extract(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

dirs = [(-1, 0), (0, -1), (0, 1), (1, 0)]

def other(s): return 'G' if s == 'E' else 'E'

def distances(map, y, x):
    d = deque([(y, x)])
    dists = [[100000000000 for i in range(len(map[0]))] for j in range(len(map))]
    dists[y][x] = 0
    while d:
        y, x = d.popleft()
        for i, j in dirs:
            if map[y+i][x+j] == '.' and dists[y+i][x+j] == 100000000000:
                dists[y+i][x+j] = dists[y][x] + 1
                d.append((y+i, x+j))
    return dists

def get_targets(map, noob, asdf='.'):
    y, x = noob.loc
    return [(y+i, x+j) for i, j in dirs if map[y+i][x+j] == asdf]

def main(args):
#    data = [extract(s.strip()) for s in sys.stdin]
    data = [list(s.strip()) for s in sys.stdin]
    map = data

    # y, X!
    noobs = set()
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] in 'GE':
                noobs.add(Noob(data[y][x], (y, x)))
#            data[y][x] = '.'
    print(data)
    print(noobs)

    rounds = 0
    done = False

    while True:
        print('\n'.join(''.join(s) for s in data))

        order = sorted(noobs, key=lambda x: x.loc)

        for noob in order:
            attacked = False

            if noob.hp <= 0: continue
#            print('moving!', noob)
            if all(n.type == noob.type for n in noobs):
                done = True
                print("DONE!", noobs)
                print('\n'.join(''.join(s) for s in data))
                break


            y, x = noob.loc
            targets = []
            for dude in noobs:
                if dude.type == other(noob.type):
#                    print(dude)
                    targets.extend(get_targets(map, dude))

            if not any(data[y+i][x+j] == other(noob.type) for i, j in dirs ):
#                print(targets)

                if targets:
                    attacked = True

                    # try moving!
                    dists = distances(data, y, x)
                    # print('\n'.join(''.join(s) for s in data))
                    # print()
                    # print('\n'.join(''.join([str(i) if i < 100000000000 else '#' for i in s]) for s in dists))
                    dist, target = min((dists[dy][dx], (dy, dx)) for dy, dx in targets)
#                    print(dist, target)

                    if dist < 100000000000:


                    # OK THIS SUCKS
                        fuck = []
                        for i, j in dirs:
                            if map[y+i][x+j] == '.':
                                dists = distances(data, y+i, x+j)
                                # print('\n'.join(''.join([str(i) if i < 100000000000 else '#' for i in s]) for s in dists))
                                # print()
                                fuck.append((dists[target[0]][target[1]], (y+i, x+j)))
    #                    print("FUCK", fuck)
                        if fuck and min(fuck)[0] < 100000000000:
                            dist, next = min(fuck)
    #                        print(dist, next)
                            ny, nx = next
                            map[ny][nx] = noob.type
                            map[y][x] = '.'
                            noob.loc = next
                            y, x = next

            # OK NOW WE ATTACK???
            vulnerable = get_targets(map, noob, other(noob.type))
            really_vulnerable = [x for x in noobs if x.loc in vulnerable]
            if really_vulnerable:
                attacked = True
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
    print(rounds * hp)


#            return



if __name__ == '__main__':
    sys.exit(main(sys.argv))

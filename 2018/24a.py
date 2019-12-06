#!/usr/bin/env python3.7

from collections import defaultdict, deque
import sys
import re
import time
from dataclasses import dataclass, field
from typing import Set


def extract(s):
    return [int(x) for x in re.findall(r'\d+', s)]


@dataclass
class Group:
    units: int
    hp: int
    damage: int
    init: int
    damage_type: str
    immune: Set[str]
    weak: Set[str]

    def __hash__(self):
        return id(self)

    @staticmethod
    def from_str(s):
        units, hp, damage, init = extract(s)
        parts = s.split(" ")
        damage_type = parts[parts.index("damage") - 1]
        immune = set()
        weak = set()
        if "(" in s:
            rest = s.split("(")[1].split(")")[0].split("; ")
            for half in rest:
                parts = half.split(" ")
                valence = weak if parts[0] == "weak" else immune
                for typ in parts[2:]:
                    valence.add(typ.strip(","))

        return Group(units, hp, damage, init, damage_type, immune, weak)

    @property
    def effective_power(self):
        return self.units * self.damage

    def damage_estimate(self, target):
        if self.damage_type in target.immune:
            return 0
        elif self.damage_type in target.weak:
            return self.effective_power * 2
        else:
            return self.effective_power

    def ranking(self, target):
        return (self.damage_estimate(target), target.effective_power, target.init)

    def attack(self, target):
        dead = self.damage_estimate(target) // target.hp
        target.units = max(0, target.units - dead)

def select_targets(attack, defense):
    available = set(defense)
    targets = {}

    for x in reversed(sorted(attack, key=lambda x: (x.effective_power, x.init))):
        if not available:
            continue
        target = max(available, key=x.ranking)
        if x.damage_estimate(target):
            targets[x] = target
            available.remove(target)

    return targets

def main(args):
    data = [s.strip() for s in sys.stdin]

    immune = []
    infection = []

    cur = immune
    for x in data:
        if "units" in x:
            cur.append(Group.from_str(x))
        if x == "Infection:":
            cur = infection

    while immune and infection:
        fights = select_targets(immune, infection)
        fights.update(select_targets(infection, immune))

        for unit in reversed(sorted(fights.keys(), key=lambda x: x.init)):
            if unit.units:
                unit.attack(fights[unit])

        immune = [x for x in immune if x.units]
        infection = [x for x in infection if x.units]

    print(sum(x.units for x in immune+infection))


if __name__ == '__main__':
    sys.exit(main(sys.argv))

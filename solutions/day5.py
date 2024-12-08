from utils.utils import split_groups
from collections import deque
from collections import defaultdict
from math import inf


def find_order(root, mapping):
    current = {root}
    sequence = {}
    i = -1
    while current:
        i += 1
        new = set()
        for k in current:
            if sequence.get(k) is None:
                sequence[k] = i
                new.update(mapping[k])
        current = new
    #sequence.pop(root)
    return sequence


ordering, updates = split_groups("inputs/day5.txt")
updates = [list(map(int, l.split(","))) for l in updates.splitlines()]
lines = ordering.splitlines()
before, after = list(zip(*(map(int, l.split("|")) for l in lines)))

mapping = defaultdict(set)
for k, v in zip(before,after):
    mapping[k].add(v)


sequences = {}
part1 = 0

for group in updates:
    # FOr part 2, put sequence in correct order from rules instead of brute-forcing
    orderings = {g : find_order(g, mapping) for g in group}
    counts = [sum(s.get(g) is not None  for s in orderings.values()) for g in group]

    # Check if priority order correct
    print(counts)
    if counts == sorted(counts):
        part1 += group[len(group) // 2]


print(part1)

from utils.utils import split_groups
from collections import deque
from operator import add
from functools import reduce
from collections import defaultdict
from itertools import permutations
from math import inf



def find_after(possible, before, after, mapping):
    seen = {possible}
    before = set(before)
    after = set(after)
    queue = [possible]

    while queue and after:
        current = queue.pop()
        new = mapping[current]
        for n in new:
            if n in after:
                after.remove(n)
            elif n  in before:
                return False
            elif n not in seen:
                seen.add(n)
                queue.append(n)
    return not len(after)

def count_children(start, mapping):
    queue = [ start ]
    seen = set()

    while queue:
        current = queue.pop()
        seen.add(current)
        print({k for k in mapping[current] if k in seen})
        new = mapping[current]
        queue.extend(new)
    return seen - { start }



def verify_group(group, mapping):
    return [ find_after(g, group[:i], group[i+1:], mapping) for i, g in enumerate(group) ]

def reorder(group_map):
    ordering = []
    targets = set(group_map.keys())
    all_children = reduce(set.union, group_map.values())
    while targets:
        for number in targets:
            children = group_map[number]
            this_children = all_children - children
            if number not in this_children:
                targets.remove(number)
                ordering.append(number)
                break
    return ordering

# TODO: Topological sort
def bubble_sort(ordering, mapping):
    # Swap only problem groups, assuming others in correct order
    # E.g., try each as first until whole group to that index correct
    # Or would just bubble sort of bad indices work
    n = len(ordering)
    while True:
        swapped = False
        # Descending order of priority
        for i in range(1, n):
            this = ordering[i]
            last = ordering[i-1]
            if is_child(last, this, mapping):
                ordering[i], ordering[i-1] = ordering[i-1], ordering[i]
                swapped = True
        if not swapped:
            return ordering

def is_child(parent, child, mapping):
    queue = [parent]
    seen = set()
    while queue:
        current = queue.pop()
        if current == child:
            return True
        seen.add(current)
        new = mapping[current] - seen
        queue.extend(new)
    return False
            
        
ordering, updates = split_groups("inputs/day5.txt")
updates = [list(map(int, l.split(","))) for l in updates.splitlines()]
lines = ordering.splitlines()
before, after = list(zip(*(map(int, l.split("|")) for l in lines)))

mapping = defaultdict(set)
for k, v in zip(before,after):
    mapping[k].add(v)


part1 = part2 =  0

# Trim mapping to numbers involved in each rule group
for group in updates:
    this_mapping = defaultdict(set)
    this_mapping.update({k: v & set(group) for k, v in mapping.items()})
    middle = len(group) // 2
    result = False
    result =  [is_child(group[i], group[i+1], this_mapping) for i in range(len(group) - 1)] + [ True ]
    if all(result):
        part1 += group[middle]
    else:
    #result = verify_group(group, this_mapping)
        # Too high on test, too low on actual
        #as if two consecutive elements were not ordered properly, you would just swap them and continue until you had no swaps. No need for graphs at all, just a map was enough
        #counts = {g: count_children(g, mapping) for g in group}
        problems = [ group[i] for i, el in enumerate(result) if not el ]
        problems_mapping = {k : v | set(problems) for k, v in this_mapping.items()}
        current_fault =  result.index(False)
        reordered = bubble_sort(group, this_mapping)
        part2 += reordered[middle]
        # while problems:
        #     print(problems)
        #     for p in problems: 
        #         if is_child(group[current_fault - 1], p, this_mapping):
        #             group[current_fault] = p
        #             problems.remove(p)
        #             break
        #
        # counts = {k : count_children(k, mapping) for k in group}
        # order = bubble_sort(problems, counts)
        # print(order)
        # for i in range(len(group)):
        #     if not result[i]:
        #         group[i] = order.pop(0)
        # assert verify_group(group, this_mapping)
        #part2 += group[middle]

# 6083 too low
print(part1)
print(part2)

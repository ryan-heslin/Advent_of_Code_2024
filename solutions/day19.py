from utils.utils import split_groups, count_dict
from collections import defaultdict
import bisect


def arrange_towels(possible, towels):
    # Like 2023 day 12?
    def rec(col, index):
        nonlocal possible
        if index == len(col) - 1:
            return True
        for sequence in possible:
            new = index + len(sequence)
            if col[index:new] == sequence:
                result = rec(col, new)
                if result:
                    bisect.insort(possible, col[:new], key=len)
                    return result
        else:
            return False

    return sum(rec(t, 0) for t in towels)


def count_options(towel, possible):
    dp = count_dict()
    # Each dp index represents before char, so 0 i
    dp[0] = 1
    n = len(towel)
    for i in range(n):
        for p in possible:
            stop = i + len(p)
            if stop > n:
                break
            new = towel[i:stop]
            if new == p:
                dp[stop] += dp[i]
    return dp[n]


# Take towel
# For each length of colors
# Count matches
# Repeat on remainder of string
# Recurse on rest of string
# length : {patterns} dict, then try perms of length?

colors, towels = split_groups("inputs/day19.txt")
colors = colors.split(", ")
towels = towels.rstrip("\n").split("\n")

possible = sorted(colors, key=len)
values = [count_options(t, possible) for t in towels]
part1 = sum(map(bool, values))
part2 = sum(values)
print(part1)
print(part2)

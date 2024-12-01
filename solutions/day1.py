import heapq
from collections import defaultdict
from utils.utils import split_lines
from utils.utils import count_dict

data = split_lines("inputs/day1.txt")
part1 = 0

left = []
right = []
heapq.heapify(left)
heapq.heapify(right)

for el in data:
    l, r= el.split("   ")
    heapq.heappush(left, int(l))
    heapq.heappush(right, int(r))

n = len(left)

left_map =  count_dict()
right_map =  count_dict()

for _ in range(n):
    l = heapq.heappop(left)
    r = heapq.heappop(right)
    part1 += abs(l - r)
    left_map[l] += 1
    right_map[r] += 1

part2 = sum(el * count * right_map[el] for el, count in left_map.items())
print(part1)
print(part2)

# TODO

# 1. Read into heapqs
# Solve part 1 by reading from each queue
# Read into counter defaultdics
# Iterate over left dict to solve part 2

# i = split_lines("inputs/day1.txt")
#
# part1 = part2 = 0
# l1 = []
# l2 = []
# for l in i:
#     l1 += [ int(l.split("   ")[0]) ]
#     l2 += [ int(l.split("   ")[1]) ]
#
# l1.sort()
# l2.sort()
# for ix in range(len(l1)):
#     part1 += abs(l1[ix] - l2[ix])
#     part2 += (l1[ix] * sum(k == l1[ix] for k in l2)) 
#
#
# print(part1)
# print(part2)

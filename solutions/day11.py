from utils.utils import scan_ints, count_dict
from math import log10, floor
from functools import cache
from collections import defaultdict, Counter

@cache
def process_number(num):
        if  num == 0:
            result = (1,)
        elif (digits := n_digits(num)) % 2 == 0:
            result = split(num, digits // 2)
        else:
            result = (num * 2024,)
        return result

def n_digits(x):
    return floor(log10(x)) + 1


def split(x, size):
    divisor = 10**size
    return divmod(x, divisor)


def iterate(numbers, n):
    for _ in range(n):
        new = defaultdict(lambda: 0)
        for num, count in numbers.items():
            result = process_number(num)
            for n in result:
               new[n] += count 
        numbers = new
    return numbers

with open("inputs/day11.txt") as f:
    numbers = list(scan_ints(f.read().rstrip("\n")))
count = Counter(numbers)
part1_iterations = 25
part2_iterations = 75
numbers = count_dict()
numbers.update(count)
result = iterate(numbers, 25)
print(sum(result.values()))
result = iterate(result, part2_iterations - part1_iterations)
print(sum(result.values()))


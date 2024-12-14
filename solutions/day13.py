import re
from math import ceil
from utils.utils import split_groups, list_map


def parse(lines):
    numbers = list_map(re.findall(r"\d+", lines), int)
    return [[[numbers[0], numbers[2]], [numbers[1], numbers[3]]], numbers[4:]] 


def determinant(A):
    return (A[0][0] * A[1][1]) - (A[0][1] * A[1][0])


def check(solution, costs):
    result = 0
    for s, c in zip(solution, costs):
        if s < 0 or ceil(s) != s:
            return 0
        result += s * c
    return result

def solve_matrix(A, b):
    inverse = [[A[1][1], -A[0][1]], [-A[1][0], A[0][0]]]
    det = determinant(A)
    rhs = [
        (inverse[0][0] * b[0]) + (inverse[0][1] * b[1]),
        (inverse[1][0] * b[0]) + (inverse[1][1] * b[1]),
    ]
    return  [rhs[0] / det, rhs[1] / det]

def solve(data, prices):
    A, b = data
    first = solve_matrix(A,b)
    second = solve_matrix(A, [x + 10000000000000 for x in b])

    return [check(first, prices), check(second, prices)]


text = split_groups("inputs/day13.txt")
parsed = list_map(text, parse)
prices = [3, 1]
parts = list(zip(*[ solve(d, prices)  for d in parsed]))
part1 = int(sum(parts[0]))
part2 = int(sum(parts[1]))
print(part1)
print(part2)

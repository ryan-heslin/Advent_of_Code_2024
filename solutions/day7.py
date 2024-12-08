from utils.utils import split_lines
from operator import add
from operator import mul
from math import floor, log10


def concat(lhs, rhs):
    return lhs * 10 ** (floor(log10(rhs)) + 1) + rhs


def parse_line(l):
    parts = l.split(": ")
    return int(parts[0]), list(map(int, parts[1].split(" ")))


def check_solution(target, rhs, operations, init=0):
    if init > target:
        return 0
    if rhs == []:
        if init == target:
            return target
        else:
            return 0
    for op in operations:
        solution = check_solution(target, rhs[1:],operations, op(init, rhs[0]) )
        if solution > 0:
            break
    return solution

# TODO: Optimize by working backwards, since  last operation can be deduced, then second-to-last, etc.

inputs = split_lines("inputs/day7.txt")
targets, operands = list(zip(*map(parse_line, inputs)))
operations = [add, mul]
part1 = sum(check_solution(t, o, operations) for t, o in zip(targets, operands))
print(part1)
operations.append(concat)
part2 = sum(check_solution(t, o, operations) for t, o in zip(targets, operands))
print(part2)

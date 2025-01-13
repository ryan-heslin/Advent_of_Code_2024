import re
from math import inf
from utils.utils import split_groups
from functools import reduce
from operator import add


# 8 ** n intervals
def check_intervals(code, index, lower, upper):
    target = code[index]
    interval = 8 ** index
    # Closed on left, open on right
    # Like Dijkstra intended
    return [
        (i, i + interval)
        for i in range(lower, upper + 1, interval)
        if try_value(code, i, index)[index] == target
    ]


def solve(code):
    n= len(code)
    lower = 8 ** (n - 1)
    upper = 8 ** n
    intervals = [[lower, upper]]
    index = n -1

    while intervals[0][1] - intervals[0][0] > 1:
        intervals = reduce(
            add,
            (
                check_intervals(code=code, index=index, lower=i[0], upper=i[1])
                for i in intervals
            ),
        )
        index -= 1
    assert try_value(code, intervals[0][0], inf) == code
    return intervals[0][0]


def try_value(code, value, index):
    prog = Program(code, {"A": value, "B": 0, "C": 0}, index)
    prog.run()
    return prog.out


def parse(registers, program):
    registers = dict(zip(("A", "B", "C"), map(int, re.findall(r"-?\d+", registers))))
    program = list(map(int, re.findall(r"-?\d+", program)))
    return registers, program


class Program:
    def __init__(self, code, registers, index = inf):
        self.registers = registers
        self.code = code
        self.index = index
        self.halt = len(self.code)
        self.out = []
        self.pointer = self.current = 0
        self.current = self.code[self.pointer]
        self.operand = self.code[self.pointer + 1]
        ops = [
            self._adv,
            self._bxl,
            self._bst,
            self._jnz,
            self._bxc,
            self._out,
            self._bdv,
            self._cdv,
        ]
        self.ops = dict(enumerate(ops))

    def run(self):
        while 0 <= self.pointer < self.halt:
            if len(self.out) == self.index + 1:
                return
            self.current = self.code[self.pointer]
            self.operand = self.code[self.pointer + 1]
            self.ops[self.current]()
            self.pointer += 2

    def _combo(self, op):
        if op < 4:
            return op
        elif op < 7:
            return self.registers[["A", "B", "C"][op - 4]]
        else:
            raise ValueError

    def _adv(self):
        self.registers["A"] //= 2 ** self._combo(self.operand)

    def _bxl(self):
        self.registers["B"] ^= self.operand

    def _bst(self):
        self.registers["B"] = self._combo(self.operand) % 8

    def _jnz(self):
        if self.registers["A"] != 0:
            self.pointer = self.operand
            self.pointer -= 2

    def _bxc(self):
        self.registers["B"] ^= self.registers["C"]

    def _out(self):
        self.out.append(self._combo(self.operand) % 8)

    def _bdv(self):
        self.registers["B"] = self.registers["A"] // (2 ** self._combo(self.operand))

    def _cdv(self):
        self.registers["C"] = self.registers["A"] // (2 ** self._combo(self.operand))


registers, code = split_groups("inputs/day17.txt")
registers, code = parse(registers, code)
program = Program(code, registers)
program.run()
print(",".join(map(str, program.out)))

part2 = solve(code)
print(part2)

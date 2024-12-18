import re
from utils.utils import split_groups
from math import ceil


def try_value(code, value):
    prog = Program(code, {"A": value, "B" : 0, "C" : 0})
    prog.run()
    return prog.out

def binary_left(code, upper, target, fn):
    left = 0
    right = upper

    while left < right:
        mid = (left + right) // 2
        result = fn(try_value(code, mid))

        print(left)
        if result < target:
            left = mid + 1
        else:
            right = mid
    return left

def binary_right(code, upper, target, fn):
    left = 0
    right = upper

    while left < right:
        mid = (left + right) // 2
        result = fn(try_value(code, mid))

        if result > target:
            right = mid
        else:
            left = mid + 1
    return right - 1



def find_bounds(code, start, end, increment):
    target = len(code)
    lower = -1
    new_registers = {"A" : start , "B" : 0 , "C" : 0}
    for i in range(start, end, increment):
        new_registers["A"] = i
        try:
            new = Program(code, new_registers)
            new.run()
            length = len(new.out)
            print(length)
            if lower < 0 and length == target:
                lower = i - increment
            elif length > target:
                upper = i
                return lower, upper
        except:
            continue

def parse(registers, program):
    registers = dict(zip(("A", "B", "C"), map(int, re.findall(r"-?\d+", registers))))
    program = list(map(int, re.findall(r"-?\d+", program)))
    return registers, program


class Program():
    
    def __init__(self, code, registers):
        # jnz increase by value, subtract 2, increment 2 for all
        self.registers = registers
        self.code = code
        self.halt = len(self.code)
        self.out = []
        self.pointer = self.current =  0
        self.current = self.code[self.pointer]
        self.operand = self.code[self.pointer + 1]
        ops = [self._adv, self._bxl, self._bst, self._jnz, self._bxc, self._out, self._bdv, self._cdv]
        self.ops = dict(enumerate(ops))

    def run(self):
        while 0 <= self.pointer < self.halt:
            self.current = self.code[self.pointer]
            self.operand = self.code[self.pointer + 1]
            self.ops[self.current]()
            self.pointer += 2

    def _combo(self, op):
        if op < 4:
            return op
        elif op < 7:
            return self.registers[ ["A", "B", "C"][op - 4] ]
        else:
            raise ValueError

    def _adv(self):
        self.registers["A"] //= (2 ** self._combo(self.operand))

    def _bxl(self):
        self.registers["B"] ^= self.operand

    def _bst(self):
        self.registers["B"] = self._combo(self.operand) % 8

    def _jnz(self):
        if self.registers["A"] != 0:
            self.pointer  = self.operand
            self.pointer -= 2

    def _bxc(self):
        self.registers["B"] ^= self.registers["C"]

    def _out(self):
        self.out.append(self._combo(self.operand) % 8)

    def _bdv(self):
        self.registers["B"] = self.registers["A"] // ( 2 ** self._combo(self.operand))

    def _cdv(self):
        self.registers["C"] = self.registers["A"] // (2 ** self._combo(self.operand))

registers, code = split_groups("inputs/day17.txt")
registers, code = parse(registers, code)
program = Program(code, registers)
program.run()
print(",".join(map(str, program.out)))


cutoff = 10 ** 18
target = len(code)
lower = binary_left(code, cutoff, target, len)
upper = binary_right(code, cutoff, target, len)
assert len(try_value(code, lower - 1)) < target
assert len(try_value(code, upper + 2)) > target


start = (upper - lower) // 2
last = try_value(code, (upper - lower) // 2)
cycles = [[1] for _ in range(target)]
# nth digit has cycle of n ** 8 
for i in range(start + 1, start + 100000):
    result = try_value(code, i)
    for i in range(target):
        if last[i] == result[i]:
            cycles[i][-1] += 1
        else:
            last[i] = result[i]
            cycles[i].append(1)

result = []
# Grid-search for upper and lower bounds of last needed digit in range
#  8 ** n size?
# Repeat for next-last digit
# I guess resort to brute force eventually
for i in range(lower, upper + 1, (upper + 1 - lower) // 10000):
    result.append(try_value(code, i)[-1])



#lower, upper = find_bounds(code, 10** 12, 10 ** 16, 10 ** 11)
# Either do this sequentially, or binary search to find range of 15-digit outputs

# for i in range(10 ** 12, 10 ** 16, 10 ** 12):
#     new_registers = {"A": i, "B" : 0, "C" : 0}
#     try:
#         new = Program(code, new_registers)
#         new.run()
#         if new.out:
#             print(i, ",".join(map(str, new.out)))
#     except:
#         continue

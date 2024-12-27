import re
from operator import xor, and_, or_
from collections import defaultdict
from utils.utils import split_groups
from itertools import permutations, combinations
from copy import deepcopy

# Based on https://www.reddit.com/r/adventofcode/comments/1hla5ql/2024_day_24_part_2_a_guide_on_the_idea_behind_the/

def parse(inits, rules):
    operators = {"AND": and_, "OR": or_, "XOR": xor}
    # All start without value
    registers = defaultdict(lambda: -1)
    for line in inits.splitlines():
        reg, value = line.split(": ")
        registers[reg] = int(value)

    result = []
    for line in rules.rstrip("\n").splitlines():
        inputs, output = line.split(" -> ")
        lhs, op, rhs = inputs.split(" ")
        op = operators[op]
        result.append({"func": op, "lhs": lhs, "rhs": rhs, "output": output})

    return registers, result


def simulate(registers, rules):
    unfinished = set(range(len(rules)))
    while unfinished:
        old = set(unfinished)
        for i, rule in enumerate(rules):
            if (
                i not in unfinished
                or registers[rule["lhs"]] == -1
                or registers[rule["rhs"]] == -1
            ):
                continue
            registers[rule["output"]] = rule["func"](
                registers[rule["lhs"]], registers[rule["rhs"]]
            )
            unfinished.remove(i)
        # Infinite loop
        if unfinished == old:
            return
    return registers


def calculate(registers, letter="z"):
    zs = sorted((k for k in registers.keys() if k[0] == letter), reverse=True)
    chars = "".join(str(registers[z]) for z in zs)
    return int(chars, base=2)


def all_leading_ones(num):
    # TODO less embarassing
    return re.match("^1+0+$", bin(num)[2:])


def swap_rules(rules, first, second):
    rules[first]["output"], rules[second]["output"] = (
        rules[second]["output"],
        rules[first]["output"],
    )


def find_misaligned(rules, registers, orig_registers):
    last = sorted(r for r in registers if r[0] == "z")[-1]
    inputs = {"x", "y"}
    should_be_xor = []
    should_not_be_xor = []
    for i, r in enumerate(rules):
        if r["output"] != last and r["output"][0] == "z" and r["func"] != xor:
            should_be_xor.append(i)
        elif (
            r["output"][0] != "z"
            and r["lhs"][0] not in inputs
            and r["rhs"][0] not in inputs
            and r["func"] == xor
        ):
            should_not_be_xor.append(i)
    print(should_be_xor)
    print(should_not_be_xor)

    n = len(should_not_be_xor)
    x = y = n_input = 0
    for k, v in orig_registers.items():
        number = int(k[1:])
        n_input = max(n_input, number)
        val = v * (2 ** int(k[1:]))
        if k[0] == "x":
            x += val
        else:
            y += val

    correct = x + y
    print(correct)

    orig = deepcopy(rules)
    for swap in permutations(should_not_be_xor, r=3):
        current = deepcopy(rules)
        for i in range(n):
            first = should_be_xor[i]
            second = swap[i]
            swap_rules(current, first, second)
        result = simulate(orig_registers.copy(), current)
        if result:
            result = calculate(result)
            print(bin(result ^ correct))
            if all_leading_ones(result ^ correct):
                break
            # Reverse swap
        for i in range(n):
            first = should_be_xor[i]
            second = swap[i]
            # swap_rules(rules, second, first)
        assert rules == orig

    rules = current
    known = set(should_be_xor + should_not_be_xor)
    print(sorted(rules[i]["output"] for i in known))
    possible = set(range(len(rules)))
    # TODO
    # DOesn't work when rules are deepcopied each run!?
    for pair in combinations(possible, r=2):
        # if set([ rules[pair[0]]["output"], rules[pair[1]]["output"] ]) == {"hqc", "qcw"}:
        #     breakpoint()
        current = deepcopy(rules)
        swap_rules(current, pair[0], pair[1])
        result = simulate(orig_registers.copy(), current)
        if result:
            result = calculate(result)
            inputs = [
                rules[pair[0]]["lhs"][0],
                rules[pair[0]]["rhs"][0],
                rules[pair[1]]["lhs"][0],
                rules[pair[1]]["rhs"][0],
            ]
            #
            if (
                result == correct
                and sorted(inputs) == ["x", "x", "y", "y"]
                and int(rules[pair[0]]["lhs"][1:])
                == int(rules[pair[0]]["rhs"][1:])
                == int(rules[pair[1]]["lhs"][1:])
                == int(rules[pair[1]]["rhs"][1:])
            ):
                # TODO:
                # Just test solution on range of values and accept it if enough are correct
                print(rules[pair[0]], rules[pair[1]])
                known.update(pair)
                break
        # swap_rules(rules, pair[1], pair[0])
    return ",".join(sorted(rules[i]["output"] for i in known))


inits, rules = split_groups("inputs/day24.txt")
registers, rules = parse(inits, rules)
orig_registers = registers.copy()
registers = simulate(registers, rules)
part1 = calculate(registers)
print(part1)
part2 = find_misaligned(rules, registers, orig_registers)
print(part2)

import re
from math import inf
from collections import defaultdict
from utils.utils import split_lines


def recurse(start, char,  paths, memo, depth, max_depth):
    if depth == max_depth:
        return 1
    this_paths = paths[depth]
    options = this_paths[start][char]
    best = inf

    key = (start, char)
    if key in memo[depth]:
        best =  memo[depth][key]
    else:
        for option in options:
            # Record cost of whole path at depth
            this_cost = 0  # For A
            option += "A"
            # Not sure about this...
            prev = "A"
            for new_char in option:
                this_cost += recurse(prev, new_char, paths, memo, depth + 1, max_depth)
                prev = new_char
            # THis should be right...
            best = min(best, this_cost)
            # Here is the bug: 
            memo[depth][key] = min(memo[depth].get(key, inf), this_cost)
    return best

    # prev = "A"
    # result = 0
    # #breakpoint()
    # for char in code:
    #     result += inner(prev, char, 0)
    #     prev = char
    # return result
    #

# Best paths change direction at most once
def min_turns(path):
    if len(path) < 3:
        return True
    prev = path[0]
    turns = 0
    for p in path[1:]:
        turns += p != prev
        if turns > 1:
            return False
        prev = p
    return True


def parse_keypad(keypad):
    keypad = keypad.rstrip("\n").splitlines()
    keypad = keypad[1:-1:]
    y = 0
    result = {}
    for line in keypad:
        if not "+" in line:
            chars = re.findall(r"\s([^|])\s", line)
            for x, c in enumerate(chars):
                if c != " ":
                    result[c] = complex(x, y)
            y += 1

    return result


def explore_paths(keypad):
    inverse = dict(zip(keypad.values(), keypad.keys()))
    result = defaultdict(lambda: defaultdict(list))
    directions = {-1j: "^", 1: ">", 1j: "v", -1: "<"}

    for symbol, coord in keypad.items():
        queue = [(coord, [])]
        best = defaultdict(lambda: inf)
        while queue:
            current_coord, current_prev = queue.pop()
            n = len(current_prev)

            if n > best[current_coord]:
                continue
            if n <= best[current_coord]:
                current_symbol = inverse[current_coord]
                if n < best[current_coord]:
                    result[symbol][current_symbol] = []
                    best[current_coord] = n

                path = "".join(current_prev)
                if min_turns(path):
                    result[symbol][current_symbol].append(path)
            for dir, dir_symbol in directions.items():
                new_coord = current_coord + dir
                if new_coord in inverse:
                    queue.append((new_coord, current_prev + [dir_symbol]))

    return result


door_keypad = """+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+"""

robot_keypad = """+---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+"""
# Find outer robot's commands for inner robot
door_keymap = parse_keypad(door_keypad)
robot_keymap = parse_keypad(robot_keypad)
door_paths = explore_paths(door_keymap)
robot_paths = explore_paths(robot_keymap)
codes = split_lines("inputs/day21.txt")

paths_dict = defaultdict(lambda: robot_paths)
paths_dict[0] = door_paths
part1_memo = defaultdict(dict)
part2_memo = defaultdict(dict)
part1 = part2 = 0

for code in codes:
    s1 = s2 =  0
    prev = "A"
    for c in code:
        #print(recurse(prev, c, paths_dict, memo, 0, 3))
        s1 += recurse(prev, c, paths_dict, part1_memo, 0, 3)
        s2 += recurse(prev, c, paths_dict, part2_memo, 0, 26)
        prev = c
    factor = int(code[:-1])
    part1 += (s1 * factor)
    part2 += (s2 * factor)
    
print(part1)
print(part2)

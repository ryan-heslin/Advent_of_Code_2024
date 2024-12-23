import re
from math import inf
from collections import defaultdict
from itertools import product


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

                result[symbol][current_symbol].append("".join(current_prev))
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


def find_paths(paths, previous):
    last = "A"
    result = []
    for c in  previous:
        result.append({ p + "A" for p in paths[last][c] })
        last = c
    return result

def find_shortest(paths, previous):
    possibilities = [i  for i, el in enumerate(previous) if len(el) > 1 ]
    sequences = product(*(previous[p] for p in possibilities))
    result = []
    for s in sequences:
        s = list(s)
        this = ""
        for i, el in enumerate(previous):
            if i in possibilities:
                this += s.pop(0)
            else:
                this += next(iter(el))
        result.append(find_paths(paths, this))
   
    #TODO aggregate result paths
    breakpoint()
    return result





# Find outer robot's commands for inner robot

# TODO Check total length of all permutations, use shortest

door_keymap = parse_keypad(door_keypad)
robot_keymap = parse_keypad(robot_keypad)
door_paths = explore_paths(door_keymap)
robot_paths = explore_paths(robot_keymap)
start = find_paths(door_paths, "029A")
part2 = find_shortest(robot_paths, start)

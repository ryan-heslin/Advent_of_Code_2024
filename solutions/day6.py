from utils.utils import split_lines
from bisect import bisect_left
from collections import defaultdict
from math import copysign
from collections import OrderedDict


def parse(lines):
    directions = {"^": -1j, ">": 1, "v": 1j, "<": -1}
    graph = {}
    start = direction = None

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if directions.get(char):
                coord = complex(x, y)
                direction = directions[char]
                graph[coord] = "."
                start = coord
            else:
                graph[complex(x, y)] = char
    return graph, start, direction


def parse2(lines):

    # FOr each x coord, list of y coords of blocked spaces, vice versa for y coords
    # (x, {blocked y})
    # (y , {blocked x})
    result = [defaultdict(list), defaultdict(list)]
    directions = {"^": -1j, ">": 1, "v": 1j, "<": -1}
    start = direction = None
    xmax = len(lines[0])
    ymax = len(lines)

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                x_index = bisect_left(result[0][x], y)
                result[0][x].insert(x_index, y)
                y_index = bisect_left(result[1][y], x)
                result[1][y].insert(y_index, x)
            elif directions.get(char):
                start = complex(x, y)
                direction = directions[char]
    return start, direction, result, xmax, ymax


def walk(graph, start, direction, xmax, ymax):
    xmin = ymin = 0
    current = start
    visited = set()
    while xmin <= current.real <= xmax and ymin <= current.imag <= ymax:
        # Moving horizontally
        if direction.real != 0:
            position = current.real
            obstacles = graph[1]
            sign = copysign(1, direction.real)
        # Vertical
        else:
            position = current.imag
            obstacles = graph[0]
            sign = copysign(1, direction.imag)

        index = bisect_left(obstacles, position)
        # Out of bounds
        if index == 0 or index == len(obstacles):
            pass

        direction *= 1j

def check_loops(graph, options, start, direction):
    result = 0
    for o in options:
        result += not len(traverse(graph | {o: "#"}, start, direction))
    return result


def traverse(graph, start, direction):
    current = start
    visited = defaultdict(set)
    rotations = {-1j : 1, 1 : 1j, 1j: -1, -1: -1j}

    while True:
        if direction in visited[current]:
            return set()
        visited[current].add(direction)
        new = direction + current
        if graph.get(new) is None:
            return set(visited.keys())

        if graph[new] == "#":
            direction = rotations[direction]
        else:
            current = new
        # Loop found

lines = split_lines("inputs/day6.txt")
# start, direction, graph, xmax, ymax = parse(lines)
graph, start, direction = parse(lines)
path = traverse(graph, start, direction)
print(len(path))
path.discard(start)
part2 = check_loops(graph, path, start, direction)
print(part2)
# x = "\n".join(
#         "".join(
#             graph[complex(x, y)] if complex(x, y) not in visited else "X"
#             for x in range(len(lines[0]))
#             )
#         
# for y in range(len(lines)))
# print(x)

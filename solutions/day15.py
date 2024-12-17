from enum import Enum
from utils.utils import split_groups


DIRECTIONS = {"^": -1j, ">": 1, "v": 1j, "<": -1}


class Tile(Enum):
    OPEN = 0
    WALL = 1
    BOX = 2
    LBOX = 3
    RBOX = 4


def parse(lines, mapping):
    result = {}
    start = None
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            coord = complex(x, y)
            if char == "@":
                start = coord
            result[coord] = mapping[char]

    return result, start


# def print_graph(graph, current):
#     extremes = extrema(graph)
#     mapping = {
#         Tile.OPEN: ".",
#         Tile.WALL: "#",
#         Tile.BOX: "O",
#         Tile.LBOX: "[",
#         Tile.RBOX: "]",
#     }
#     return "\n".join(
#         "".join(
#             mapping[graph[complex(x, y)]] if complex(x, y) != current else "@"
#             for x in range(extremes["xmax"] + 1)
#         )
#         for y in range(extremes["ymax"] + 1)
#     )


def simple_push(graph, new, dir, boxes):
    head = new
    while (tile := graph.get(head)) in boxes:
        head += dir

    if tile == Tile.OPEN:
        # Have to swap all boxes' side types if part 2
        graph[new] = Tile.OPEN
        # Part 2 boxes
        if len(boxes) > 1:
            height = new.imag
            choices = (Tile.LBOX, Tile.RBOX)
            # Since leftmost of leftward push is left box, etc.
            choice = int(dir == 1)
            for i in range(int(head.real), int(new.real), -int(dir.real)):
                graph[complex(i, height)] = choices[choice]
                choice = (choice + 1) % 2
        else:
            box = next(iter(boxes))
            graph[head] = box
        return new
    return new - dir


def complex_push(graph, new, dir, boxes):
    box_type = graph[new]
    other = new + (1 if box_type == Tile.LBOX else -1)
    checked_boxes = [{new: box_type, other: graph[other]}]
    while True:
        new_boxes = {}
        for coord, box_type in checked_boxes[-1].items():
            contact = coord + dir
            tile_type = graph.get(contact)
            # SInce pushing either side pushes whole box
            if tile_type in boxes:
                new_boxes[contact] = tile_type
                other = contact + (1 if tile_type == Tile.LBOX else -1)
                assert graph[other] in boxes
                new_boxes[other] = graph[other]
            # Hit any wall and push fails
            elif tile_type == Tile.WALL or tile_type is None:
                return new - dir
        if not new_boxes:
            break
        checked_boxes.append(new_boxes)
    for box_set in reversed(checked_boxes):
        for coord, box_type in box_set.items():
            graph[coord] = Tile.OPEN
            graph[coord + dir] = box_type
    return new


def calculate_1(graph, boxes):
    # Part 1 formula
    return sum(k.imag * 100 + k.real if v in boxes else 0 for k, v in graph.items())


def execute(graph, instructions, start, boxes, calculator, part2=False):
    current = start
    # print(print_graph(graph,  current))
    for char in instructions:
        dir = DIRECTIONS[char]
        new = current + dir
        result = graph.get(new)
        if result == Tile.OPEN:
            current = new
        elif result in boxes:
            # Just have clear box closest to bot and add to end of chain
            func = complex_push if (part2 and dir.imag) else simple_push
            current = func(graph, new, dir, boxes)
    return int(calculator(graph, boxes))


mapping = dict(zip((".", "#", "O", "[", "]", "@"), list(Tile) + [Tile.OPEN]))
lines, instructions = split_groups("inputs/day15.txt")
instructions = instructions.replace("\n", "")
graph, start = parse(lines.splitlines(), mapping)
part1 = execute(graph, instructions, start, {Tile.BOX}, calculate_1)
print(part1)

replacements = {"#": "##", "O": "[]", ".": "..", "@": "@."}
for old, new in replacements.items():
    lines = lines.replace(old, new)
part2_graph, part2_start = parse(lines.splitlines(), mapping)
part2 = execute(
    part2_graph,
    instructions,
    part2_start,
    {Tile.LBOX, Tile.RBOX},
    lambda g, _: calculate_1(g, {Tile.LBOX}),
    True,
)
print(part2)

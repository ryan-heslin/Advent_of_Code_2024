from utils.utils import split_lines
from collections import defaultdict
from itertools import combinations


def parse(lines):
    result = defaultdict(set)
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != ".":
                result[char].add(complex(x, y))
    return result

    # d = {complex(x, y) : char
    #      if char != "."}
    # result = defaultdict(lambda: ".")
    # result.update(d)
    # return result


def in_range(xmin, xmax, ymin, ymax, x):
    return (xmin <= x.real <= xmax) and (ymin <= x.imag <= ymax)


def find_antinodes(map, xmax, ymax):
    part1 = set()
    part2 = set()

    # Find slope
    # Use first coord as intercept
    # Compute intercepts of borders
    # Integer divide by signal's rise and run, subtract 2

    for coordinates in map.values():
        for combo in combinations(coordinates, r=2):
            combo = sorted(combo, key=lambda x: (x.real, x.imag))
            offset = combo[1] - combo[0]
            first = combo[0] - offset
            # All antennas count as antinodes
            part2.update(combo)

            if in_range(0, xmax, 0, ymax, first):
                part1.add(first)
                current = first
                while in_range(0, xmax, 0, ymax, current):
                    part2.add(current)
                    current -= offset

            second = combo[1] + offset
            if in_range(0, xmax, 0, ymax, second):
                part1.add(second)
                current = second
                while in_range(0, xmax, 0, ymax, current):
                    part2.add(current)
                    current += offset

    print(
        "\n".join(
            ("".join("#" if complex(x, y) in part2 else "." for x in range(xmax + 1)))
            for y in range(ymax + 1)
        )
    )
    return len(part1), len(part2)


lines = split_lines("inputs/day8.txt")
xmax = len(lines[0]) - 1
ymax = len(lines) - 1
mapping = parse(lines)
part1, part2 = find_antinodes(mapping, xmax, ymax)
print(part1)
print(part2)

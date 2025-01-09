from utils.utils import neighbors
from utils.utils import split_lines


def parse(lines):
    return {
        complex(x, y): int(char)
        for y, line in enumerate(lines)
        for x, char in enumerate(line)
    }


def count_paths(coords, neighbors):
    target = 9
    part1 = part2 =  0

    for coord, val in coords.items():
        if val == 0:
            paths = [[coord]]
            peaks = set()

            while paths:
                new_paths = []
                for path in paths:
                    last = path[-1]
                    elevation = coords[last]
                    if coords[last] == target:
                        peaks.add(last)
                        part2 += 1
                    else:
                        elevation += 1
                        new = neighbors(last)
                        # Increasing condition ensures no repeat coords
                        for n in new:
                            if coords[n] == elevation:
                                new_paths.append(path + [n])
                paths = new_paths
            part1 += len(peaks)
    return part1, part2


lines = split_lines("inputs/day10.txt")
graph = parse(lines)
xmin = ymin = 0
xmax = len(lines[0]) - 1
ymax = len(lines) - 1
neighbors = neighbors(xmin, xmax, ymin, ymax)
part1, part2 = count_paths(graph, neighbors)
print(part1)
print(part2)

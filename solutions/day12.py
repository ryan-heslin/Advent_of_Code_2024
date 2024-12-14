from utils.utils import split_lines
from collections import deque
from math import inf


def parse(lines):
    return {
        complex(x, y): char
        for y, line in enumerate(lines)
        for x, char in enumerate(line)
    }


# TODO
def count_sides(edges):
    vertical = edges[0].real // 1 != edges[0].real
    attrs = ("real", "imag") if vertical else ("imag", "real")
    first, second = attrs
    groups = 0
    last = inf
    for e in edges:
        groups += (
            getattr(e, first) != getattr(last, first)
            or abs(getattr(e, second) - getattr(last, second)) > 1
        )
        last = e
    return groups


def compute_price(graph):
    done = set()
    price = 0
    discounted = 0
    neighbors = {-1j, 1, 1j, -1}
    for coord, val in graph.items():
        if coord not in done:
            unvisited = deque([coord])
            horizontal_edges = set()
            vertical_edges = set()
            perimeter = area = 0

            while unvisited:
                current = unvisited.pop()
                if current in done:
                    continue
                done.add(current)
                area += 1
                for direction in neighbors:
                    new = direction + current
                    edge = graph.get(new) != val
                    # perimeter += edge
                    if edge:
                        target = (
                            horizontal_edges if direction.real == 0 else vertical_edges
                        )
                        # Hack to distinguish separate edges touching at corners
                        target.add(current + direction * 0.49)
                    elif new not in done:
                        unvisited.append(new)

            # Measure out first segment
            perimeter = len(horizontal_edges) + len(vertical_edges)
            vertical_edges = sorted(vertical_edges, key=lambda x: (x.real, x.imag))
            horizontal_edges = sorted(horizontal_edges, key=lambda x: (x.imag, x.real))
            sides = count_sides(vertical_edges) + count_sides(horizontal_edges)

            # So each contiguous run is a vertical side, since a gap means the side ended

            # Record edge coords as x.5, y(vertical) or (y.5, x) (horizontal)
            # Use some line segment representation to track uniqueness, merging where needed
            # Use x.5, y coords coords
            # Group into segments once done and count
            # Count this set once done for part 2

            # Make {coord : {edge directions}} dict
            # Pick coord and find length of a side
            #
            # Alternately, expand each coord to 3x3 and walk edge coords
            price += area * perimeter
            discounted += area * sides

    return price, discounted


lines = split_lines("inputs/day12.txt")
graph = parse(lines)
part1, part2 = compute_price(graph)
print(part1)
print(part2)

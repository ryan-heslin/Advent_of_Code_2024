from collections import defaultdict
from utils.utils import split_lines
from utils.utils import manhattan
from functools import reduce
from math import inf
import heapq

# TODO: Use reconstruct_path instead of tracking, use A* instead of Dijkstra


class State:
    def __init__(self, coord, direction, previous, score):
        self.coord = coord
        self.direction = direction
        self.previous = previous
        self.score = score

    def __lt__(self, other):
        return self.score < other.score

    def __hash__(self):
        return hash((self.coord, self.direction))

    def __repr__(self) -> str:
        return (self.coord, self.direction, self.score).__repr__()


def parse(lines):
    start = end = None
    graph = set()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            coord = complex(x, y)
            if char not in {".", "#"}:
                if char == "S":
                    start = coord
                elif char == "E":
                    end = coord
                char = "."
            if char == ".":
                graph.add(coord)

    return graph, start, end


# Tighter lower bound if we check if at least one rotation is needed
# TODO compute number of rotations needed
def h(x, y):
    return manhattan(x, y)  # + 1000 * (x.real != y.real or x.imag != y.imag)

def count_paths(paths, endpoint):
    found = set()
    current = {endpoint}
    while current:
        found.update(current)
        current = reduce(set.union, (paths[p] for p in current))
        print(current)
        print("\n\n")

    return len(found)

def dijkstra(graph, start, end):
    directions = {-1j, 1, 1j, -1}
    first = State(start, 1, set(), 0)
    queue = [first]
    heapq.heapify(queue)

    dist = defaultdict(lambda: inf)
    dist[first] = 0
    prev = defaultdict(set)
    # prev[start] = h(start, end)
    cutoff = inf
    visited = set()
    paths =  {end}

    while queue:
        current = heapq.heappop(queue)
        # print(queue)
        if current.coord == end:
            if current.score <= cutoff:
                if current.score < cutoff:
                    paths = {end}
                    cutoff = current.score
                paths.update(current.previous)
            continue
        # if (current.coord, current.direction) in visited:
        #     continue
        for new_dir in directions:
            # No reversals
            if new_dir == -current.direction:
                continue
            rotation = new_dir != current.direction
            new_coord = current.coord if rotation else current.coord + new_dir
            if new_coord not in graph:
                continue
            new_score = current.score + (1000 if rotation else 1)
            new_state = State(new_coord, new_dir, current.previous | {current.coord}, new_score)
            if new_score < dist[new_state]:
                dist[(current.coord, current.direction)] = new_score
                prev[new_coord].add((current.coord))
                if (new_coord, new_dir) not in visited:
                    heapq.heappush(queue, new_state)
                    visited.add((current.coord, current.direction))

    return cutoff, len(paths)


lines = split_lines("inputs/day16.txt")
graph, start, end = parse(lines)
part1, part2 = dijkstra(graph, start, end)
print(part1)
print(part2)

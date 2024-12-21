from utils.utils import manhattan, neighbors, split_lines
from collections import defaultdict
from itertools import combinations, product
from math import inf
import heapq


class State(complex):
    def __new__(cls, real, imag=0.0, target=0.0, cheated=None):
        this = super().__new__(cls, real, imag)
        # Set the additional attribute
        this.target = target
        this.cheated = cheated
        return this

    def __init__(self, real, imag=0.0, target=0.0, cheated=None):
        self.target = target
        self.cheated = cheated

    def __add__(self, value: complex, /) -> complex:
        return self.__class__(
            self.real + value.real, self.imag + value.imag, self.target, self.cheated
        )

    def __hash__(self):
        return hash((self.real, self.imag, self.cheated))

    @property
    def dist(self):
        return manhattan(self, self.target)

    def __lt__(self, other):
        return self.dist < other.dist

    def __repr__(self) -> str:
        return f"(x={int(self.real)}, y={int(self.imag)}, cheated={self.cheated})"


def parse(lines):
    start = end = None
    graph = set()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != "#":
                coord = complex(x, y)
                if char == "S":
                    start = coord
                elif char == "E":
                    end = coord
                graph.add(coord)

    return start, end, graph


def A_star(graph, start, end, neighbors):
    unexplored = set(graph)
    # start = State(start, target=end, cheated=None)
    # end = State(end, target=end, cheated=None)
    open_set = [(start, manhattan(start, end))]
    heapq.heapify(open_set)

    g_score = defaultdict(lambda: inf)
    g_score[start] = 0

    while unexplored:
        try:
            current, dist = heapq.heappop(open_set)
            #unexplored.remove(current)
        except IndexError:
            break
        # if current == end:
        #     return g_score[current]

            # We need all routes that save 100, not just shortest
            # cutoff = min(cutoff, g_score[current])

        for n in neighbors(current):
            if n not in graph:
                continue

            new_g_score = g_score[current] + 1
            if new_g_score < g_score[n]:
                g_score[n] = new_g_score
                heapq.heappush(open_set, (n, new_g_score))

    return g_score


def count_cheats(from_start, from_end, xmax, ymax, graph, neighbors, cutoff):
    # Each cheat counted only once
    result = 0
    for x, y in product(range(xmax), range(ymax)):
        coord = complex(x, y)
        # if coord == 6 + 7j:
        #     breakpoint()
        if coord not in graph:
            options = (n for n in neighbors(coord) if from_start[n] < inf and from_start[end] < inf)
            for first, second in combinations(options, r=2):
                #print(((from_start[first] + 1 + from_end[second])))
                result += ((from_start[first] + 2 + from_end[second]) <= cutoff) + (
                    (from_start[second] + 2 + from_end[first]) <= cutoff
                    )
    return result

def count_cheats_2(from_start, from_end, cutoff, size = 20):
    result = 0
    for start, end in combinations(from_end.keys(), r = 2):
        dist = manhattan(start, end) 
        if 1 < dist  <= size:
            result += ((from_start[start] + from_end[end] + dist) <= cutoff) + ((from_start[end] + from_end[start] + dist) <= cutoff)
    return result




lines = split_lines("inputs/day20.txt")
xmax = len(lines[0]) - 1
ymax = len(lines) - 1
start, end, graph = parse(lines)
neighbor_finder = neighbors(0, xmax, 0, ymax, diag=False)
from_start = A_star(graph, start, end, neighbor_finder)
from_end = A_star(graph, end, start, neighbor_finder)
saving = 100
cutoff = from_start[end] - saving
# Expect 44 cheats
part1 = count_cheats(from_start, from_end, xmax, ymax, graph, neighbor_finder, cutoff)
print(part1)

part2 = count_cheats_2(from_start, from_end, cutoff)
print(part2)

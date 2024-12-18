from utils.utils import split_lines, manhattan
from math import inf
from collections import defaultdict
import heapq
# alt04 — Today at 2:31 PM
# TODO
# I thought about it and what the algorithm will basically do is:
# put all blocks down. apply djikstra (flood fill).
#
# Remove a block, knowing where the block was removed: continue djikstra/flood fill from there. Repeat untill you removed enough blocks to reach the target.

class Coord(complex):
    def __new__(cls, real, imag=0.0, target=0.0):
        this = super().__new__(cls, real, imag)
        # Set the additional attribute
        this.target = target
        return this

    def __init__(self, real, imag=0.0, target=0.0):
        self.target = target

    def __add__(self, value: complex, /) -> complex:
        return self.__class__(
            self.real + value.real, self.imag + value.imag, self.target
        )

    @property
    def dist(self):
        return manhattan(self, self.target)

    def __lt__(self, other):
        return self.dist < other.dist


def parse(lines, n=None):
    if n is None:
        n = len(lines)
    return (complex(*map(int, line.split(","))) for line in lines[:n])


def A_star(graph, start, end, xmax, ymax, verify = False):
    start = Coord(start, target=end)
    end = Coord(end, target=end)
    open_set = [start]
    heapq.heapify(open_set)
    directions = {-1j, 1, 1j, -1}

    g_score = defaultdict(lambda: inf)
    g_score[start] = 0

    cutoff = inf
    while True:
        try:
            current = heapq.heappop(open_set)
        except IndexError:
            break
        if current == end:
            if verify:
                return g_score[current]
            cutoff = min(cutoff, g_score[current])
            continue
        if g_score[current] >= cutoff:
            continue

        for dir in directions:
            new_coord = current + dir
            if new_coord in graph or not (
                0 <= new_coord.real <= xmax and 0 <= new_coord.imag <= ymax
            ):
                continue
            new_g_score = g_score[current] + 1
            if new_g_score < g_score[new_coord]:
                g_score[new_coord] = new_g_score
                heapq.heappush(open_set, new_coord)

    return cutoff


def find_block(graph, start, end, xmax, ymax, coords):
    for coord in coords:
        graph.add(coord)
        result = A_star(graph, start, end, xmax, ymax, verify=True)
        if result == inf:
            return f"{int(coord.real)},{int(coord.imag)}"


lines = split_lines("inputs/day18.txt")
n = 1024
graph = set(parse(lines, n))
xmax = ymax = 70
start = 0
end = complex(xmax, ymax)
part1 = A_star(graph, 0, end, xmax, ymax)
print(part1)

part2 = find_block(graph, start, end, xmax, ymax, list(parse(lines[n:])))
print(part2)

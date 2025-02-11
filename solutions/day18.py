from utils.utils import split_lines, manhattan
from math import inf
from collections import defaultdict
import heapq

class Coord(complex):
    def __new__(cls, real, imag=0.0, target: float|complex=0.0):
        this = super().__new__(cls, real, imag)
        this.target = target
        return this

    def __init__(self, real, imag=0.0, target :float | complex=0.0):
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
    return [ complex(*map(int, line.split(","))) for line in lines[:n] ]


def A_star(graph, start, end, xmax, ymax, coords):
    start = Coord(start, target=end)
    end = Coord(end, target=end)
    open_set = [start]
    heapq.heapify(open_set)
    directions = {-1j, 1, 1j, -1}
    coord_index = len(coords) - 1

    g_score = defaultdict(lambda: inf)
    g_score[start] = 0

    cutoff = inf
    while True:
        try:
            index = heapq.heappop(open_set)
        except IndexError:
            if cutoff < inf:
                break
            cost =  inf
            new = Coord(0, 0)
            while cost == inf:
                new = Coord(coords[coord_index], target = complex(end.real, end.imag))
                graph.remove(new)
                coord_index -= 1
                cost = min(g_score[dir + new] for dir in directions)
            #breakpoint()
            g_score[new] = cost + 1
            heapq.heappush(open_set, new)
            continue
        if index == end:
            cutoff = min(cutoff, g_score[index])
            continue
        if g_score[index] >= cutoff:
            continue

        for dir in directions:
            new_coord = index + dir
            if new_coord in graph or not (
                0 <= new_coord.real <= xmax and 0 <= new_coord.imag <= ymax
            ):
                continue
            new_g_score = g_score[index] + 1
            if new_g_score < g_score[new_coord]:
                g_score[new_coord] = new_g_score
                heapq.heappush(open_set, new_coord)

    if coord_index < len(coords) -1:
        coord = coords[coord_index + 1]
        return f"{int(coord.real)},{int(coord.imag)}"
    else:
        return cutoff


lines = split_lines("inputs/day18.txt")
n = 1024
first = parse(lines, n)
xmax = ymax = 70
start = 0
end = complex(xmax, ymax)
part1 = A_star(set(first), 0, end, xmax, ymax, first)
print(part1)

second = parse(lines[n:])
coords = first + second

part2 = A_star(set(coords), start, end, xmax, ymax, coords)
print(part2)

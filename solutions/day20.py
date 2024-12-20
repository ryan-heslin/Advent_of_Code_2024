from utils.utils import manhattan, neighbors, split_lines
from collections import defaultdict
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


def A_star(graph, start, end, neighbors, shortest_honest=inf):
    cheating = shortest_honest < inf
    start = State(start, target=end, cheated=None)
    end = State(end, target=end, cheated=None)
    open_set = [start]
    heapq.heapify(open_set)

    g_score = defaultdict(lambda: inf)
    g_score[start] = 0

    cutoff = shortest_honest
    result = {}

    def can_cheat(current, neighbor):
        return (
            cheating
            and current.cheated is None
            and any(
                (new_neighbor.real, new_neighbor.imag) != (current.real, current.imag)
                and new_neighbor in graph
                for new_neighbor in neighbors(neighbor)
            )
        )

    while True:
        # if cheating:
        #     breakpoint()
        try:
            current = heapq.heappop(open_set)
        except IndexError:
            break
        if current.real == end.real and current.imag == end.imag:
            if not cheating:
                return {None: g_score[current]}
            elif g_score[current] <= cutoff:
                result[current.cheated] = g_score[current]

            # We need all routes that save 100, not just shortest
            # cutoff = min(cutoff, g_score[current])
            continue
        if g_score[current] >= cutoff:
            continue

        for n in neighbors(current):
            wall = n not in graph
            if wall:
                if not can_cheat(current, n):
                    continue
                #breakpoint()
                cheated = True
            else:
                cheated = False

            new_state = State(
                n.real,
                n.imag,
                target=end.target,
                cheated=(complex(current.real + current.imag), n) if cheated else None,
            )
            new_g_score = g_score[current] + 1
            if new_g_score < g_score[new_state]:
                g_score[new_state] = new_g_score
                heapq.heappush(open_set, new_state)

    return result


lines = split_lines("inputs/day20.txt")
xmax = len(lines[0]) - 1
ymax = len(lines) - 1
start, end, graph = parse(lines)
neighbor_finder = neighbors(0, xmax, 0, ymax, diag=False)
shortest_honest = A_star(graph, start, end, neighbor_finder)[None]
part1 = A_star(graph, start, end, neighbor_finder, shortest_honest)
print(part1)

result = set()
for x in range(xmax+1):
    for y in range(ymax + 1):
        if complex(x, y) not in graph and sum(n in graph for n in neighbor_finder(complex(x, y))) > 1:
            result.add(complex(x, y))

from collections import defaultdict
from utils.utils import split_lines


def organize(nodes):
    return ",".join(sorted(nodes))

def parse(lines):
    result = defaultdict(set)
    for line in lines:
        to, fro = line.split("-")
        result[to].add(fro)
        result[fro].add(to)
    return result


def biggest_cluster(graph):
    biggest = set()

    for node in graph:
        remaining = graph[node]
        prev = {node}

        while remaining:
            current = remaining.pop()
            # All previous must be neighbors of new node
            if current in prev or prev - graph[current]:
                continue
            prev.add(current)
            remaining.update(graph[current])
        if len(prev) > len(biggest):
            biggest = prev

    return ",".join(sorted(biggest))



def clusters(graph):
    found = set()
    for start, neighbors in graph.items():
        for n in neighbors:
            for third in graph[n]:
                if start in graph[third]:
                    cluster = frozenset((start, n, third))
                    if len(cluster) == 3 and ("t" == start[0] or "t" == n[0] or "t" == third[0]):
                        found.add(cluster)

    return len(found)


def bron_kerbosch(R, P, X, G):
    if not (len(P) or len(X)):
        return R

    best = set()
    for vertex in set(P):
        result = bron_kerbosch(R | {vertex}, P & G[vertex], X &  G[vertex] , G  )
        if len(result) > len(best):
            best = result
        P.discard(vertex)
        X.add(vertex)
    return best


lines = split_lines("inputs/day23.txt")
graph = parse(lines)
part1 = clusters(graph)
print(part1)

part2 = organize(bron_kerbosch(set(), set(graph.keys()), set(), graph))
part2 = biggest_cluster(graph)
print(part2)

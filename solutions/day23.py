from collections import defaultdict
from utils.utils import split_lines

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


lines = split_lines("inputs/day23.txt")
graph = parse(lines)
part1 = clusters(graph)
print(part1)

part2 = biggest_cluster(graph)
print(part2)
# TODO: https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
#Part 2 starts with the set of edges, which are 2-cliques, and then recursively trying to grow the cliques one vertex. For this, starting off with all vertices reachable by any vertex in the clique and filtering the clique's vertices and filtering all vertices that are not reachable by all clique members. 

#!/usr/bin/env python3

from __future__ import print_function

import sys
from collections import deque, defaultdict
from dataclasses import dataclass


def tile_neighbours(pos, tile, part2):
    x, y = pos
    if tile == "." or part2:
        yield (x, y - 1)
        yield (x + 1, y)
        yield (x, y + 1)
        yield (x - 1, y)
    elif tile == ">":
        yield (x + 1, y)
    elif tile == "<":
        yield (x - 1, y)
    elif tile == "^":
        yield (x, y - 1)
    elif tile == "v":
        yield (x, y + 1)


def parse_map(lines, part2=False):
    rows = [line.strip() for line in lines]

    height = len(rows)
    width = len(rows[0])

    graph = defaultdict(lambda: set())
    for y, row in enumerate(rows):
        for x, tile in enumerate(row):
            if tile == "#":
                continue
            pos = (x, y)
            for nx, ny in tile_neighbours(pos, tile, part2):
                if nx < 0 or nx >= width or ny < 0 or ny >= height:
                    continue
                ntile = rows[ny][nx]
                if ntile != "#":
                    graph[pos].add((nx, ny))

    start = None
    end = None

    for x, tile in enumerate(rows[0]):
        pos = (x, 0)
        if tile == ".":
            start = pos
            break

    for x, tile in enumerate(rows[-1]):
        pos = (x, height-1)
        if tile == ".":
            end = pos
            break

    dims = width, height
    return start, end, dims, graph


@dataclass
class Node:
    edges: dict # (x,y) -> int /*dist*/

def condense_graph(graph):
    new_graph = {pos:Node({node:1  for node in children}) for pos, children in graph.items()}
    queue = deque(pos for pos in new_graph)
    while queue:
        pos = queue.popleft()
        node = new_graph[pos]
        if len(node.edges) == 2:
            (pos_a, weight_a), (pos_b, weight_b) = node.edges.items()

            new_weight = weight_a + weight_b
            node_a = new_graph[pos_a]
            node_a.edges.pop(pos)
            node_a.edges[pos_b] = new_weight

            node_b = new_graph[pos_b]
            node_b.edges.pop(pos)
            node_b.edges[pos_a] = new_weight

            new_graph.pop(pos)

    return new_graph


def part1(lines):
    start, end, _, graph = parse_map(lines)
    distances = {pos:-1 for pos in graph.keys()}
    queue = deque([(start, 0, None)])

    while queue:
        pos, prev_dist, prev_node = queue.popleft()
        distances[pos] = prev_dist

        for npos in graph[pos]:
            if npos == prev_node:
                continue

            dist = prev_dist + 1
            if dist <= distances[npos]:
                continue

            queue.appendleft((npos, dist, pos))
            distances[npos] = max(distances[npos], dist)

    return distances[end]


def part2(lines):
    start, end, _, graph = parse_map(lines, True)
    condensed_graph = condense_graph(graph)
    distances = {pos:-1 for pos in condensed_graph.keys()}
    queue = deque([(start, 0, set())])
    distances[start] = 0

    while queue:
        pos, prev_dist, path = queue.popleft()
        new_path = set(path)
        new_path.add(pos)

        for npos, weight in condensed_graph[pos].edges.items():
            if npos in new_path:
                continue
            dist = prev_dist + weight
            queue.appendleft((npos, dist, new_path))
            distances[npos] = max(distances[npos], dist)
    return distances[end]


def part2b(lines):
    start, end, _, graph = parse_map(lines, True)
    condensed_graph = condense_graph(graph)
    distances = {pos:-1 for pos in condensed_graph.keys()}
    distances[start] = 0

    def dfs(pos, dist=0, path=set()):
        path.add(pos)
        for npos, weight in condensed_graph[pos].edges.items():
            if npos in path:
                continue
            distances[npos] = max(distances[npos], dist + weight)
            dfs(npos, dist + weight, path)
        path.remove(pos)

    dfs(start)
    return distances[end]


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

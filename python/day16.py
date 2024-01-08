#!/usr/bin/env python3

import sys
from dataclasses import dataclass, field
from typing import List


@dataclass
class Node:
    mirror: str
    next_nodes: List['Node'] = field(default_factory=list)


def parse_mirrors(lines):
    nodes = {}
    height = len(lines)
    width = len(lines[0].strip())
    for y, line in enumerate(lines):
        for x, mtype in enumerate(line.strip()):
            if mtype == '.':
                continue
            pos = x, y
            nodes[pos] = Node(mtype)
    return nodes, (width, height)


def split_beam(mirror, vel):
    vx, vy = vel
    if (mirror == '-' and vx) or (mirror == '|' and vy):
        return [vel]
    return [(-abs(vy), -abs(vx)), (abs(vy), abs(vx))]


def reflect_beam(mirror, vel):
    vx, vy = vel
    if mirror == '/':
        return [(-vy, -vx)]
    else:
        return [(vy, vx)]


def part1(lines):
    nodes, (width, height) = parse_mirrors(lines)
    visited = set()
    queue = [((0, 0), (1, 0))]
    while queue:
        pos, vel = queue.pop(0)
        x, y = pos

        if (pos, vel) in visited:
            continue

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        visited.add((pos, vel))
        node = nodes[pos] if pos in nodes else None

        next_vel = []
        if not node:
            next_vel = [vel]
        elif node.mirror in '|-':
            next_vel = split_beam(node.mirror, vel)
        elif node.mirror in '/\\':
            next_vel = reflect_beam(node.mirror, vel)

        for vx, vy in next_vel:
            new_pos = (x + vx, y + vy)
            queue.append((new_pos, (vx, vy)))

    return len(set(pos for pos, _ in visited))


def part2(lines):
    nodes, (width, height) = parse_mirrors(lines)

    def run(pos, vel):
        visited = set()
        queue = [(pos, vel)]
        while queue:
            pos, vel = queue.pop(0)
            x, y = pos

            if (pos, vel) in visited:
                continue

            if x < 0 or x >= width or y < 0 or y >= height:
                continue

            visited.add((pos, vel))
            node = nodes[pos] if pos in nodes else None

            next_vel = []
            if not node:
                next_vel = [vel]
            elif node.mirror in '|-':
                next_vel = split_beam(node.mirror, vel)
            elif node.mirror in '/\\':
                next_vel = reflect_beam(node.mirror, vel)

            for vx, vy in next_vel:
                new_pos = (x + vx, y + vy)
                queue.append((new_pos, (vx, vy)))

        return len(set(pos for pos, _ in visited))

    answer = 0
    answer = max(answer, run((0, 0), (1, 0)), run((0, 0), (0, 1)))
    answer = max(answer, run((width-1, 0), (-1,0)), run((width-1, 0), (0, 1)))
    answer = max(answer, run((0, height-1), (1, 0)), run((0, height-1), (0, -1)))
    answer = max(answer, run((width-1, height-1), (-1, 0)), run((width-1, height-1), (0, -1)))
    for y in range(height):
        answer = max(answer, run((0, y), (1, 0)), run((width-1, y), (-1, 0)))
    for x in range(width):
        answer = max(answer, run((x, 0), (0, 1)), run((x, height-1), (0, -1)))
    return answer


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


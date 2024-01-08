#!/usr/bin/env python3

import sys


DIRS = {
    'R': (1, 0),
    'L': (-1, 0),
    'D': (0, 1),
    'U': (0, -1),
}


def parse_plan(lines):
    steps = []
    for line in lines:
        line = line.strip()
        direction, count, _ = line.split()
        steps.append((DIRS[direction], int(count, 10)))
    return steps


def parse_flipped_plan(lines):
    dir_map = { 0: 'R', 1: 'D', 2: 'L', 3: 'U' }
    steps = []
    for line in lines:
        line = line.strip()
        _, _, color = line.split()
        count, num = color[2:-2], int(color[-2:-1], 10)

        steps.append((DIRS[dir_map[num]], int(count, 16)))
    return steps


def next_steps(pos, direction, count):
    x, y = pos
    dx, dy = direction
    return [(x+dx*n, y+dy*n) for n in range(1, count+1)]


def flood_fill(plotted, pos, bounds):
    min_x, min_y, max_x, max_y = bounds
    width = max_x - min_x
    height = max_y - min_y

    filled = {}
    queue = [pos]
    while queue:
        px, py = queue.pop()
        filled[(px, py)] = True
        for dx, dy in DIRS.values():
            x, y = px + dx, py + dy
            if (x, y) in filled or (x, y) in plotted:
                continue
            if x < min_x or x >= max_x or y < min_y or y >= max_y:
                continue
            queue.append((x, y))
    return filled


def print_filled(filled, bounds):
    min_x, min_y, max_x, max_y = bounds
    width = max_x - min_x
    height = max_y - min_y

    print('╔' + ('═' * width) + '╗')
    for y in range(min_y, max_y):
        print('║', end='')
        for x in range(min_x, max_x):
            pos = (x, y)
            print('#' if pos in filled else '.', end='')
        print('║')
    print('╚' + ('═' * width) + '╝')


def part1(lines):
    steps = parse_plan(lines)
    current = (0, 0)
    plotted = { current: True }

    min_x, min_y = 0, 0
    max_x, max_y = 0, 0

    for direction, count in steps:
        for x, y in next_steps(current, direction, count):
            plotted[(x, y)] = True
            current = (x, y)
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)

    min_x -= 1
    min_y -= 1
    max_x += 2
    max_y += 2
    width = max_x - min_x
    height = max_y - min_y
    total_plots = width * height
    bounds = (min_x, min_y, max_x, max_y)
    filled = flood_fill(plotted, (min_x, min_y), bounds)
    # print_filled(filled, bounds)
    return total_plots - len(filled)


def part2(lines):
    steps = [(dx * amount, dy * amount) for (dx,dy), amount in parse_flipped_plan(lines)]
    prev = (0, 0)
    positions = []
    for (dx, dy) in steps:
        px, py = prev
        pos = (px + dx, py + dy)
        prev = pos
        positions.append(pos)

    # shoelace algorithm
    left, right = 0, 0
    for idx in range(len(positions)):
        ax, ay = positions[idx]
        bx, by = positions[(idx + 1) % len(positions)]
        left += (ax * by)
        right += (ay * bx)
    total = abs(left - right) // 2

    # add half total number of steps + 1 to account for outer tiles not included in shoelace algo
    total += sum(abs(dx + dy) for dx, dy in steps) // 2 + 1
    return total



def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


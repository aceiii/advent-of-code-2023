#!/usr/bin/env python3

import sys
from operator import itemgetter


def parse_galaxies(lines):
    galaxies = []
    height = len(lines)
    width = 0
    for y, line in enumerate(lines):
        for x, tile in enumerate(line.strip()):
            width = max(width, x)
            if tile == '#':
                galaxies.append((x, y))
    return galaxies, (width, height)


def expand_galaxies(galaxies, dims, expansion_amount=1):
    width, height = dims
    by_x = {}
    by_y = {}

    for x, y in galaxies:
        if x not in by_x:
            by_x[x] = []
        if y not in by_y:
            by_y[y] = []

        by_x[x].append((x, y))
        by_y[y].append((x, y))

    expand_cols = [x for x in range(width) if x not in by_x]
    expand_rows = [y for y in range(height) if y not in by_y]

    print('missing_x', expand_cols)

    galaxies = expand_by_x(galaxies, expand_cols, expansion_amount)
    galaxies = expand_by_y(galaxies, expand_rows, expansion_amount)

    return galaxies, (width + len(expand_cols), height + len(expand_rows))


def expand_by_x(galaxies, cols, expansion_amount):
    galaxies.sort(key=itemgetter(0), reverse=True)
    while cols:
        col = cols.pop()
        for idx in range(len(galaxies)):
            x, y = galaxies[idx]
            if x < col:
                break
            galaxies[idx] = (x+expansion_amount, y)
    return galaxies


def expand_by_y(galaxies, rows, expansion_amount):
    galaxies.sort(key=itemgetter(1), reverse=True)
    while rows:
        row = rows.pop()
        for idx in range(len(galaxies)):
            x, y = galaxies[idx]
            if y < row:
                break
            galaxies[idx] = (x, y+expansion_amount)
    return galaxies


def part1(lines):
    galaxies, dims = parse_galaxies(lines)
    #for glxy in galaxies:
    #    print(glxy)
    galaxies, new_dims = expand_galaxies(galaxies, dims)
    for glxy in galaxies:
        print(glxy)

    answer = 0
    for i, (x, y) in enumerate(galaxies[:-1]):
        for j, (x2, y2) in enumerate(galaxies[i:]):
            dx = abs(x2 - x)
            dy = abs(y2 - y)
            answer += dx + dy
    return answer


def part2(lines):
    galaxies, dims = parse_galaxies(lines)
    galaxies, new_dims = expand_galaxies(galaxies, dims, 1_000_000 - 1)

    answer = 0
    for i, (x, y) in enumerate(galaxies[:-1]):
        for j, (x2, y2) in enumerate(galaxies[i+1:]):
            dx = abs(x2 - x)
            dy = abs(y2 - y)
            answer += dx + dy
    return answer


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


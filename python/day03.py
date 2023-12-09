#!/usr/bin/env python3

import re
import sys


def neighbours(pos):
    x, y = pos
    yield x-1, y-1
    yield x, y-1
    yield x+1, y-1
    yield x+1, y
    yield x+1, y+1
    yield x, y+1
    yield x-1, y+1
    yield x-1, y


def parse_schematic(lines):
    numbers = []
    symbols = []

    for y, line in enumerate(lines):
        line = line.strip()
        for match in re.finditer('\d*|[^.]', line):
            digits = match.group(0)
            if not digits:
                continue
            x, xend = match.span()
            try:
                num = int(digits, 10)
                numbers.append((num, (x, y), xend - x))
            except:
                symbols.append((digits, (x, y)))
    return (numbers, symbols)


def find_part_numbers(schematic):
    numbers, symbols = schematic
    number_map = {}

    for num, (x, y), ln in numbers:
        for n in range(ln):
            pos = (x + n, y)
            number_map[pos] = (num, (x, y))

    parts = set()
    for _, pos in symbols:
        for new_pos in neighbours(pos):
            if new_pos in number_map:
                parts.add(number_map[new_pos])

    return parts


def find_gears(schematic):
    numbers, symbols = schematic
    number_map = {}

    for num, (x, y), ln in numbers:
        for n in range(ln):
            pos = (x + n, y)
            number_map[pos] = (num, (x, y))

    gears = []
    for sym, pos in symbols:
        if sym != '*':
            continue
        adjacent = set()
        for new_pos in neighbours(pos):
            if new_pos in number_map:
                adjacent.add(number_map[new_pos])
        if len(adjacent) == 2:
            first, second = adjacent
            gears.append(first[0] * second[0])

    return gears


def part1(lines):
    schematic = parse_schematic(lines)
    part_numbers = find_part_numbers(schematic)
    answer = 0
    for num, _ in part_numbers:
        answer += num
    return answer


def part2(lines):
    schematic = parse_schematic(lines)
    gears = find_gears(schematic)
    answer = 0
    for ratio in gears:
        answer += ratio
    return answer


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


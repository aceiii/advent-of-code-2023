#!/usr/bin/env python3

import sys
from functools import reduce


def parse_time_sheet(lines):
    time_line = lines[0][5:].strip()
    distance_line = lines[1][9:].strip()
    times = [int(x, 10) for x in time_line.split()]
    distances = [int(x, 10) for x in distance_line.split()]
    return list(zip(times, distances))


def parse_time_sheet2(lines):
    time_line = lines[0][5:].strip()
    distance_line = lines[1][9:].strip()
    time = int(time_line.replace(' ', ''), 10)
    distance = int(distance_line.replace(' ', ''), 10)
    return [(time, distance)]


def calc_first_win(time, distance):
    for t in range(1, time):
        tr = time - t
        if t * tr > distance:
            return t


def calc_last_win(time, distance):
    for t in range(time-1, 0, -1):
        tr = time - t
        if t * tr > distance:
            return t


def calc_winning_set(races):
    wins = []
    for time, distance in races:
        first = calc_first_win(time, distance)
        assert first is not None, 'Uh-oh!'
        last = calc_last_win(time, distance)
        wins.append(last - first + 1)
    print(wins)
    return wins


def part1(lines):
    races = parse_time_sheet(lines)
    return reduce(lambda a, b:  a * b, calc_winning_set(races))


def part2(lines):
    races = parse_time_sheet2(lines)
    print(races)
    return reduce(lambda a, b:  a * b, calc_winning_set(races))


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


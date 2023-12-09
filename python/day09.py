#!/usr/bin/env python3

import sys


def gen_diffs(history):
    return [history[x+1] - history[x] for x in range(len(history) - 1)]


def extrapolate_next_value(history):
    diffs = [history[:]]
    while not all(x == 0 for x in diffs[-1]):
        diffs.append(gen_diffs(diffs[-1]))


    while len(diffs) > 1:
        last_diff = diffs.pop()
        diffs[-1].append(diffs[-1][-1] + last_diff.pop())

    return diffs[-1][-1]


def extrapolate_prev_value(history):
    diffs = [history[:]]
    while not all(x == 0 for x in diffs[-1]):
        diffs.append(gen_diffs(diffs[-1]))

    while len(diffs) > 1:
        last_diff = diffs.pop()
        diffs[-1].insert(0, diffs[-1][0] - last_diff.pop(0))

    return diffs[-1][0]


def part1(lines):
    histories = [list(map(int, line.strip().split())) for line in lines]
    return sum(extrapolate_next_value(history) for history in histories)


def part2(lines):
    histories = [list(map(int, line.strip().split())) for line in lines]
    return sum(extrapolate_prev_value(history) for history in histories)


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


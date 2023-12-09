#!/usr/bin/env python3

import sys
from math import gcd
from functools import reduce


def part1(lines):
    steps = lines[0].strip()
    node_map = {}
    for line in lines[2:]:
        key, rest  = line.strip().split(' = ')
        left, right = rest[1:-1].split(', ')
        node_map[key] = (left, right)

    node  = 'AAA'
    end = 'ZZZ'

    idx = 0
    num_steps = len(steps)
    step_count = 0
    while node != end:
        step = steps[idx]
        node  = node_map[node][0 if step == 'L' else 1]
        idx = (idx + 1) % num_steps
        step_count += 1

    return step_count


def part2(lines):
    steps = lines[0].strip()
    node_map = {}
    for line in lines[2:]:
        key, rest  = line.strip().split(' = ')
        left, right = rest[1:-1].split(', ')
        node_map[key] = (left, right)


    def simulate_steps(start):
        idx = 0
        num_steps = len(steps)
        node = start
        while True:
            step = steps[idx]
            node  = node_map[node][0 if step == 'L' else 1]
            idx = (idx + 1) % num_steps
            yield node

    iterators = [simulate_steps(key) for key in node_map.keys() if key[-1] == 'A']
    z_match = [0] * len(iterators)
    count = 0
    while not all(z_match):
        count += 1
        nodes = [next(it) for it in iterators]
        if any(map(lambda node: node[-1] == 'Z', nodes)):
            for idx, node in enumerate(nodes):
                if node[-1] == 'Z' and z_match[idx] == 0:
                    z_match[idx] = count
    return reduce(lambda x, y: lcm(x, y), z_match)


def lcm(a, b):
    return (a * b) // gcd(a, b)


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


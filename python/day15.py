#!/usr/bin/env python3

import sys
import re


def hash(string):
    val = 0
    for c in string:
        val = ((val + ord(c)) * 17) % 256
    return val


def parse_init(lines):
    steps = []
    for line in lines:
        parts = line.strip().split(',')
        for part in parts:
            label, num = re.match('([a-z]+)(?:=(\d+)|-)', part).groups()
            steps.append(((label), int(num,10) if num is not None else None))
    return steps


def index_of(arr, func):
    for idx, item in enumerate(arr):
        if func(item):
            return idx
    return -1


def print_boxes(boxes):
    for idx, box in enumerate(boxes):
        if box:
            print('Box', idx, box)
    print()


def part1(lines):
    answer = 0
    for line in lines[0].strip().split(','):
        answer += hash(line)
    return answer


def part2(lines):
    boxes  = [[] for _ in range(256)]
    steps = parse_init(lines)
    for label, focus in steps:
        val = hash(label)
        idx = index_of(boxes[val], lambda x: x[0] == label)
        if focus is None and idx > -1:
            boxes[val].pop(idx)
        elif focus is not None:
            if idx == -1:
                boxes[val].append((label, focus))
            else:
                boxes[val][idx] = (label, focus)

    answer = 0
    for bid, box in enumerate(boxes):
        for slot, (_, focus) in enumerate(box):
            answer += (bid+1) * (slot+1) * focus
    return answer


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


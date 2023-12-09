#!/usr/bin/env python3

import sys
import re
import string


digit_names = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def calibration_value(line):
    s = re.sub(r'[^\d]', '', line.strip());
    if len(s) < 1:
        return 0
    return int(s[0] + s[-1], 10)


def calibration_value2(line):
    line = line.strip()
    digits = []
    for idx in range(len(line)):
        char = line[idx]
        if char in string.digits:
            digits.append(int(char, 10))
            continue

        rest = line[idx:idx + 5]
        for n, digit in enumerate(digit_names):
            if rest.find(digit) == 0:
                digits.append(n + 1)
                break
    return digits[0] * 10 + digits[-1]


def part1(lines):
    return sum(calibration_value(line) for line in lines if line.strip())


def part2(lines):
    return sum(calibration_value2(line) for line in lines if line.strip())


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


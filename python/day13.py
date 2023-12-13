#!/usr/bin/env python3

import sys



def rotate_pattern(pattern):
    height = len(pattern)
    width = len(pattern[0])
    rows = []
    for x in range(width):
        col = []
        for y in range(height-1, -1, -1):
            col.append(pattern[y][x])
        rows.append(''.join(col))
    return rows


def parse_patterns(lines):
    pattern = []
    patterns = []
    for line in lines:
        line = line.strip()
        if line == '':
            patterns.append(pattern)
            pattern = []
            continue
        pattern.append(line)
    if pattern:
        patterns.append(pattern)
    return patterns



to_bits = str.maketrans('.#', '01')
def parse_patterns2(lines):
    pattern = []
    patterns = []
    for line in lines:
        line = line.strip().translate(to_bits)
        if line == '':
            patterns.append(pattern)
            pattern = []
            continue
        pattern.append(line)
    if pattern:
        patterns.append(pattern)
    return patterns


def print_pattern(pattern):
    for line in pattern:
        print(line)
    print()


def check_mirror(pattern, y):
    h = min(y + 1, len(pattern) - y - 1)
    for dy in range(h):
        if pattern[y-dy] != pattern[y+dy+1]:
            return False
    return True


def count_bits(n):
    return f'{n:b}'.count('1')


def check_smudged_mirror(pattern, y):
    h = min(y + 1, len(pattern) - y - 1)

    diffs = [count_bits(int(pattern[y-dy], 2) ^ int(pattern[y+dy+1], 2)) for dy in range(h)]

    return sum(diffs) == 1

    for dy in range(h):
        if pattern[y-dy] != pattern[y+dy+1]:
            return False
    return True


def find_mirror(pattern):
    for y in range(len(pattern)-1):
        if check_mirror(pattern, y):
            return y + 1
    return 0


def find_smudged_mirror(pattern):
    for y in range(len(pattern)-1):
        if check_smudged_mirror(pattern, y):
            return y + 1
    return 0

def score_pattern(pattern):
    score = find_mirror(pattern)
    score2 =  find_mirror(rotate_pattern(pattern))
    return score * 100 + score2


def score_pattern2(pattern):
    score = find_smudged_mirror(pattern)
    score2 = find_smudged_mirror(rotate_pattern(pattern))
    return score * 100 + score2


def part1(lines):
    answer = 0
    patterns = parse_patterns(lines)
    for pattern in patterns:
        #print_pattern(rotate_pattern(pattern))
        answer += score_pattern(pattern)
    return answer


def part2(lines):
    answer = 0
    patterns = parse_patterns2(lines)
    for pattern in patterns:
        #print_pattern(rotate_pattern(pattern))
        answer += score_pattern2(pattern)
    return answer


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


#!/usr/bin/env python3

import re
import sys
from functools import reduce


def parse_report_line(line):
    springs, rest = line.strip().split(' ')
    return springs, [int(x, 10) for x in rest.split(',')]


def brute_force_arrangements(springs, groups):
    n = springs.count('?')
    max_n = 2**n
    result = 0
    for i in range(max_n):
        bits = list(f'{i:0{n}b}'.translate(str.maketrans('01', '.#')))
        replaced = ''.join(bits.pop(0) if c == '?' else c for c in springs)
        if errors_match(replaced, groups):
            result += 1
    return result


def errors_match(springs, groups):
    grouped_springs = [len(g) for g in springs.split('.') if g]
    return grouped_springs == groups


def to_spring_groups(springs):
    return [x for x in re.split(r'\.+', springs) if x]


def replace_spring(springs, idx, c):
    lsprings = list(springs)
    lsprings[idx] = c
    return ''.join(lsprings)


def to_groups(spring_groups):
    return tuple(len(sg) for sg in spring_groups)


cache = {}
def solve_springs(orig_springs, groups):
    global cache
    def solve_springs_inner(spring_groups, groups):
        key = (tuple(spring_groups), groups)

        if key in cache:
            return cache[key]

        if (not spring_groups and not groups) or (len(spring_groups) == 1 and '?' not in spring_groups[0]) or (not spring_groups and groups):
            ans = 1 if to_groups(spring_groups) == groups else 0
            cache[key] = ans
            return ans

        springs, *rest_springs = spring_groups
        ans = 0
        if '?' in springs:
            idx = springs.find('?')
            for c in '.#':
                new_springs = to_spring_groups(replace_spring(springs, idx, c))
                new_springs.extend(rest_springs)
                ans += solve_springs_inner(new_springs, groups)
        else:
            ans = solve_springs_inner(rest_springs, groups[1:]) if groups and len(springs) == groups[0] else 0

        cache[key] = ans
        return ans


    return solve_springs_inner(to_spring_groups(orig_springs), tuple(groups))


def part1(lines):
    answer = 0
    for line in lines:
        springs, groups = parse_report_line(line)
        #count = brute_force_arrangements(springs, groups)
        count = solve_springs(springs, groups)
        answer += count

    return answer


def part2(lines):
    answer = 0
    for line in lines:
        springs, groups = parse_report_line(line)
        springs = '?'.join([springs] * 5)
        groups = groups * 5
        answer += solve_springs(springs, groups)
    return answer

def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


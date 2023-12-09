#!/usr/bin/env python3

import sys
from operator import itemgetter
from dataclasses import dataclass, field
from typing import List


class Map:
    def __init__(self, name):
        self._name = name
        self._mappings = []

    def add_mapping(self, dst, src, rng):
        self._mappings.append((src, dst, rng))
        self._mappings.sort()


    def find(self, target):
        for src, dst, rng in self._mappings:
            if target >= src and target < src + rng:
                diff = target - src
                return dst + diff
        else:
            return target


    def __repr__(self):
        return str(self._mappings)


class Almanac:
    def __init__(self):
        self._maps = []

    def add_map(self, map):
        self._maps.append(map)

    def find(self, target):
        for map in self._maps:
            target = map.find(target)
        return target


class SeedRanges:
    def __init__(self, ranges):
        self.ranges = ranges

    def _split_ranges(self, mappings):
        for dst, src, rng in mappings:
            new_ranges = []
            for pos, pos_rng in self.ranges:
                pos_end = pos + pos_rng
                src_end = src + rng

                if src >= pos_end or src_end <= pos:
                    new_ranges.append((pos, pos_rng))
                elif src <= pos and src_end >= pos_end:
                    new_ranges.append((pos, pos_rng))
                elif src <= pos and src_end < pos_end:
                    new_rng1 = src_end - pos
                    new_rng2 = pos_end - src_end
                    new_ranges.append((pos, new_rng1))
                    new_ranges.append((pos + new_rng1, new_rng2))
                elif src > pos and src_end >= pos_end:
                    new_rng1 = src - pos
                    new_rng2 = pos_end - src
                    new_ranges.append((pos, new_rng1))
                    new_ranges.append((src, new_rng2))
                elif src > pos and src_end < pos_end:
                    new_rng1 = src - pos
                    new_rng2 = src_end - src
                    new_rng3 = pos_end - src_end
                    new_ranges.append((pos, new_rng1))
                    new_ranges.append((src, new_rng2))
                    new_ranges.append((pos + new_rng1 + new_rng2, new_rng3))
                else:
                    new_ranges.append((pos, pos_rng))

            self.ranges = new_ranges

    def _move_ranges(self, mappings):
        new_ranges = []
        for pos, pos_rng in self.ranges:
            for dst, src, rng in mappings:
                pos_end = pos + pos_rng
                src_end = src + rng
                delta = dst - src

                if src <= pos and src_end >= pos_end:
                    new_ranges.append((pos + delta, pos_rng))
                    break
            else:
                new_ranges.append((pos, pos_rng))

        self.ranges = new_ranges

    def apply_mappings(self, mappings):
        self._split_ranges(mappings)
        self._move_ranges(mappings)


def part1(lines):
    seeds = []
    almanac = Almanac()
    last_map = None

    for line in lines:
        line = line.strip()
        if line == '':
            continue
        elif line.find('seeds:') == 0:
            seeds = [int(x, 10) for x in line[7:].split()]
        elif line.find('map:') != -1:
            last_map = Map(line[:-4])
            almanac.add_map(last_map)
        else:
            dst, src, rng = [int(x, 10) for x in line.split()]
            last_map.add_mapping(dst, src, rng)

    return min(almanac.find(seed) for seed in seeds)


def part2(lines):
    seeds = [int(x, 10) for x in lines[0][7:].split()]
    seed_ranges = []
    while seeds:
        seed_ranges.append((seeds.pop(0), seeds.pop(0)))

    mappings = []
    for line in lines:
        line = line.strip()
        if line == '' or line.find('seeds:') == 0:
            continue
        elif line.find('map:') != -1:
            mappings.append([])
        else:
            dst, src, rng = [int(x, 10) for x in line.split()]
            mappings[-1].append((dst, src, rng))

    sr = SeedRanges(seed_ranges)

    for mapping in mappings:
        sr.apply_mappings(mapping)

    return sorted(sr.ranges)[0][0]


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


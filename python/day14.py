#!/usr/bin/env python3

import sys


def part1(lines):
    height = len(lines)
    width = len(lines[0])
    cols = {x:[] for x in range(width)}

    answer = 0
    for y, line in enumerate(lines):
        line = line.strip()
        for x,c in enumerate(line):
            if c == '#':
                cols[x].append(('#', y))
            elif c == 'O':
                new_y = cols[x][-1][1] + 1 if cols[x] else 0
                cols[x].append(('O', new_y))
                answer += height - new_y

    return answer


ROCK_TYPES = {
    '#': 0,
    'O': 1,
}

class RocksMap:
    def __init__(self, lines):
        self._height = len(lines)
        self._width = len(lines[0].strip())
        self._rows = [[] for _ in range(self._height)]

        for y, line in enumerate(lines):
            line = line.strip()
            for x, c in enumerate(line):
                if c not in ROCK_TYPES:
                    continue

                rock_type = ROCK_TYPES[c]
                pos = (x, y)
                rock = (rock_type, pos)
                self._rows[y].append(rock)

    def tilt(self, direction):
        if direction in 'NS':
            is_s = direction == 'S'
            cols = [[] for _ in range(self._width)]
            orig_rows = reversed(self._rows) if is_s else self._rows
            for row in orig_rows:
                for rock in row:
                    rock_type, (x, y) = rock
                    if not rock_type:
                        cols[x].append(rock)
                    else:
                        _, py = cols[x][-1][1] if cols[x] else (0, self._height if is_s else -1)
                        rock = (rock_type, (x, py + (-1 if is_s else 1)))
                        cols[x].append(rock)

            rows = [[] for _ in range(self._height)]
            for col in cols:
                for rock in col:
                    _, (_, y) = rock
                    rows[y].append(rock)
            self._rows = rows

        else:
            is_w = direction == 'W'
            is_e = direction == 'E'

            dx = 1 if is_w else -1
            default_pos = (-1,-1) if is_w else (self._width, 0)

            rows = [[] for _ in range(self._height)]
            for y, row in enumerate(self._rows):
                orig_row = reversed(row) if is_e else row
                for rock in orig_row:
                    rock_type, (x, _) = rock
                    if not rock_type:
                        rows[y].append(rock)
                    else:
                        if not is_w and not is_e:
                            rows[y].append(rock)
                        else:
                            px, _ = rows[y][-1][1] if rows[y] else default_pos
                            rock = (rock_type, (px + dx, y))
                            rows[y].append(rock)
                rows[y] = list(reversed(rows[y])) if is_e else rows[y]
            self._rows = rows

    def cycle(self):
        for direction in 'NWSE':
            self.tilt(direction)

    def total_load(self):
        load = 0
        for row in self._rows:
            for rock_type, (x, y) in row:
                if not rock_type:
                    continue
                load += self._height - y
        return load

    def print_map(self):
        #print(self._rows)
        print(self._height, self._width)
        print('┏' + '━' * self._width + '┓')
        for row in self._rows:
            prev_x = -1
            print('┃', end='')
            for rock_type, (x, _) in row:
                dx = x - prev_x - 1
                print('.' * dx, end='')
                print('O' if rock_type else '#', end='')
                prev_x = x
            dx = self._width - prev_x - 1
            print('.' * dx, end='')
            print('┃')
        print('┗' + '━' * self._width + '┛')


def part2(lines):
    repeats = {}
    rocks = RocksMap(lines)

    for n in range(1000):
        rocks.cycle()
        load = rocks.total_load()
        if load not in repeats:
            repeats[load] = []
        repeats[load].append(n+1)

    answer = None
    target = 1000000000
    for key, vals in repeats.items():
        if len(vals) <= 3:
            continue
        left = target - vals[0]
        diff = vals[1] - vals[0]
        n = left / diff
        if n == int(n):
            answer = key

    return answer

def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


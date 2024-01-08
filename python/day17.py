#!/usr/bin/env python3

from __future__ import print_function

import sys
from heapq import heappush, heappop


class LavaMap:
    class Node:
        def __init__(self, pos, val):
            self.pos = pos
            self.val = val

    def __init__(self, lines):
        self._rows = []
        self._dims = (len(lines[0].strip()), len(lines))
        for y, line in enumerate(lines):
            row = []
            for x, c in enumerate(line.strip()):
                node = LavaMap.Node((x, y), int(c, 10))
                row.append(node)
            self._rows.append(row)

    def _neighbours(self, pos):
        w, h = self._dims
        x, y = pos
        if y > 0:
            yield (x, y-1), '↑'
        if x < w-1:
            yield (x+1, y), '→'
        if y < h-1:
            yield (x, y+1), '↓'
        if x > 0:
            yield (x-1, y), '←'

    def dimensions(self):
        return self._dims

    def _node(self, pos):
        x, y = pos
        return self._rows[y][x]

    def _prev(self, prev, pos, limit=float('inf')):
        path = []
        node = pos
        i = 0
        while i < limit and node and node in prev and prev[node]:
            item = prev[node]
            node = item[0]
            path.append(item)
            i += 1
        return path

    def shortest_path2(self, start, end):
        def turning_func(dir_count, new_dir_count):
            if new_dir_count > 10:
                return False
            if new_dir_count == 1 and dir_count > 0 and dir_count < 4:
                return False
            return True

        return self.shortest_path(start, end, turning_func)

    def shortest_path(self, start, end, turning_func=None):
        reversed_dir = {
            '←': '→',
            '→': '←',
            '↓': '↑',
            '↑': '↓',
        }

        prev = {}
        queue = []

        queue.append((0, start, '', 0))
        w, h = self._dims

        while queue:
            prev_dist, pos, prev_dir, dir_count = heappop(queue)

            for new_pos, new_dir in self._neighbours(pos):
                if reversed_dir[new_dir] == prev_dir:
                    continue

                new_dir_count = dir_count + 1 if prev_dir == new_dir else 1
                if turning_func:
                    if not turning_func(dir_count, new_dir_count):
                        continue
                elif new_dir_count > 3:
                    continue

                node = self._node(new_pos)
                new_dist = prev_dist + node.val
                dist_key = (new_pos, new_dir, new_dir_count)

                if dist_key not in prev:
                    prev[dist_key] = new_dist, (pos, prev_dir, dir_count)
                    heappush(queue, (new_dist, new_pos, new_dir, new_dir_count))

        found = None
        for (key,(dist, prev_key)) in prev.items():
            pos, d, _ = key
            if pos == end and (not found or dist < found[0]):
                found = dist, key

        prev_map = {}
        _, key = found
        path = [self._node(key[0])]
        while key and key in prev:
            pos, _, _ = key
            _, prev_key = prev[key]
            prev_pos, _, _ = prev_key
            prev_map[pos] = prev_pos
            pos = prev_pos
            key = prev_key
            path.append(self._node(pos))

        #self.print_prev_map(prev_map, end)

        return list(reversed(path))


    def print_prev_map(self, prev_map, current):
        w, h = self._dims
        print('╔' + ('═' * w) + '╗')
        for y in range(h):
            print('║', end='')
            for x in range(w):
                pos = (x, y)
                if pos == current:
                    print('#', end='')
                elif pos not in prev_map:
                    print('.', end='')
                else:
                    ndir = self._node(pos).val
                    print(ndir, end='')
            print('║')
        print('╚' + ('═' * w) + '╝')

    def print_map(self, path):
        positions = set(node.pos for node in path)
        w, h = self._dims
        print('╔' + ('═' * w) + '╗')
        for y in range(h):
            print('║', end='')
            for x in range(w):
                pos = (x, y)
                if pos not in positions:
                    print('.', end='')
                else:
                    node = self._rows[y][x]
                    print(node.val, end='')
            print('║')
        print('╚' + ('═' * w) + '╝')

def part1(lines):
    lava = LavaMap(lines)
    width, height = lava.dimensions()
    path = lava.shortest_path((0, 0), (width-1, height-1))
    #lava.print_map(path)
    return sum(node.val for node in path[1:])


def part2(lines):
    lava = LavaMap(lines)
    width, height = lava.dimensions()
    path = lava.shortest_path2((0, 0), (width-1, height-1))
    #lava.print_map(path)
    return sum(node.val for node in path[1:])


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


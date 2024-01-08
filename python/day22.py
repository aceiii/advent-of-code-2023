#!/usr/bin/env python3

from __future__ import print_function

import sys
from collections import defaultdict, deque
from copy import deepcopy
from functools import reduce


def overlaps(a_bounds, b_bounds):
    axmin, axmax, aymin, aymax = a_bounds
    bxmin, bxmax, bymin, bymax = b_bounds

    if axmin > bxmax or axmax < bxmin:
        return False
    if aymin > bymax or aymax < bymin:
        return False
    return True


class Brick:
    def __init__(self, id_, start, end):
        self.id = id_
        self.start = start
        self.end = end

    def __repr__(self):
        return 'Brick[' + str(self.id) +']:' + str(self.start) + ',' + str(self.end)

    def bounds(self):
        ax, ay, az = self.start
        bx, by, bz = self.end
        xmin = min(ax, bx)
        xmax = max(ax, bx)
        ymin = min(ay, by)
        ymax = max(ay, by)
        zmin = min(az, bz)
        zmax = max(az, bz)
        return xmin, xmax, ymin, ymax, zmin, zmax

    def zmin(self):
        return min(self.start[2], self.end[2])

    def zmax(self):
        return max(self.start[2], self.end[2])

    def tiles(self):
        min_x, max_x, min_y, max_y, min_z, max_z = self.bounds()
        for z in range(min_z, max_z+1):
            for y in range(min_y, max_y+1):
                for x in range(min_x, max_x+1):
                    yield (x, y, z)

    def zadd(self, diff):
        ax, ay, az = self.start
        bx, by, bz = self.end
        self.start = (ax, ay, az + diff)
        self.end = (bx, by, bz + diff)


def sign(num):
    return int(num / abs(num))


def parse_pos(s):
    return tuple(int(a, 10) for a in s.split(','))


def parse_bricks(lines):
    bricks = []
    min_x, max_x = 2**32, -2**32
    min_y, max_y = 2**32, -2**32
    max_z = 1

    for y, line in enumerate(lines):
        line = line.strip()
        if not line:
            break

        left, right = line.split('~')
        start, end = parse_pos(left), parse_pos(right)

        bricks.append(Brick(y, start, end))

        sx, sy, sz = start
        ex, ey, ez = end
        min_x, max_x = min(min_x, sx, ex), max(max_x, sx, ex)
        min_y, max_y = min(min_y, sy, ey), max(max_x, sy, ey)
        max_z = max(max_z, sz, ez)

    bounds = (min_x, max_x, min_y, max_y, 1, max_z)
    return bricks, bounds


class World:
    def __init__(self, bricks, bounds):
        self._bounds = tuple(bounds)
        self._bricks = {brick.id:deepcopy(brick) for brick in bricks}
        self._tiles = {}

        min_x, max_x, min_y, max_y, min_z, max_z = bounds
        for z in range(min_z, max_z+1):
            for y in range(min_y, max_y+1):
                for x in range(min_x, max_x+1):
                    pos = (x, y, z)
                    self._tiles[pos] = None

        for brick in self._bricks.values():
            for pos in brick.tiles():
                self._tiles[pos] = brick.id

    def tiles(self):
        return self._tiles

    def tile(self, pos):
        return self._tiles[pos] if pos in self._tiles else None

    def drop_bricks(self):
        stopped = set()

        for brick in self._bricks.values():
            for _,_,z in brick.tiles():
                if z == 1:
                    stopped.add(brick.id)

        bricks = sorted([brick for brick in self._bricks.values() if brick.id not in stopped], key=lambda b: (b.zmin(), b.zmax()))

        while bricks:
            for brick in bricks:
                old_tiles = list(brick.tiles())
                new_tiles = [(x, y, max(1, z-1)) for x,y,z in old_tiles]
                if all(self._tiles[pos] == None or self._tiles[pos] == brick.id for pos in new_tiles):
                    for old_tile, new_tile in zip(old_tiles, new_tiles):
                        a, b = self._tiles[old_tile], self._tiles[new_tile]
                        self._tiles[old_tile] = b
                        self._tiles[new_tile] = a
                    brick.zadd(-1)
                elif any(self._tiles[pos] in stopped for pos in new_tiles):
                    stopped.add(brick.id)

                if any(z == 1 for _,_,z in new_tiles):
                    stopped.add(brick.id)

            bricks = sorted([brick for brick in self._bricks.values() if brick.id not in stopped], key=lambda b: (b.zmin(), b.zmax()))


def part1(lines):
    bricks, bounds = parse_bricks(lines)
    world = World(bricks, bounds)
    world.drop_bricks()

    supported_by = defaultdict(lambda: set())
    supporting = defaultdict(lambda: set())

    for pos, brick_id in world.tiles().items():
        if brick_id is None:
            continue
        x, y, z = pos
        above_tile = world.tile((x, y, z + 1))
        if above_tile is not None and above_tile != brick_id:
            supported_by[above_tile].add(brick_id)
            supporting[brick_id].add(above_tile)

    marked = set()
    for brick in bricks:
        if all(len(supported_by[bid]) > 1 for bid in supporting[brick.id]):
            marked.add(brick.id)
    return len(marked)


def part2(lines):
    bricks, bounds = parse_bricks(lines)
    world = World(bricks, bounds)
    world.drop_bricks()

    supported_by = defaultdict(lambda: set())
    supporting = defaultdict(lambda: set())

    for pos, brick_id in world.tiles().items():
        if brick_id is None:
            continue
        x, y, z = pos
        above_tile = world.tile((x, y, z + 1))
        if above_tile is not None and above_tile != brick_id:
            supported_by[above_tile].add(brick_id)
            supporting[brick_id].add(above_tile)

    marked = set()
    for brick in bricks:
        if all(len(supported_by[bid]) > 1 for bid in supporting[brick.id]):
            # marked.add(brick.id)
            pass
        else:
            marked.add(brick.id)

    supporting_counts = defaultdict(lambda: 0)
    queue = deque([brick_id for brick_id, supported_bricks in supporting.items() if supported_bricks])
    while queue:
        brick_id = queue.popleft()
        supporting_counts[brick_id] = len(supporting[brick_id]) + sum(supporting_counts[b] for b in supporting[brick_id])
        for other_brick in supported_by[brick_id]:
            queue.append(other_brick)

    def fall_count(brick_id):
        removed = set()
        queue = deque([brick_id])
        while queue:
            brick_id = queue.popleft()
            removed.add(brick_id)
            for other_brick_id in supporting[brick_id]:
                supports_left = set(supported_by[other_brick_id])
                supports_left.difference_update(removed)

                if supports_left:
                    continue
                queue.append(other_brick_id)
        return len(removed) - 1

    answer = 0
    for brick_id in marked:
        answer += fall_count(brick_id)
    return answer


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


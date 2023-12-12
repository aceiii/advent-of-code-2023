#!/usr/bin/env python3

import sys


PIPES = {
    '|': ((0,-1),(0,1)),
    '-': ((-1,0),(1,0)),
    'L': ((0,-1),(1,0)),
    'J': ((0,-1),(-1,0)),
    '7': ((0,1),(-1,0)),
    'F': ((0,1),(1,0)),
}


PRETTY_PIPES = {
    '|': '║',
    '-': '═',
    'L': '╚',
    'J': '╝',
    '7': '╗',
    'F': '╔',
    'S': '▲',
}

def neighbours(pos):
    x, y = pos
    yield x, y-1
    yield x+1, y
    yield x, y+1,
    yield x-1, y


def starting_pipes(pipe_map, pos):
    x, y = pos
    connecting = []
    for nx,ny in neighbours(pos):
        if nx < 0 or ny < 0 or ny >= len(pipe_map) or nx >= len(pipe_map[0]):
            continue
        pipe = pipe_map[ny][nx]
        if pipe not in PIPES:
            continue
        (px1, py1), (px2, py2) = PIPES[pipe]
        p1 = nx + px1, ny + py1
        p2 = nx + px2, ny + py2
        if p1 == pos or p2 == pos:
            connecting.append((nx, ny))
    return connecting


def connecting_pipes(pipe_map, pos):
    x, y = pos
    for nx, ny in PIPES[pipe_map[y][x]]:
        yield x + nx, y + ny


def parse_pipes(lines):
    start_pos = None
    pipe_map = []
    for y, line in enumerate(lines):
        row = []
        for x, tile in enumerate(line.strip()):
            if tile == 'S':
                start_pos = (x, y)
            row.append(tile)
        pipe_map.append(row)
    return start_pos, pipe_map


def part1(lines):
    pos, pipe_map = parse_pipes(lines)
    visited = { pos: 0 }
    next_pos = []

    for npos in starting_pipes(pipe_map, pos):
        visited[npos] = 1
        next_pos.append(npos)

    while next_pos:
        #print_map(pipe_map, visited)
        pos = next_pos.pop(0)
        connected = list(connecting_pipes(pipe_map, pos))
        for new_pos in connected:
            if new_pos in visited:
                continue
            visited[new_pos] = visited[pos] + 1
            next_pos.append(new_pos)

    return max(visited.values())


def print_map(pipe_map, visited):
    height = len(pipe_map)
    width = len(pipe_map[0])
    rows = []
    for y in range(height):
        cols = []
        for x in range(width):
            cols.append(visited[(x,y)] if (x,y) in visited else '.')
        rows.append(cols)
    for row in rows:
        print(''.join(map(str, row)))
    print()


def part2(lines):
    pos, pipe_map = parse_pipes(lines)
    visited = { pos: PRETTY_PIPES[pipe_map[pos[1]][pos[0]]] }
    next_pos = []

    for npos in starting_pipes(pipe_map, pos):
        visited[npos] = PRETTY_PIPES[pipe_map[npos[1]][npos[0]]]
        next_pos.append(npos)

    next_pos.sort()
    x, y = pos
    for pipe,((x1, y1), (x2, y2)) in PIPES.items():
        pos1 = (x + x1, y + y1)
        pos2 = (x + x2, y + y2)
        if sorted([pos1, pos2]) == next_pos:
            pipe_map[y][x] = pipe
            break

    while next_pos:
        pos = next_pos.pop(0)
        connected = list(connecting_pipes(pipe_map, pos))
        for new_pos in connected:
            if new_pos in visited:
                continue
            visited[new_pos] = PRETTY_PIPES[pipe_map[new_pos[1]][new_pos[0]]]
            next_pos.append(new_pos)

    answer = 0
    height = len(pipe_map)
    width = len(pipe_map[0])
    for y in range(height):
        crossing = 0
        for x in range(width):
            pos = (x, y)
            pipe = pipe_map[y][x]
            if pos in visited and  pipe in '|LJ':
                crossing += 1
            elif pos not in visited and crossing % 2 == 1:
                visited[pos] = 'I'
                answer += 1

    #print_map(pipe_map, visited)
    return answer


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


#!/usr/bin/env python3

import sys


def parse_cube(line):
    count, color = line.split(' ')
    return int(count, 10), color


def parse_line(line):
    line = line.strip()
    game, rest = line.split(':')
    game_id = int(game[5:], 10)

    draws =[]
    for draw in rest.split(';'):
        cubes = draw.strip().split(',')
        draw_cubes = []
        for cube in cubes:
            count, color = cube.strip().split(' ')
            draw_cubes.append((int(count, 10), color))
        draws.append(draw_cubes)

    return game_id, draws


def map_colors(draw):
    colors = {}
    for count, color in draw:
        colors[color] = count
    return colors


def decide_draw_part1(colors):
    red_valid = 'red' not in colors or colors['red'] <= 12
    green_valid = 'green' not in colors or colors['green'] <= 13
    blue_valid = 'blue' not in colors or colors['blue'] <= 14
    return red_valid and green_valid and blue_valid


def decide_game_part1(draws):
    for draw in draws:
        colors = map_colors(draw)
        if not decide_draw_part1(colors):
            break
    else:
        return True
    return False


def min_colors(draw):
    colors = {}
    for cubes in draw:
        for count, color in cubes:
            if color not in colors or count > colors[color]:
                colors[color] = count
    return colors


def power_of(colors):
    red = colors['red'] if 'red' in colors else 0
    green = colors['green'] if 'green' in colors else 0
    blue = colors['blue'] if 'blue' in colors else 0
    return red * green * blue


def part1(lines):
    answer = 0
    for line in lines:
        game_id, draws = parse_line(line)
        if decide_game_part1(draws):
            answer += game_id
    return answer


def part2(lines):
    answer = 0
    for line in lines:
        game_id, draws = parse_line(line)
        colors = min_colors(draws)
        answer += power_of(colors)
    return answer


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


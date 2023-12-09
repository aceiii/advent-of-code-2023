#!/usr/bin/env python3

import sys


def parse_cards(lines):
    cards = []
    for line in lines:
        line = line.strip()
        first, rest = line.split(':')
        card_id = int(first[5:], 10)
        left, right = rest.strip().split('|')
        winning = sorted(int(x, 10) for x in left.split(' ') if x != '')
        hand = sorted(int(x, 10) for x in right.split(' ') if x != '')
        cards.append((card_id, winning, hand))
    return cards


def part1(lines):
    answer = 0
    cards = parse_cards(lines)
    for _, winning, hand in cards:
        count = len(set(winning).intersection(hand))
        score = 2**(count-1)
        answer += int(score)
    return answer


def part2(lines):
    cards = parse_cards(lines)
    multipliers = [1] * len(cards)
    num_cards = len(cards)
    for idx, (_, winning, hand) in enumerate(cards):
        win_count = len(set(winning).intersection(hand))
        mult = multipliers[idx]
        for y in range(win_count):
            multipliers[min(idx + y + 1, num_cards-1)] += mult
    print(multipliers)
    return sum(multipliers)


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


#!/usr/bin/env python3

import sys
from operator import itemgetter


card_types = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
hand_types = ['high_card', 'one_pair', 'two_pair', 'three_kind', 'full_house', 'four_kind', 'five_kind']
joker_card_types = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']


def hand_type(cards):
    counts = tuple(sorted([cards.count(card) for card in set(cards)], reverse=True))
    if counts[0] == 5:
        return 'five_kind'
    if counts[0] == 4:
        return 'four_kind'
    if counts[0] == 3 and counts[1] == 2:
        return 'full_house'
    if counts[0] == 3:
        return 'three_kind'
    if counts[0] == 2 and counts[1] == 2:
        return 'two_pair'
    if counts[0] == 2:
        return 'one_pair'
    return 'high_card'


def replace_joker(cards, replacement_card):
    return [replacement_card if card == 'J' else card for card in cards]


def joker_hand_type(cards):
    card_counts = sorted([(card, cards.count(card)) for card in set(cards)], reverse=True, key=itemgetter(1))

    if card_counts[0][1] == 5:
        return 'five_kind'

    best = [(hand_strength(cards), cards)]
    for card, count in card_counts:
        new_cards = replace_joker(cards, card)
        best.append((hand_strength(new_cards), new_cards))

    return hand_type(sorted(best, reverse=True)[0][1])


def hand_strength(cards):
    hand = hand_type(cards)
    strength = (hand_types.index(hand)+1)*(16**7)
    for idx, card in enumerate(cards):
        power = 5-idx
        strength += card_types.index(card)*(16**power)
    return strength


def joker_hand_strength(cards):
    hand = joker_hand_type(cards)
    strength = (hand_types.index(hand)+1)*(16**7)
    for idx, card in enumerate(cards):
        power = 5-idx
        strength += joker_card_types.index(card)*(16**power)
    return strength


def parse_hands(lines):
    hands = []
    for line in lines:
        hand, bid = line.strip().split()
        hands.append((list(hand), int(bid, 10)))
    return hands


def compare_hands(hand_a, hand_b):
    hand_strength(hand_a[0]) - hand_strength(hand_b[0])


def part1(lines):
    hands = parse_hands(lines)
    hands.sort(key=lambda hand: hand_strength(hand[0]))

    answer = 0
    for idx, (cards, bid) in enumerate(hands):
        answer += (idx+1) * bid
    return answer


def part2(lines):
    hands = parse_hands(lines)
    hands.sort(key=lambda hand: joker_hand_strength(hand[0]))

    answer = 0
    for idx, (cards, bid) in enumerate(hands):
        answer += (idx+1) * bid
    return answer


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


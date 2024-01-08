#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
from math import gcd
from functools import reduce


def lcm(a, b):
    return (a * b) // gcd(a, b)


def parse_input(lines):
    config = {}
    for line in lines:
        left, right = line.strip().split(' -> ')
        targets = right.strip().split(', ')
        if left == 'broadcaster':
            config[left] = (targets, None)
            continue
        mtype = left[0]
        name = left[1:]
        config[name] = (targets, 0 if mtype == '%' else 1)
    return config


class Broadcaster:
    def __init__(self, config):
        self._config = config
        self.reset()

    def reset(self):
        self._flipflops = defaultdict(lambda: False)
        self._conjunctions = {}
        self._pulse_count = defaultdict(lambda: 0)
        self._pulses = defaultdict(lambda: 0)
        self._queue = deque()
        for name, (_, mtype) in self._config.items():
            if mtype:
                self._conjunctions[name] = {}

        for name, (targets, _) in self._config.items():
            for target in targets:
                if target in self._conjunctions:
                    self._conjunctions[target][name] = -1

    def pulse_counts(self):
        return dict(self._pulse_count)

    def last_pulse(self, target):
        return self._pulses[target]

    def push(self, target='broadcaster'):
        self._queue.append((target, -1, 'button'))

        while self._queue:
            target, pulse, parent = self._queue.popleft()
            self._pulse_count[pulse] += 1
            self._pulses[target] = pulse

            #print(parent, '-low->' if pulse == -1 else '-high->', target)

            targets, mtype = self._config[target] if target in self._config else ([], None)
            new_pulse = pulse

            if target == 'broadcaster':
                pass
            elif not mtype:
                if pulse > 0:
                    continue
                state = not self._flipflops[target]
                self._flipflops[target] = state
                new_pulse = 1 if state else -1
            else:
                state = self._conjunctions[target]
                state[parent] = pulse
                self._conjunctions[target] = state
                new_pulse = -1 if all(p > 0 for p in state.values()) else 1

            for new_target in targets:
                self._queue.append((new_target, new_pulse, target))


def part1(lines):
    config = parse_input(lines)
    broadcaster = Broadcaster(config)
    for _ in range(1000):
        broadcaster.push()
    pulse_count = broadcaster.pulse_counts()
    return pulse_count[-1] * pulse_count[1]


def part2(lines):
    config = parse_input(lines)
    broadcaster = Broadcaster(config)
    counts = defaultdict(lambda: 0)

    for circuit in broadcaster._config['broadcaster'][0]:
        broadcaster.reset()
        while True:
            counts[circuit] += 1
            broadcaster.push(circuit)
            if all(not val for val in broadcaster._flipflops.values()):
                break

    return reduce(lambda x, y: lcm(x, y), counts.values())


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


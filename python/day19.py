#!/usr/bin/env python3

from __future__ import print_function

import re
import sys


def make_id_func(id):
    def inner_func(_):
        return id
    return inner_func


def make_rule_func(prop, op, num, target):
    def gt_func(obj):
        return target if obj[prop] > num else None
    def lt_func(obj):
        return target if obj[prop] < num else None
    return gt_func if op == '>' else lt_func


def parse_rule(rule):
    idx = rule.find(':')
    if idx == -1:
        return make_id_func(rule)

    try:
        left, target = rule.split(':')
        prop, op, num = re.split('(<|>)', left)
        return make_rule_func(prop, op, int(num, 10), target)
    except:
        print('er', rule)

def parse_rule2(rule):
    idx = rule.find(':')
    if idx == -1:
        return (rule,)

    left, target = rule.split(':')
    prop, op, num = re.split('(<|>)', left)
    return (prop, op, int(num, 10), target)


def parse_workflow(lines):
    mode = 0
    flows = {}
    parts = []
    for line in lines:
        line = line.strip()
        if line == '':
            mode += 1
            continue
        if not mode:
            name, rest = line.split('{')
            rules = rest[:-1].split(',')
            flows[name] = [parse_rule(rule) for rule in rules]
        else:
            props = line[1:-1].split(',')
            part = {}
            for prop in props:
                key, val = prop.split('=')
                part[key] = int(val, 10)
            parts.append(part)

    return flows, parts


def parse_workflow2(lines):
    flows = {}
    for line in lines:
        line = line.strip()
        if line == '':
            break
        name, rest = line.split('{')
        rules = rest[:-1].split(',')
        flows[name] = [parse_rule2(rule) for rule in rules]
    return flows


def run_flows(flows, part):
    name = 'in'
    while name not in ['A','R']:
        rules = flows[name]
        for rule in rules:
            result = rule(part)
            if result:
                name = result
                break
    return name


def split_data(prop, op, num, data):
    data_left = dict(data)
    data_right = dict(data)
    prop_min, prop_max = data[prop]

    new_mid = min(max(num + 1 if op == '>' else num, prop_min), prop_max)
    new_min = min(prop_min, new_mid)
    new_max = max(prop_max, new_mid)

    if op == '>':
        data_left[prop] = (new_mid, new_max)
        data_right[prop] = (new_min, new_mid)
    else:
        data_left[prop] = (new_min, new_mid)
        data_right[prop] = (new_mid, new_max)

    return data_left, data_right


def run_rule(rule, data):
    if len(rule) == 1:
        return (rule[0], data)
    prop, op, num, target = rule
    data_left, data_right = split_data(prop, op, num, data)
    return (target, data_left, data_right)


def run_flows2(flows, rule_name, data):
    accepted = []
    for rule in flows[rule_name]:
        target, *new_data = run_rule(rule, data)
        if target in ['A', 'R']:
            if target == 'A':
                accepted.append(new_data[0])
        else:
            accepted.extend(run_flows2(flows, target, new_data[0]))

        if len(new_data) == 2:
            data = new_data[1]

    return accepted


def part1(lines):
    flows, parts = parse_workflow(lines)
    answer = 0
    for part in parts:
        if run_flows(flows, part) == 'A':
            answer += sum(part.values())
    return answer


def part2(lines):
    flows = parse_workflow2(lines)
    data = {'x': (1, 4001), 'm': (1, 4001), 'a': (1, 4001), 's': (1, 4001)}
    accepted = run_flows2(flows, 'in', data)
    answer = 0
    for item in accepted:
        xmin, xmax = item['x']
        mmin, mmax = item['m']
        amin, amax = item['a']
        smin, smax = item['s']
        xdiff = xmax - xmin
        mdiff = mmax - mmin
        adiff = amax - amin
        sdiff = smax - smin
        answer += xdiff * mdiff * adiff * sdiff
    return answer


def main():
    lines = sys.stdin.readlines()
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()


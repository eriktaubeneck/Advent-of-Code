import string
from itertools import zip_longest

priority = {}
for i, s in enumerate(string.ascii_letters):
    priority[s] = i+1


sum_priority = 0

with open('input.txt', 'r') as f:
    for row in f:
        row = row.strip('\n')
        n_items = len(row)
        compartments = set(row[:n_items//2]), set(row[n_items//2:])
        items_in_both = compartments[0] & compartments[1]
        for item in items_in_both:
            sum_priority += priority[item]

print(f'Part 1: Sum of priorities: {sum_priority}')


def grouper(iterable, n, *, incomplete='fill', fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # from https://docs.python.org/3/library/itertools.html#itertools-recipes
    # grouper('ABCDEFG', 3, fillvalue='x') --> ABC DEF Gxx
    # grouper('ABCDEFG', 3, incomplete='strict') --> ABC DEF ValueError
    # grouper('ABCDEFG', 3, incomplete='ignore') --> ABC DEF
    args = [iter(iterable)] * n
    if incomplete == 'fill':
        return zip_longest(*args, fillvalue=fillvalue)
    if incomplete == 'strict':
        return zip(*args, strict=True)
    if incomplete == 'ignore':
        return zip(*args)
    else:
        raise ValueError('Expected fill, strict, or ignore')


sum_badge_priority = 0

with open('input.txt', 'r') as f:
    rucksacks = [row.strip('\n') for row in f]

groups = grouper(rucksacks, 3)
for group in groups:

    badge = set(group[0]) & set(group[1]) & set(group[2])
    if len(badge) != 1:
        raise Exception('unexpected number of unique items')
    badge = badge.pop()
    sum_badge_priority += priority[badge]

print(f'Sum badge priority: {sum_badge_priority}')

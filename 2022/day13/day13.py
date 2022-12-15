from itertools import zip_longest
from functools import cmp_to_key


use_example = False

if use_example:
    filename = 'example_input.txt'
else:
    filename = 'input.txt'

with open(filename, 'r') as f:
    _input = [row.strip() for row in f if row != '\n']

left_input = _input[::2]
right_input = _input[1::2]

left_items, right_items = None, None

# this is a dirty dirty hack, but it's an advent of code so who cares
exec('left_items = ['+', '.join(left_input)+']')
exec('right_items = ['+', '.join(right_input)+']')

# print(left_items)
# print(right_items)


def correct_order(left_packet, right_packet):
    # print(f'Compare {left_packet} vs {right_packet}')
    for left, right in zip_longest(left_packet, right_packet, fillvalue=None):
        # print(f'Compare {left} vs {right}')
        if type(left) is int and type(right) is int:
            if left < right:
                # print('Left side is smaller, so inputs are in the right order')
                return -1
            elif right < left:
                # print('Right side is smaller, so inputs are not in the right order')
                return 1
        elif left is None:
            # print('Left side ran out of items, so inputs are in the right order')
            return -1
        elif right is None:
            # print('Right side ran out of items, so inputs are not in the right order')
            return 1
        else:
            if type(left) is int:
                # print(f'Mixed types; convert left to [{left}] and retry comparison')
                left = [left, ]
            elif type(right) is int:
                # print(f'Mixed types; convert right to [{right}] and retry comparison')
                right = [right, ]
            result = correct_order(left, right)
            if result is not None:
                return result


right_order_indicies = []


for i, (left, right) in enumerate(zip(left_items, right_items)):
    # print(f'\nPair {i+1}')
    if correct_order(left, right) == -1:
        right_order_indicies.append(i+1)

print(f'Sum of indicies of pairs in the correct order: {sum(right_order_indicies)}')

packets = left_items + right_items + [[[2]], [[6]]]
sorted_packets = sorted(packets, key=cmp_to_key(correct_order))

divider_packet_indicies = [
    sorted_packets.index([[2]]) + 1,
    sorted_packets.index([[6]]) + 1
]
decoder_key = divider_packet_indicies[0] * divider_packet_indicies[1]

print(f'Decoder key for the distress signal is {decoder_key}')

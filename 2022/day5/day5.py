with open('input.txt', 'r') as f:
    _input = [row for row in f]

_rows = [row.strip('\n') for row in _input if not row.startswith('move')][:-2]
rows = [
    tuple(row[i] for i in range(1, len(_rows[0]), 4))
    for row in _rows
]


def build_stacks():
    stacks = [[] for _ in rows[0]]

    for row in rows[::-1]:
        for i, crate in enumerate(row):
            if crate != ' ':
                stacks[i].append(crate)
    return stacks


_moves = [row.strip('\n') for row in _input if row.startswith('move')]
_moves = [
    tuple(
        int(m) for m in
        move.replace('move ', '').replace('from ', '').replace('to ', '').split(' ')
    )
    for move in _moves]

moves = [(a, b-1, c-1) for a, b, c in _moves]


def print_stacks(stacks):
    for i, stack in enumerate(stacks):
        print(f'{i}' + ''.join(stack))


part_1_stacks = build_stacks()
for item_count, stack_from, stack_to in moves:
    for _ in range(item_count):
        part_1_stacks[stack_to].append(part_1_stacks[stack_from].pop())

print('Part 1 stacks:')
print_stacks(part_1_stacks)
print(f'Top row: {"".join(stack[-1] for stack in part_1_stacks if stack)}')

part_2_stacks = build_stacks()
for item_count, stack_from, stack_to in moves:
    part_2_stacks[stack_to].extend(part_2_stacks[stack_from][-item_count:])
    part_2_stacks[stack_from] = part_2_stacks[stack_from][:-item_count]

print('Part 2 stacks:')
print_stacks(part_2_stacks)
print(f'Top row: {"".join(stack[-1] for stack in part_2_stacks if stack)}')

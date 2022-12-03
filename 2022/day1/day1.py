
elves = []
accumulator = 0

with open('input.txt', 'rb') as f:
    for value in f:
        if value == b'\n':
            elves.append(accumulator)
            accumulator = 0
        else:
            accumulator += int(value.decode('utf8').strip('\n'))

elves.append(accumulator)

print(elves[-1])

max_calories = max(elves)

print(f'part 1, max calories: {max_calories}')

second_max_calories = max(v for v in elves if v not in [max_calories])
third_max_calories = max(
    v for v in elves if v not in [max_calories, second_max_calories]
)

print(
    f'part 2, max 3 calories: '
    f'{max_calories + second_max_calories + third_max_calories}'
)

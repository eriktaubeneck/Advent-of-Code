
elves = []
accumulator = 0

with open('part1-input.txt', 'rb') as f:
    for value in f:
        if value == b'\n':
            elves.append(accumulator)
            accumulator = 0
        else:
            accumulator += int(value.decode('utf8').strip('\n'))

print(max(elves))

with open('input.txt', 'r') as f:
    buffer = next(f)

for i in range(4, len(buffer)):
    if len(set(buffer[i-4:i])) == 4:
        print(f'First start-of-packet marker after character {i}')
        break

for i in range(14, len(buffer)):
    if len(set(buffer[i-14:i])) == 14:
        print(f'First start-of-message marker after character {i}')
        break

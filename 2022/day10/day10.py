
def generate_register(program):
    X = 1
    for instruction in program:
        args = instruction.strip().split(' ')
        match args:
            case ('noop',):
                yield X
            case ('addx', V):
                V = int(V)
                yield X
                yield X
                X += V


def sum_signal_at_indicies(indicies, values):
    _sum = 0
    for i, v in enumerate(values):
        if i in indicies:
            _sum += (i+1) * v
    return _sum


def draw_crt(values):
    s = ''
    for i, v in enumerate(values):
        j = i % 40
        if j == 0:
            s = s + '\n'
        if j-1 <= v <= j+1:
            s = s + '#'
        else:
            s = s + '.'
    return s


with open('input.txt', 'r') as f:
    register_values = generate_register(f)
    interesting_indicies = [i-1 for i in [20, 60, 100, 140, 180, 220]]
    _sum = sum_signal_at_indicies(interesting_indicies, register_values)
    print(f'Sum of intresting signal strengths is {_sum}')

with open('input.txt', 'r') as f:
    register_values = generate_register(f)
    crt = draw_crt(register_values)
    print(crt)

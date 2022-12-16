from dataclasses import dataclass, field

use_example = False

if use_example:
    filename = 'example_input.txt'
else:
    filename = 'input.txt'

rocks = []

with open(filename, 'r') as f:
    for rock in f:
        _points = [point for point in rock.strip().split(' -> ')]
        points = []
        for point in _points:
            x, y = point.split(',')
            x, y = int(x), int(y)
            points.append((x, y))
        rocks.append(points)


@dataclass
class Wall:
    rocks: list[list[tuple[int, int]]] = field(default_factory=list)
    part_one: bool = False

    def __post_init__(self):
        self._first_print = True
        self.start = (500, 0)
        self.state = {self.start: '+'}
        self.count = 0
        for rock in self.rocks:
            for point0, point1 in zip(rock[:-1], rock[1:]):
                self.fill_between_points(point0, point1)

        bottom = self.max_y + 2
        if self.part_one:
            for x in range(self.min_x-2, self.max_x+2):
                self.state[(x, bottom)] = '~'
        else:
            for x in range(self.min_x-2, self.max_x+2):
                self.state[(x, bottom)] = '#'

    def fill_between_points(self, point0, point1):
        x0, y0 = point0
        x1, y1 = point1
        x0, x1 = min([x0, x1]), max([x0, x1])
        y0, y1 = min([y0, y1]), max([y0, y1])
        if not (x0 == x1 or y0 == y1):
            raise Exception(f'Unexpeted path {point0} -> {point1}')
        for x in range(x0, x1+1):
            for y in range(y0, y1+1):
                self.state[(x, y)] = '#'

    def drop_grain(self):
        x, y = self.start
        while self.state.get((x, y), '.') != '~':
            if not self.part_one and y + 1 == self.max_y:
                for _x in [x-1, x, x+1]:
                    self.state[(_x, y+1)] = '#'

            if self.state.get((x, y+1), '.') in ['.', '~']:
                x, y = x, y+1
            elif self.state.get((x-1, y+1), '.') in ['.', '~']:
                x, y = x-1, y+1
            elif self.state.get((x+1, y+1), '.') in ['.', '~']:
                x, y = x+1, y+1
            else:
                self.state[(x, y)] = 'o'
                self.count += 1
                if self.part_one:
                    return False
                else:
                    if (x, y) == self.start:
                        return True
                    else:
                        return False
        return True

    def drop_all_sand(self, _print=False):
        while not self.drop_grain():
            if _print:
                if self.count % 100 == 0:
                    self.print_visual()
            else:
                self.print_count()
        self.print_visual()

    @property
    def min_x(self) -> int:
        return min(point[0] for point in self.state.keys())

    @property
    def min_y(self) -> int:
        return min(point[1] for point in self.state.keys())

    @property
    def max_x(self) -> int:
        return max(point[0] for point in self.state.keys())

    @property
    def max_y(self) -> int:
        return max(point[1] for point in self.state.keys())

    @property
    def header_str(self) -> str:
        x_values = [self.min_x]
        x_values.extend(list(range(
            self.min_x + (-self.min_x % 5),
            self.max_x - (-self.max_x % 5), 5)))
        x_values.append(self.max_x)
        height = len(str(self.max_x))
        width = len(str(self.max_y)) + 1
        s = ''
        for i in range(height):
            s = s + ' ' * width
            for a, b in zip(x_values[:-1], x_values[1:]):
                str_a = str(a) + ' ' * height
                s = s + str_a[i]
                diff = b - a
                s = s + ' ' * (diff - 1)
            str_b = str(b) + ' ' * height
            s = s + str_b[i]
            s = s + '\n'
        return s

    @property
    def visual_str(self) -> str:
        s = self.header_str
        width = len(str(self.max_y)) + 1
        for y in range(self.min_y, self.max_y + 1):
            str_y = str(y) + ' ' * (width - len(str(y)))
            s = s + str_y
            for x in range(self.min_x, self.max_x + 1):
                s = s + self.state.get((x, y), '.')
            s = s + '\n'
        s += f'{self.count} grains of sand have come to rest\n'
        return s

    def print_visual(self):
        visual_str = self.visual_str
        height = visual_str.count('\n') + 1

        LINE_UP = '\033[1A'
        LINE_CLEAR = '\x1b[2K'
        if self._first_print:
            self._first_print = False
        else:
            for _ in range(height):
                print(LINE_UP, end=LINE_CLEAR)
        print(visual_str)

    def print_count(self):
        print(f'{self.count} grains of sand have come to rest')
        LINE_UP = '\033[1A'
        LINE_CLEAR = '\x1b[2K'
        print(LINE_UP, end=LINE_CLEAR)


wall = Wall(rocks=rocks, part_one=True)

wall.drop_all_sand()

print(
    f'Part 1: Units of sand coming to rest: '
    f'{sum(1 for _ in wall.state.values() if _ == "o")}'
)

wall = Wall(rocks=rocks, part_one=False)

wall.drop_all_sand()

print(
    f'Part 2: Units of sand coming to rest: '
    f'{sum(1 for _ in wall.state.values() if _ == "o")}'
)

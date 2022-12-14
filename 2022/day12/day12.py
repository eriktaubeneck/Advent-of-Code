import string
from copy import deepcopy
import time
from dataclasses import dataclass, field

use_example = False

if use_example:
    filename = 'example_input.txt'
else:
    filename = 'input.txt'

big_int = 10**10


@dataclass
class ElevationMap:
    elevations: list[list[str]] = field(default_factory=list)

    def __post_init__(self):
        self.scores = [[big_int for _ in row] for row in self.elevations]
        start_x, start_y = self.start
        self.set_score_at(start_x, start_y, 0)
        self.visited = [[False for _ in row] for row in self.elevations]
        self.first_print = True

    def get_score_at(self, x: int, y: int) -> int:
        return self.scores[y][x]

    def set_score_at(self, x: int, y: int, value: int):
        self.scores[y][x] = value

    def visit(self, x: int, y: int):
        self.visited[y][x] = True

    def find_min_unvisited_score(self) -> tuple[int, int]:
        _min = big_int
        for _y, _scores in enumerate(self.scores):
            for _x, score in enumerate(_scores):
                if not self.visited[_y][_x] and score < _min:
                    x, y = _x, _y
                    _min = score
        return x, y

    def get_value_at(self, x: int, y: int) -> str:
        return self.elevations[y][x]

    def get_height_at(self, x: int, y: int) -> int:
        h = self.get_value_at(x, y)
        if h == 'S':
            h = 'a'
        if h == 'E':
            h = 'z'
        if h not in string.ascii_lowercase:
            raise Exception(f'unknown height: {h}')
        return string.ascii_lowercase.find(h)

    def is_end(self, x: int, y: int) -> bool:
        return self.get_value_at(x, y) == 'E'

    @property
    def start(self):
        for y, _elevations in enumerate(self.elevations):
            for x, elevation in enumerate(_elevations):
                if elevation == 'S':
                    return x, y
        raise Exception('start not found')

    @property
    def height(self):
        return len(self.elevations)

    @property
    def width(self):
        return len(self.elevations[0])

    def is_valid_move(self, x: int, y: int, new_x: int, new_y: int) -> bool:
        if new_x < 0 or new_y < 0 or new_x >= self.width or new_y >= self.height:
            return False
        elif self.visited[new_y][new_x]:
            return False
        else:
            current_height = self.get_height_at(x, y)
            new_height = self.get_height_at(new_x, new_y)
            return new_height <= current_height + 1

    def available_moves(self, x: int, y: int) -> list[tuple[int, int]]:
        possible_positions = [
            (x + move[0], y + move[1])
            for move in [(0, 1), (1, 0), (0, -1), (-1, 0)]
        ]
        return [
            new_position for new_position in possible_positions
            if self.is_valid_move(x, y, new_position[0], new_position[1])
        ]

    def find_path(self):
        x, y = self.start
        while not self.is_end(x, y):
            self.visit(x, y)
            self.print_current_path()
            # print(f'visiting {x, y}')
            for move in self.available_moves(x, y):
                # print(f'available move: {move}')
                _x, _y = move
                self.set_score_at(_x, _y, self.get_score_at(x, y) + 1)
            x, y = self.find_min_unvisited_score()
        return self.get_score_at(x, y)

    def print_current_path(self):
        if not self.first_print:
            LINE_UP = '\033[1A'
            LINE_CLEAR = '\x1b[2K'
            for _ in range(self.height + 1):
                print(LINE_UP, end=LINE_CLEAR)
        else:
            self.first_print = False

        tmp = deepcopy(self.elevations)
        for y, row in enumerate(tmp):
            for x, value in enumerate(row):
                if self.visited[y][x]:
                    tmp[y][x] = '#'
        print('\n'.join(''.join(row) for row in tmp))
        max_score = max(
            max(score if score < big_int else 0 for score in row)
            for row in self.scores
        )
        print(f'Max score: {max_score}')
        time.sleep(0.005)


with open(filename, 'r') as f:
    elevation_map = ElevationMap(
        [[height for height in row if height != '\n'] for row in f]
    )

print(f'Part 1: Number of steps required: {elevation_map.find_path()}')


def opposite(s):
    if s == 'S':
        return 'E'
    if s == 'a':
        return 'E'
    if s == 'E':
        return 'S'
    i = string.ascii_lowercase.find(s)
    return string.ascii_lowercase[-i-1]


with open(filename, 'r') as f:
    elevation_map = ElevationMap(
        [[opposite(height) for height in row if height != '\n'] for row in f]
    )

print(f'Part 2: Number of steps required: {elevation_map.find_path()}')

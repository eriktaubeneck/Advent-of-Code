from dataclasses import dataclass
from enum import StrEnum
import time


class Direction(StrEnum):
    LEFT = 'L'
    RIGHT = 'R'
    UP = 'U'
    DOWN = 'D'


@dataclass
class Move:
    direction: Direction
    steps: int

    @classmethod
    def build_from_input(cls, input_str):
        direction, steps = input_str.strip().split(' ')
        return cls(Direction(direction), int(steps))


@dataclass(frozen=True)
class Position:
    x: int
    y: int


with open('input.txt', 'r') as f:
    moves = [Move.build_from_input(row) for row in f]


def build_path(moves: list[Move]) -> list[Position]:
    head: Position = Position(x=0, y=0)
    path: list[Position] = [head]

    for move in moves:
        for _ in range(move.steps):
            match move.direction:
                case Direction.LEFT:
                    head = Position(head.x-1, head.y)
                case Direction.RIGHT:
                    head = Position(head.x+1, head.y)
                case Direction.UP:
                    head = Position(head.x, head.y+1)
                case Direction.DOWN:
                    head = Position(head.x, head.y-1)
            path.append(head)
    return path


def follow_path(path: list[Position]) -> list[Position]:
    tail = Position(x=0, y=0)
    tail_path: list[Position] = [tail]
    for head in path[1:]:
        difference = (head.x - tail.x, head.y - tail.y)
        match difference:
            case (x, y) if abs(x) <= 1 and abs(y) <= 1:
                pass
            case (x, 0) if abs(x) == 2:
                tail = Position(x=tail.x+x // abs(x), y=tail.y)
            case (0, y) if abs(y) == 2:
                tail = Position(x=tail.x, y=tail.y+y // abs(y))
            case (x, y) if abs(x) <= 2 and abs(y) <= 2:
                tail = Position(x=tail.x+(x // abs(x)), y=tail.y+(y // abs(y)))
            case _:
                raise Exception(
                    f'unknown difference: {difference} '
                    f'between {head} and {tail}'
                )
        tail_path.append(tail)
    return tail_path


def print_paths(paths_lookup: dict[str, list[Position]]):
    min_x = min(pos.x for poss in paths_lookup.values() for pos in poss)
    max_x = max(pos.x for poss in paths_lookup.values() for pos in poss)
    diff_x = max_x - min_x + 1
    min_x = min_x % diff_x
    max_x = (max_x + 1) % diff_x
    min_y = min(pos.y for poss in paths_lookup.values() for pos in poss)
    max_y = max(pos.y for poss in paths_lookup.values() for pos in poss)
    diff_y = max_y - min_y + 1
    min_y = min_y % diff_y
    max_y = (max_y + 1) % diff_y

    steps = [
        zip(paths_lookup.keys(), positions)
        for positions in zip(*paths_lookup.values())
    ]
    for i, step in enumerate(steps):
        print(f'\nStep {i}')
        tmp = [['.' for _ in range(diff_x)] for _ in range(diff_y)]
        tmp[0][0] = 's'
        for k, pos in list(step)[::-1]:
            tmp[pos.y][pos.x] = k

        print(
            '\n'.join(
                ''.join(p for p in row[max_x:]+row[:min_x])
                for row in tmp[max_y:]+tmp[:min_y]
            )
        )
        LINE_UP = '\033[1A'
        LINE_CLEAR = '\x1b[2K'
        time.sleep(0.02)
        if i < len(steps)-1:
            for _ in range(diff_y + 2):
                print(LINE_UP, end=LINE_CLEAR)


head_path = build_path(moves)
tail_path = follow_path(head_path)
paths = {'H': head_path, '1': tail_path}

print(f'Tail visitied {len(set(tail_path))} unique positions.')

for i in range(2, 10):
    paths[str(i)] = follow_path(paths[str(i-1)])
# print_paths(paths)

print(f'Tail 9 visitied {len(set(paths["9"]))} unique positions.')

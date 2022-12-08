grid = []

with open('input.txt', 'r') as f:
    for row in f:
        grid.append([int(v) for v in row.strip('\n')])

width = len(grid[0])
depth = len(grid)


def is_edge(grid, location):
    x, y = location
    if x in [0, width-1] or y in [0, depth-1]:
        return True
    return False


def column(grid, column):
    return [row[column] for row in grid]


def up(grid, location):
    x, y = location
    return column(grid, x)[y-1::-1]


def down(grid, location):
    x, y = location
    return column(grid, x)[y+1:]


def left(grid, location):
    x, y = location
    return grid[y][x-1::-1]


def right(grid, location):
    x, y = location
    return grid[y][x+1:]


def is_visable(grid, location):
    if is_edge(grid, location):
        return True
    x, y = location
    trees_to_compare = [
        max(up(grid, location)),
        max(down(grid, location)),
        max(left(grid, location)),
        max(right(grid, location)),
    ]
    if grid[y][x] <= min(trees_to_compare):
        return False
    return True


def scenic_score(grid, location):
    if is_edge(grid, location):
        return 0
    x, y = location
    trees_to_compare = [
        up(grid, location),
        down(grid, location),
        left(grid, location),
        right(grid, location),
    ]
    score = 1
    for direction in trees_to_compare:
        for i, tree in enumerate(direction):
            if grid[y][x] <= tree or i + 1 == len(direction):
                score *= (i + 1)
                break
    return score


locations = [(x, y) for x in range(width) for y in range(depth)]
print(f'Grid is {width}x{depth}, with {len(locations)} locations')

visable_trees = sum(is_visable(grid, location) for location in locations)
print(f'Total trees visable: {visable_trees}')


max_score = max(scenic_score(grid, location) for location in locations)
print(f'Maximum scenic score: {max_score}')

import math

class Monkey:
    def __init__(
            self,
            starting_items: list[int],
            divisible_test: int,
            throw_to_monkeys: tuple[int, int],
            operation: callable,
            part_one: bool,
    ):
        self.items = starting_items
        self.divisible_test = divisible_test
        self.operation = operation
        self.throw_to_monkeys = throw_to_monkeys
        self.items_inspected = 0
        self.part_one = part_one

    def __repr__(self):
        return f'<Monkey: items_inspected: {self.items_inspected}, items: {self.items}>'

    def set_monkey_lookup(self, monkey_lookup: dict[int, 'Monkey']):
        self.monkey_lookup = monkey_lookup
        if not self.part_one:
            self.divisor = math.prod(
                [monkey.divisible_test for monkey in monkey_lookup.values()]
            )

    def test(self, item: int) -> bool:
        return item % self.divisible_test == 0

    def recieve(self, item: int):
        self.items.append(item)

    def send(self, item: int, monkey: int):
        self.monkey_lookup[monkey].recieve(item)

    def turn(self):
        while self.items:
            item = self.items.pop()
            # print(f'inspecting item with worry level {item}')
            self.items_inspected += 1
            item = self.operation(item)
            # print(f'updating worry level to {item}')
            if self.part_one:
                item = item // 3
            else:
                item = item % self.divisor
            # print(f'dividing by three to {item}')
            if self.test(item):
                # print(f'item is divisible by {self.divisible_test}')
                # print(f'sending to {self.throw_to_monkeys[0]}')
                self.send(item, self.throw_to_monkeys[0])
            else:
                # print(f'item is not divisible by {self.divisible_test}')
                # print(f'sending to {self.throw_to_monkeys[1]}')
                self.send(item, self.throw_to_monkeys[1])


def build_monkeys(part_one):
    # Example
    # monkeys = {
    #     0: Monkey(
    #         [79, 98],
    #         23,
    #         (2, 3),
    #         lambda x: x * 19,
    #         part_one,
    #     ),
    #     1: Monkey(
    #         [54, 65, 75, 74],
    #         19,
    #         (2, 0),
    #         lambda x: x + 6,
    #         part_one,
    #     ),
    #     2: Monkey(
    #         [79, 60, 97],
    #         13,
    #         (1, 3),
    #         lambda x: x * x,
    #         part_one,
    #     ),
    #     3: Monkey(
    #         [74],
    #         17,
    #         (0, 1),
    #         lambda x: x + 3,
    #         part_one,
    #     ),
    # }

    monkeys = {
        0: Monkey(
            [89, 74],
            17,
            (4, 7),
            lambda x: x * 5,
            part_one,
        ),
        1: Monkey(
            [75, 69, 87, 57, 84, 90, 66, 50],
            7,
            (3, 2),
            lambda x: x + 3,
            part_one,
        ),
        2: Monkey(
            [55],
            13,
            (0, 7),
            lambda x: x + 7,
            part_one,
        ),
        3: Monkey(
            [69, 82, 69, 56, 68],
            2,
            (0, 2),
            lambda x: x + 5,
            part_one,
        ),
        4: Monkey(
            [72, 97, 50],
            19,
            (6, 5),
            lambda x: x + 2,
            part_one,
        ),
        5: Monkey(
            [90, 84, 56, 92, 91, 91],
            3,
            (6, 1),
            lambda x: x * 19,
            part_one,
        ),
        6: Monkey(
            [63, 93, 55, 53],
            5,
            (3, 1),
            lambda x: x * x,
            part_one,
        ),
        7: Monkey(
            [50, 61, 52, 58, 86, 68, 97],
            11,
            (5, 4),
            lambda x: x + 4,
            part_one,
        ),
    }
    for monkey in monkeys.values():
        monkey.set_monkey_lookup(monkeys)
    return monkeys


def run_rounds(rounds):
    for _ in range(rounds):
        print(f'round {_}')
        for i, monkey in monkeys.items():
            # print(i, monkey)
            monkey.turn()

    print({k: v.items_inspected for k, v in monkeys.items()})

    two_highest_inspections = sorted(v.items_inspected for v in monkeys.values())[-2:]

    print(
        f'Level of monkey business: '
        f'{two_highest_inspections[0] * two_highest_inspections[1]}'
    )


monkeys = build_monkeys(True)
print('part 1\n')
rounds = 20
run_rounds(rounds)


monkeys = build_monkeys(False)

print('\npart 2\n')
rounds = 10000
run_rounds(rounds)

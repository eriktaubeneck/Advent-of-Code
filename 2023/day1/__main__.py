numbers = "1234567890"

spelled_numbers = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "zero": "0",
}


def part1():
    _sum = 0
    with open("day1/input.txt", "r") as puzzle_input:
        for line in puzzle_input:
            line_numbers = [c for c in line if c in numbers]
            first = line_numbers[0]
            last = line_numbers[-1]
            calibration_value = int(first + last)
            _sum += calibration_value
    return _sum


def part2():
    _sum = 0
    with open("day1/input.txt", "r") as puzzle_input:
        for line in puzzle_input:
            line_numbers = []
            for i in range(len(line)):
                if line[i] in numbers:
                    line_numbers.append(line[i])
                else:
                    for spelled_number in spelled_numbers.keys():
                        if line[i:].startswith(spelled_number):
                            line_numbers.append(spelled_numbers[spelled_number])
            first = line_numbers[0]
            last = line_numbers[-1]
            calibration_value = int(first + last)
            _sum += calibration_value
    return _sum


if __name__ == "__main__":
    print(f"part1: {part1()}")
    print(f"part2: {part2()}")

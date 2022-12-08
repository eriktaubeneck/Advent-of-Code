import pprint

current_path = []


class Directory(dict):
    size = 0

    def __getitem__(self, path):
        for sub_path in path:
            self = dict.__getitem__(self, sub_path)
        return self

    def __setitem__(self, path, value):
        self.size += value
        for sub_path in path[:-1]:
            self = dict.__getitem__(self, sub_path)
            self.size += value
        dict.__setitem__(self, path[-1], value)

    def create_sub_directory(self, path, new_sub_path):
        parent = self
        for sub_path in path:
            self = dict.__getitem__(self, sub_path)
        if new_sub_path in self.keys():
            raise Exception(
                f'{".".join(path)}.{new_sub_path} '
                f'already exists in {parent}'
            )
        dict.__setitem__(self, new_sub_path, Directory())

    def __add__(self, other):
        if type(other) is Directory:
            return self.size + other.size
        else:
            return self.size + other

    def sum_all_directories_less_than(self, value):
        _sum = 0
        if self.size <= value:
            _sum += self.size
        for k, v in self.items():
            if type(v) is Directory:
                _sum += v.sum_all_directories_less_than(value)
        return _sum

    def all_sizes_greater_than(self, value):
        sizes = []
        if self.size >= value:
            sizes.append(self.size)
        for k, v in self.items():
            if type(v) is Directory:
                sizes.extend(v.all_sizes_greater_than(value))
        return sizes


directory = Directory()
directory.create_sub_directory([], '/')


with open('input.txt', 'r') as f:
    for line in f:
        commands = line.strip('\n').split(' ')
        if commands[0] == '$':
            if commands[1] == 'cd':
                # this handles cd commands
                if commands[2] == '..':
                    current_path.pop()
                else:
                    current_path.append(commands[2])
            elif commands[1] == 'ls':
                # this handles ls commands
                pass
        elif commands[0] == 'dir':
            # this handles dir responses
            directory.create_sub_directory(current_path, commands[1])
        else:
            # this handles file responses
            current_dir = directory[current_path+[commands[1]]] = int(commands[0])


print(
    f'Sum of directories less than 100,000: '
    f'{directory.sum_all_directories_less_than(100_000):,}'
)

total_disk_space = 70_000_000
space_required = 30_000_000

space_available = total_disk_space - directory.size
need_to_delete = space_required - space_available

print(
    f'There is {space_available:,} space_availabble, '
    f'so we need to delete {need_to_delete:,}'
)

sizes = directory.all_sizes_greater_than(need_to_delete)
print(f'The smallest directory we can delete has size {min(sizes):,}')

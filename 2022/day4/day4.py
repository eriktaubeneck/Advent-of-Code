with open('input.txt', 'r') as f:
    assignment_pairs = (
        tuple(
            tuple(
                int(bound) for bound in assignment.split('-')
            )
            for assignment in row.split(',')
        )
        for row in f
    )

    fully_overlapping_counter = 0
    any_overlap_counter = 0

    for (start_1, end_1), (start_2, end_2) in assignment_pairs:
        if start_1 <= start_2 and end_1 >= end_2:
            fully_overlapping_counter += 1
        elif start_1 >= start_2 and end_1 <= end_2:
            fully_overlapping_counter += 1

        if len(set(range(start_1, end_1+1)) & set(range(start_2, end_2+1))) > 0:
            any_overlap_counter += 1


print(f'{fully_overlapping_counter} assignment pairs fully overlap each other')
print(f'{any_overlap_counter} assignment pairs have any overlap with each other')

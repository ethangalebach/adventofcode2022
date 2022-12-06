import os

SHAPE_SUBSCORES = {
    'X': 1,
    'Y': 2,
    'Z': 3
}

REBASE = {
    'X': 'A',
    'Y': 'B',
    'Z': 'C'
}

CYCLE = ['A','B','C']

def get_outcome_subscore(your_shape, my_shape) -> int:
    my_rebased_shape = REBASE.get(my_shape)
    if your_shape == my_rebased_shape:
        return 3
    else:
        for i in range(len(CYCLE)+1):
            if CYCLE[i-1] == your_shape and CYCLE[i] == my_rebased_shape:
                return 6
            if CYCLE[i-1] == my_rebased_shape and CYCLE[i] == your_shape:
                return 0

def get_part1_answer(input_path: str) -> float:
    total_score = 0

    with open(input_path) as f:
        for num, line in enumerate(f,1):
            if not line.strip():
                continue
            your_shape = line[0]
            my_shape = line[-2]
            total_score += SHAPE_SUBSCORES.get(my_shape)
            total_score += get_outcome_subscore(your_shape, my_shape)

    return total_score

def get_part2_answer(input_path: str) -> float:
    pass

if __name__ == "__main__":
    filename = os.path.basename(__file__)
    filename = filename.removesuffix('.py') + '.txt'
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    input_path = file_name = os.path.join(file_dir, f'input/{filename}')

    part1_answer = get_part1_answer(input_path)
    part2_answer = get_part2_answer(input_path)

    print(
        f"Part 1 Answer: {part1_answer},",
        f"Part 2 Answer: {part2_answer}"
    )
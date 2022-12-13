import utils

SHAPE_SUBSCORES = {'A': 1, 'B': 2, 'C': 3}

REBASE = {'X': 'A', 'Y': 'B', 'Z': 'C'}

DIFF = {'X': -1, 'Y': 0, 'Z': -2}

CYCLE = ['A','B','C']

def get_outcome_subscore(your_shape, my_shape) -> int:
    if your_shape == my_shape:
        return 3
    else:
        for i in range(len(CYCLE)+1):
            if CYCLE[i-1] == your_shape and CYCLE[i] == my_shape:
                return 6
            if CYCLE[i-1] == my_shape and CYCLE[i] == your_shape:
                return 0

def get_answer(input_path: str, part: int) -> float:
    total_score = 0

    with open(input_path) as f:
        for line in f:
            your_shape = line[0]
            if part == 1:
                my_shape = REBASE.get(line[-2])
            elif part == 2:
                my_diff = DIFF.get(line[-2])
                my_shape = CYCLE[CYCLE.index(your_shape) + my_diff]
            else:
                raise Exception('not part 1 or 2')
            total_score += SHAPE_SUBSCORES.get(my_shape)
            total_score += get_outcome_subscore(your_shape, my_shape)

    return total_score

if __name__ == "__main__":
    input_path = utils.get_input_path(__file__)
    part1_answer = get_answer(input_path, part=1)
    part2_answer = get_answer(input_path, part=2)

    print(
        f"Part 1 Answer: {part1_answer},",
        f"Part 2 Answer: {part2_answer}"
    )
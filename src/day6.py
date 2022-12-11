import utils

def create_stacks(stack_rows: list) -> dict:
    pass


def get_answer(input_path: str, part: int) -> str:
    total_score = 0

    with open(input_path) as f:
        line = f.readline()
        if part == 1:
            for end_index in range(4, len(line)):
                possible_marker = line[end_index-4:end_index]
                if len(set(possible_marker)) == 4:
                    total_score = end_index
                    break
        elif part == 2:
            pass
        else:
            raise Exception('not part 1 or 2')

    return total_score

if __name__ == "__main__":
    input_path = utils.get_input_path(__file__)
    part1_answer = get_answer(input_path, part=1)
    part2_answer = get_answer(input_path, part=2)

    print(
        f"Part 1 Answer: {part1_answer},",
        f"Part 2 Answer: {part2_answer}"
    )
import utils

def get_answer(input_path: str, part: int) -> str:
    total_score = 0
    if part == 1:
        marker_length = 4
    elif part == 2:
        marker_length = 14
    else:
        raise Exception('not part 1 or 2')

    with open(input_path) as f:
        line = f.readline()

    for end_index in range(marker_length, len(line)):
        possible_marker = line[end_index-marker_length:end_index]
        if len(set(possible_marker)) == marker_length:
            total_score = end_index
            break

    return total_score

if __name__ == "__main__":
    input_path = utils.get_input_path(__file__)
    part1_answer = get_answer(input_path, part=1)
    part2_answer = get_answer(input_path, part=2)

    print(
        f"Part 1 Answer: {part1_answer},",
        f"Part 2 Answer: {part2_answer}"
    )
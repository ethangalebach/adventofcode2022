import utils

def has_overlap(line: str, overlap_type: str) -> int:
    overlap = 0
    pair_of_sections = str.split(line,',')
    if len(pair_of_sections) != 2:
        raise Exception(f'pair_of_sections is not a pair: {pair_of_sections}')
    first_range_start, first_range_end = str.split(pair_of_sections[0],'-')
    second_range_start, second_range_end = str.split(pair_of_sections[1],'-')

    if overlap_type == 'full' and (
        (
            int(first_range_start) <= int(second_range_start) and
            int(second_range_end) <= int(first_range_end)
        ) or (
            int(second_range_start) <= int(first_range_start) and
            int(first_range_end) <= int(second_range_end)
        )
    ):
        overlap = 1

    if overlap_type == 'any' and (
        max(int(first_range_start), int(second_range_start)) <=
        min(int(first_range_end), int(second_range_end))
    ):
        overlap = 1

    return overlap

def get_answer(input_path: str, part: int) -> float:
    total_score = 0
    if part == 1:
        overlap_type = 'full'
    elif part == 2:
        overlap_type = 'any'
    else:
        raise Exception('not part 1 or 2')

    with open(input_path) as f:
        for line in f:
            overlap = has_overlap(line, overlap_type)
            total_score += overlap
    return total_score

if __name__ == "__main__":
    input_path = utils.get_input_path(__file__)
    part1_answer = get_answer(input_path, part=1)
    part2_answer = get_answer(input_path, part=2)

    print(
        f"Part 1 Answer: {part1_answer},",
        f"Part 2 Answer: {part2_answer}"
    )
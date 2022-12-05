import os
import bisect

def get_part1_answer(input_path: str) -> float:
    max_calories = 0
    cur_elf_calories = 0

    with open(input_path) as f:
        for line in f:
            if line.strip():
                cur_elf_calories += int(line)
            else:
                if cur_elf_calories > max_calories:
                    max_calories = cur_elf_calories
                cur_elf_calories = 0

    return max_calories

def get_part2_answer(input_path: str, n_elves: int) -> float:
    top_n_calories = [0] * n_elves
    cur_elf_calories = 0

    with open(input_path) as f:
        for line in f:
            if line.strip():
                cur_elf_calories += int(line)
            else:
                bisect.insort(top_n_calories, cur_elf_calories)
                top_n_calories.pop(0)
                cur_elf_calories = 0

    return sum(top_n_calories)

if __name__ == "__main__":
    filename = os.path.basename(__file__)
    filename = filename.removesuffix('.py') + '.txt'
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    input_path = file_name = os.path.join(file_dir, f'input/{filename}')

    part1_answer = get_part1_answer(input_path)
    part2_answer = get_part2_answer(input_path, 3)

    print(
        f"Part 1 Answer: {part1_answer},",
        f"Part 2 Answer: {part2_answer}"
    )
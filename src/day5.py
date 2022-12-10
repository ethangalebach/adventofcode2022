import utils

def create_stacks (stack_rows: list) -> dict:
    keys_line = stack_rows.pop()
    stacks = {keys_line[i]:[] for i in range(len(keys_line)) if (i + 3) % 4 == 0}

    while stack_rows:
        bottom_crates = stack_rows.pop()
        for i in range(len(bottom_crates)):
            if (i + 3) % 4 == 0 and bottom_crates[i] != ' ':
                stacks[str((i+3)//4)].append(bottom_crates[i])

    return stacks

def get_answer(input_path: str, part: int) -> str:
    stacks = {}
    stack_rows = []
    below_stacks = 0
    if part == 1:
        with open(input_path) as f:
            for line in f:
                if not below_stacks:
                    stack_rows.append(line)
                    if line[1] == '1':
                        stacks = create_stacks(stack_rows)
                        below_stacks = 1
                elif line.strip():
                    _, num_crates, _, from_stack, _, to_stack = str.split(line.strip(),' ')
                    for i in range(int(num_crates)):
                        crate = stacks[from_stack].pop()
                        stacks[to_stack].append(crate)
    elif part == 2:
        pass
    else:
        raise Exception('not part 1 or 2')

    return ''.join([stacks[k].pop() for k in stacks])



if __name__ == "__main__":
    input_path = utils.get_input_path(__file__)
    part1_answer = get_answer(input_path, part=1)
    part2_answer = get_answer(input_path, part=2)

    print(
        f"Part 1 Answer: {part1_answer},",
        f"Part 2 Answer: {part2_answer}"
    )
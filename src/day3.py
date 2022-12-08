import utils

def get_priority(item: str) -> int:
    ascii_value = ord(item)
    if ascii_value in range(65,91):
        return ascii_value - 38
    elif ascii_value in range(97,123):
        return ascii_value - 96
    else:
        raise Exception(f'ASCII value of item not in alphabet: {ascii_value} {item}')

def get_shared_item(rucksack: str) -> str:
    rucksack_size = len(rucksack)
    if rucksack_size % 2 != 0:
        raise Exception(f'odd size of rucksack: {rucksack_size}; rucksack: {rucksack}')
    compartment_size = int(rucksack_size / 2)
    compartment1 = rucksack[:compartment_size]
    compartment2 = rucksack[compartment_size:]
    shared_items = set(compartment1) & set(compartment2)
    if len(shared_items) == 1:
        return shared_items.pop()
    else:
        raise Exception('more or less than one shared item')

def get_answer(input_path: str, part: int) -> float:
    total_score = 0

    with open(input_path) as f:
        for line in f:
            if part == 1:
                shared_item = get_shared_item(line.strip())
                priority = get_priority(shared_item)
                total_score += priority
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
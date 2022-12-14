import utils

def print_crt_image(path:str):
    cycle = 0
    register = 1
    row = []
    with open(path) as f:
        for line in f:
            pixels = 2 if line.startswith('addx') else 1
            for i in range(pixels):
                if cycle in range(register-1, register+2):
                    row.append('#')
                else:
                    row.append('.')
                cycle += 1
                if cycle % 40 == 0:
                        cycle = 0
                        print(' '.join(row))
                        row = []
            if line.startswith('addx'):
                register += int(str.split(line.strip())[1])

def get_signal_strength(path:str):
    cycle = 0
    register = 1
    signal_strength = 0
    with open(path) as f:
        for line in f:
            cycle += 1
            if (cycle / 20 - 1) % 2 == 0:
                    signal_strength += cycle * register
            if line.startswith('addx'):
                cycle += 1
                if (cycle / 20 - 1) % 2 == 0:
                    signal_strength += cycle * register
                register += int(str.split(line.strip())[1])
    return signal_strength

def get_answer(path:str, part:int) -> int:
    if part == 1:
        return get_signal_strength(path)
    elif part == 2:
        pass
    else:
        raise Exception('not part 1 or 2')

if __name__ == "__main__":
    input_path = utils.get_input_path(__file__)
    test_path = utils.get_test_path(__file__)
    test_answer = get_answer(test_path, part=1)
    assert test_answer == 13140, f"got signal strength of {test_answer} on {test_path}, should be 13140"
    part1_answer = get_answer(input_path, part=1)

    print(
        f"Part 1 Answer: {part1_answer},",
        f"Part 2 Answer:",
    )
    print_crt_image(input_path)

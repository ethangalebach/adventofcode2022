import os

def get_answer(input_path: str) -> float:
    answer = 0
    cur_elf = 0

    with open(input_path) as f:
        for line in f:
            if line.strip():
                cur_elf += int(line)
            else:
                if cur_elf > answer:
                    answer = cur_elf
                cur_elf = 0

    return answer

if __name__ == "__main__":
    filename = os.path.basename(__file__)
    filename = filename.removesuffix('.py') + '.txt'
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    input_path = file_name = os.path.join(file_dir, f'input/{filename}')
    answer = get_answer(input_path)
    print(answer)
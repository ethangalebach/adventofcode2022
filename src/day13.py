import utils
import ast

class DistressSignal:
    def __init__(self, path:str):
        self.packet_pairs = self.parse_signal(path)

    def parse_signal(self, path:str):
        packet_pairs = []
        pair_line_no = 0
        with open(path) as f:
            for line in f:
                if not line.strip():
                    continue
                elif pair_line_no == 0:
                    left = ast.literal_eval(line.strip())
                    pair_line_no += 1
                elif pair_line_no == 1:
                    right = ast.literal_eval(line.strip())
                    packet_pairs.append((left,right))
                    pair_line_no = 0
        return packet_pairs

    def indices_of_correct_pairs(self):
        indices =[]
        for idx, pair in enumerate(self.packet_pairs):
            if self.is_correctly_ordered(*pair):
                indices.append(idx+1)
        return indices

    def is_correctly_ordered(self, left, right):
        if isinstance(left, int) and isinstance(right, int):
            return right - left + 0.5
        elif isinstance(left, int):
            if right == []: return False
            return self.is_correctly_ordered([left],right)
        elif isinstance(right, int):
            if left == []: return True
            return self.is_correctly_ordered(left,[right])
        else:
            for i in range(len(left)):
                if i == len(right): return False
                res = self.is_correctly_ordered(left[i],right[i])
                if res <= 0: return False
                if res >= 1: return True
            return 0.5 if len(right) == len(left) else True

def get_answer(input_path:str, part:int) -> int:
    if part == 1:
        signal = DistressSignal(input_path)
        return sum(signal.indices_of_correct_pairs())
    elif part == 2:
        pass
    else:
        raise Exception('not part 1 or 2')

if __name__ == "__main__":
    input_path = utils.get_input_path(__file__)
    test_path = utils.get_test_path(__file__)
    test_answer = get_answer(test_path, part=1)
    assert test_answer == 13, f"got index sum of {test_answer} on {test_path}, should be 13"
    part1_answer = get_answer(input_path, part=1)
    part2_answer = get_answer(input_path, part=2)

    print(
        f"Part 1 Answer: {part1_answer},",
        f"Part 2 Answer: {part2_answer}"
    )
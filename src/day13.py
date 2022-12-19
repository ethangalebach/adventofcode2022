import utils
import ast
import bisect
from functools import cmp_to_key

class DistressSignal:
    def __init__(self, path:str):
        self.path = path
        self.packet_pairs = self._parse_packet_pairs()
        self.sorted_packets = self._sort_packets()

    def get_indices_of_correct_pairs(self):
        indices =[]
        packet_pairs = self._parse_packet_pairs()
        for idx, pair in enumerate(packet_pairs):
            if self._is_correctly_ordered(*pair):
                indices.append(idx+1)
        return indices

    def get_decoder_key(self):
        two_index = self.sorted_packets.index([[2]])
        six_index = self.sorted_packets.index([[6]])
        return (two_index+1)*(six_index+1)

    def _sort_packets(self):
        sorted_packets = [[[2]],[[6]]]
        cmp_func = lambda left, right: 0.5 - self._is_correctly_ordered(left, right)
        with open(self.path) as f:
            for line in f:
                if not line.strip(): continue
                packet = ast.literal_eval(line.strip())
                bisect.insort(sorted_packets, packet, key = cmp_to_key(cmp_func))
        return sorted_packets

    def _parse_packet_pairs(self):
        packet_pairs = []
        pair_line_no = 0
        with open(self.path) as f:
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

    def _is_correctly_ordered(self, left, right):
        """
        Returns:
        1 (True) if left < right,
        0 (False) if left > right,
        0.5 if left == right
        """
        if isinstance(left, int) and isinstance(right, int):
            return right - left + 0.5
        elif isinstance(left, int):
            if right == []: return False
            return self._is_correctly_ordered([left],right)
        elif isinstance(right, int):
            if left == []: return True
            return self._is_correctly_ordered(left,[right])
        else:
            for i in range(len(left)):
                if i == len(right): return False
                res = self._is_correctly_ordered(left[i],right[i])
                if res <= 0: return False
                if res >= 1: return True
            return 0.5 if len(right) == len(left) else True

def get_answer(input_path:str, part:int) -> int:
    signal = DistressSignal(input_path)
    if part == 1:
        return sum(signal.get_indices_of_correct_pairs())
    elif part == 2:
        return signal.get_decoder_key()
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
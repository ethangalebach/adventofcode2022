import utils
from itertools import cycle

class File:
    def __init__(self, path:str):
        self.start_list = self._parse_graph(path)
        self.length = len(self.start_list)

    def _parse_graph(self, path):
        start_list = []
        with open(path) as f:
            for line in f:
                if line.strip():
                    start_list.append(int(line))
        return start_list

    def get_grove_coords(self):
        mixed_list = self._mix()
        zero_idx = mixed_list.index('a0')
        first_coord = mixed_list[(1000 + zero_idx) % self.length]
        second_coord = mixed_list[(2000 + zero_idx) % self.length]
        third_coord = mixed_list[(3000 + zero_idx) % self.length]
        return int(first_coord[1:]) + int(second_coord[1:]) + int(third_coord[1:])

    def _mix(self):
        mixed_list = self.start_list.copy()
        for item in self.start_list:
            idx = mixed_list.index(item)
            _ = mixed_list.pop(idx)
            while idx+item <= 0:
                idx += self.length-1
            while idx+item >= self.length:
                idx = idx-self.length+1
            mixed_list.insert(idx+item, 'a'+str(item))
        return mixed_list

def get_answer(input_path:str, part:int) -> int:
    file = File(input_path)
    if part == 1:
        return file.get_grove_coords()
    elif part == 2:
        pass
    else:
        raise Exception('not part 1 or 2')

if __name__ == "__main__":
    input_path = utils.get_input_path(__file__)
    test_path = utils.get_test_path(__file__)
    test_part1_answer = get_answer(test_path, part=1)
    assert test_part1_answer == 3, f"got sum of grove coordinates as {test_part1_answer} on {test_path}, should be 3"
    part1_answer = get_answer(input_path, part=1)
    # test_part2_answer = get_answer(test_path, part=2)
    # assert test_part2_answer == 1707, f"got max pressure of {test_part2_answer} on {test_path}, should be 1707"
    # part2_answer = get_answer(input_path, part=2)

    print(
        f"Test Part 1 Answer: {test_part1_answer},",
        f"Part 1 Answer: {part1_answer},",
        # f"Test Part 2 Answer: {test_part2_answer},",
        # f"Part 2 Answer: {part2_answer}"
    )
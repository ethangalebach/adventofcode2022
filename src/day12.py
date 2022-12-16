import utils
from itertools import product

class Map:
    def __init__(self, path:str):
        self.cur_coord = (None, None)
        self.target_coord = (None, None)
        self.map = self._parse_map(path)

    def _parse_map(self, path):
        heights = []
        with open(path) as f:
            for line in f:
                row = list(line.strip())
                for col, c in enumerate(row):
                    if c == 'S':
                        self.cur_coord = (len(heights), col)
                        row[col] = 'a'
                    if c == 'E':
                        self.target_coord = (len(heights), col)
                        row[col] = 'z'
                heights.append(row)

        return self._create_map(heights)

    def _create_map(self, heights):
        num_rows = len(heights)
        num_cols = len(heights[0])
        map = [[None] * num_cols] * num_rows
        for i,j in product(range(num_rows), range(num_cols)):
            left = heights[i][j-1] if j > 0 else None
            right = heights[i][j+1] if j < num_cols-1 else None
            up = heights[i-1][j] if i == 0 else None
            down = heights[i+1][j] if i < num_rows-1 else None
            map[i][j] = Point(heights[i][j],left,right,up,down)

    def get_shortest_path(self):
        shortest_path = []
        #TODO
        return shortest_path


class Point:
    def __init__(self,height,left,right,up,down):
        self.height = height
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.ranks = self._calc_ranks()
        self.pref_order =  [k for k, _ in sorted(self.ranks.items(), key=lambda item: item[1])]

    def _calc_ranks(self):
        ranks = {}
        ranks['left'] = max(ord(self.height) - ord(self.left) + 1, -1) if self.left else -1
        ranks['right'] = max(ord(self.height) - ord(self.right) + 1, -1) if self.right else -1
        ranks['up'] = max(ord(self.height) - ord(self.up) + 1, -1) if self.up else -1
        ranks['down'] = max(ord(self.height) - ord(self.down) + 1, -1) if self.down else -1
        return ranks

def get_answer(input_path: str, part: int) -> int:
    if part == 1:
        map = Map(input_path)
        return map.target_coord
    elif part == 2:
        pass
    else:
        raise Exception('not part 1 or 2')

if __name__ == "__main__":
    input_path = utils.get_input_path(__file__)
    part1_answer = get_answer(input_path, part=1)
    part2_answer = get_answer(input_path, part=2)

    print(
        f"Part 1 Answer: {part1_answer},",
        f"Part 2 Answer: {part2_answer}"
    )

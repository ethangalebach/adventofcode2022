import utils
from itertools import product

class Grid:
    def __init__(self, height_grid:list):
        self.height_grid = height_grid
        self.width = len(height_grid)

    def get_count_of_visible_trees(self) -> int:
        count = 0
        for i,j in product(range(self.width), repeat=2):
            count += self._is_visible(i,j)
        return count

    def _is_visible(self, row_index, col_index) -> bool:
        tree_height = self.height_grid[row_index][col_index]
        if row_index in (0,self.width-1) or col_index in (0,self.width-1):
            return True

        #min of max tree height in each direction
        if tree_height > min(
            max(self.height_grid[row_index][:col_index]),
            max(self.height_grid[row_index][col_index+1:]),
            max([self.height_grid[r][col_index] for r in range(row_index)]),
            max([self.height_grid[r][col_index] for r in range(row_index+1,self.width)])
        ):
            return True

        return False

def build_grid(input_path:str) -> Grid:
    height_grid = []
    n = 0

    with open(input_path) as f:
        for line in f:
            if line.strip():
                height_grid.append([int(x) for x in line.strip()])
                if len(height_grid) == 1:
                    n = len(height_grid[0])
                else:
                    if n != len(line.strip()):
                        raise Exception('not a grid')

    return Grid(height_grid)

def get_answer(input_path: str, part: int) -> str:
    if part == 1:
        grid = build_grid(input_path)
        return grid.get_count_of_visible_trees()
    elif part == 2:
        pass
    else:
        raise Exception('not part 1 or 2')

    with open(input_path) as f:
        line = f.readline()

if __name__ == "__main__":
    input_path = utils.get_input_path(__file__)
    part1_answer = get_answer(input_path, part=1)
    part2_answer = get_answer(input_path, part=2)

    print(
        f"Part 1 Answer: {part1_answer},",
        f"Part 2 Answer: {part2_answer}"
    )
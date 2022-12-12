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

    def _calc_scenic_score(self, row_index:int, col_index:int) -> int:
        tree_height = self.height_grid[row_index][col_index]
        score = 1
        for east_distance in range(1,col_index+1):
            if east_distance == col_index or self.height_grid[row_index][col_index] <= self.height_grid[row_index][col_index-east_distance]:
                score *= east_distance
                break
        for west_distance in range(1,self.width-col_index):
            if west_distance == self.width-col_index-1 or tree_height <= self.height_grid[row_index][col_index+west_distance]:
                score *= west_distance
                break
        for north_distance in range(1,row_index+1):
            if north_distance == row_index or tree_height <= self.height_grid[row_index-north_distance][col_index]:
                score *= north_distance
                break
        for south_distance in range(1,self.width-row_index):
            if south_distance == self.width-row_index-1 or tree_height <= self.height_grid[row_index+south_distance][col_index]:
                score *= south_distance
                break
        return score

    def get_max_scenic_score(self) -> int:
        max_scenic_score = 0
        for row_index,col_index in product(range(1, self.width-1),repeat=2):
            max_scenic_score = max(max_scenic_score,self._calc_scenic_score(row_index, col_index))
        return max_scenic_score

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
    grid = build_grid(input_path)
    if part == 1:
        return grid.get_count_of_visible_trees()
    elif part == 2:
        return grid.get_max_scenic_score()
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
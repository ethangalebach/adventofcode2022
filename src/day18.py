import utils
import numpy as np

class ObsidianGrid:
    def __init__(self, path:str):
        self.droplet_locs = self._parse_graph(path)

    def _parse_graph(self, path):
        droplet_locs = np.empty((0,3),dtype=int)
        with open(path) as f:
            for line in f:
                if line.strip():
                    coords = list(map(int,str.split(line, ',')))
                    droplet_locs = np.vstack((droplet_locs, coords))
        return droplet_locs

    def get_surface_area(self):
        area = 0
        grid = np.zeros(self.droplet_locs.max(axis=0)+1,dtype=int)
        for x,y,z in self.droplet_locs:
            area += 6
            area -= self._get_adjacency_penalty(grid, x, y, z)
            grid[x,y,z] += 1
        return area

    def _get_adjacency_penalty(self, grid, x, y, z):
        adjacency_count = 0
        if grid.shape[0] > x+1:
            adjacency_count += grid[x+1,y,z]
        if x > 0:
            adjacency_count += grid[x-1,y,z]
        if grid.shape[1] > y+1:
            adjacency_count += grid[x,y+1,z]
        if y > 0:
            adjacency_count += grid[x,y-1,z]
        if grid.shape[2] > z+1:
            adjacency_count += grid[x,y,z+1]
        if z > 0:
            adjacency_count += grid[x,y,z-1]
        return 2*adjacency_count

def get_answer(input_path:str, part:int) -> int:
    og = ObsidianGrid(input_path)
    if part == 1:
        with open(input_path) as f:
            return og.get_surface_area()
    elif part == 2:
        return og
    else:
        raise Exception('not part 1 or 2')

if __name__ == "__main__":
    input_path = utils.get_input_path(__file__)
    test_path = utils.get_test_path(__file__)
    test_part1_answer = get_answer(test_path, part=1)
    assert test_part1_answer == 64, f"got surface area of {test_part1_answer} on {test_path}, should be 64"
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
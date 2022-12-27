import utils

class Grid:
    def __init__(self, path):
        self.rock_grid, self.abyss_height = self._parse_rock_grid(path)
        self.sand_grid = {}

    def _parse_rock_grid(self, path):
        rock_grid = {}
        abyss_height = 0
        with open(path) as f:
            for line in f:
                coords = str.split(line, ' -> ')
                for i in range(len(coords)-1):
                    x1, y1 = map(int,str.split(coords[i],','))
                    x2, y2 = map(int,str.split(coords[i+1],','))
                    if x1 == x2 and y2 >= y1:
                        for j in range(y1,y2+1):
                            rock_grid[(x1,j)] = '#'
                    elif x1 == x2 and y2 < y1:
                        for j in range(y2,y1+1):
                            rock_grid[(x1,j)] = '#'
                    elif y1 == y2 and x2 >= x1:
                        for j in range(x1,x2+1):
                            rock_grid[(j,y1)] = '#'
                    elif y1 == y2 and x2 < x1:
                        for j in range(x2,x1+1):
                            rock_grid[(j,y1)] = '#'
                    abyss_height = max(abyss_height, y1, y2)
        return rock_grid, abyss_height

    def _fall(self, loc):
        down = (loc[0], loc[1]+1)
        downleft = (loc[0]-1,loc[1]+1)
        downright = (loc[0]+1,loc[1]+1)
        if self.rock_grid.get(down) != '#' and self.sand_grid.get(down) != 'o':
            new_loc = down
        elif self.rock_grid.get(downleft) != '#' and self.sand_grid.get(downleft) != 'o':
            new_loc =  downleft
        elif self.rock_grid.get(downright) != '#' and self.sand_grid.get(downright) != 'o':
            new_loc =  downright
        else:
            new_loc = loc
        return new_loc

    def drop_sand(self):
        loc = (500,0)
        new_loc = self._fall(loc)
        while new_loc != loc:
            loc = new_loc
            if new_loc[1] == self.abyss_height:
                return False
            new_loc = self._fall(loc)
        self.sand_grid[new_loc] = 'o'
        return True

    def get_sand_capacity(self):
        self.sand_grid = {}
        capacity = 0
        while self.drop_sand():
            capacity += 1
        return capacity

def get_answer(input_path:str, part:int) -> int:
    grid = Grid(input_path)
    if part == 1:
        return grid.get_sand_capacity()
    elif part == 2:
        pass
    else:
        raise Exception('not part 1 or 2')

if __name__ == "__main__":
    input_path = utils.get_input_path(__file__)
    test_path = utils.get_test_path(__file__)
    test_answer = get_answer(test_path, part=1)
    assert test_answer == 24, f"got sand capacity of {test_answer} on {test_path}, should be 24"
    part1_answer = get_answer(input_path, part=1)
    part2_answer = get_answer(input_path, part=2)

    print(
        f"Test Answer: {test_answer},",
        f"Part 1 Answer: {part1_answer},",
        f"Part 2 Answer: {part2_answer}"
    )
import utils
import itertools
import numpy as np
from functools import cache

class Board:
    def __init__(self, height, width):
        self.height = height
        self.store_height = 0
        self.width = width
        self.grid = np.zeros((height,width))

    def extend_grid(self, new_height) -> None:
        if new_height > self.height:
            self.grid = np.append(
                np.zeros((new_height-self.height,7)),
                self.grid,
                axis=0
            )
            self.height = new_height
        if self.height > 1000:
            self.store_height += 500
            self.height = self.height - 500
            self.grid = self.grid[:-500,:]


class TetrisGame:
    def __init__(self, path):
        self.jetstream = self._parse(path)
        self.rockstream = itertools.cycle(['-','+','L','I','s'])
        self.board = Board(7,7)

    def _parse(self, path):
        with open(path) as f:
            line = f.readline()
        return itertools.cycle(line.strip())

    def tower_height(self, drops:int) -> int:
        for _ in range(drops):
            self.drop_rock()
        return self.board.store_height + self.board.height - 7

    def drop_rock(self) -> None:
        rock = next(self.rockstream)
        topleft = tuple([0, 2])
        while True:
            topleft = self.blow(rock, topleft, next(self.jetstream))
            if not self.is_falling(rock, topleft):
                break
            topleft = tuple([topleft[0]+1,topleft[1]])

        self.freeze(rock, topleft)

    def blow(self, rock:str, topleft:tuple[int,int], jet:str) -> tuple[int,int]:
        rock_mass = self.get_rock_mass(rock)
        rock_width = np.amin(np.where(np.append(np.max(rock_mass,axis=0),0) == 0))
        if jet == '>':
            if topleft[1] + rock_width + 1 > self.board.width:
                return topleft
            else:
                overlap = self.board.grid[
                    topleft[0]:topleft[0]+4,
                    topleft[1]+1:topleft[1]+rock_width+1
                    ] + rock_mass[:,:rock_width]
                if np.amax(overlap) == 1:
                    return tuple([topleft[0],topleft[1]+1])
                else:
                    return topleft
        if jet == '<':
            if topleft[1] == 0:
                return topleft
            else:
                overlap = self.board.grid[
                    topleft[0]:topleft[0]+4,
                    topleft[1]-1:topleft[1]+rock_width-1
                    ] + rock_mass[:,:rock_width]
                if np.amax(overlap) == 1:
                    return tuple([topleft[0],topleft[1]-1])
                else:
                    return topleft

    def is_falling(self, rock:str, topleft:tuple[int,int]) -> bool:
        rock_mass = self.get_rock_mass(rock)
        mass_idxs = np.argwhere(rock_mass) + topleft
        for mass_idx in mass_idxs:
            if mass_idx[0] == self.board.height-1:
                return False
            if self.board.grid[mass_idx[0]+1, mass_idx[1]] == 1:
                return False
        return True

    def freeze(self, rock:str, topleft:tuple[int,int]) -> None:
        rock_mass = self.get_rock_mass(rock)
        rock_width = np.amin(np.where(np.append(np.max(rock_mass,axis=0),0) == 0))
        rock_height = 4 - np.amin(np.where(np.max(rock_mass,axis=1) == 1))
        new_height=(self.board.height-topleft[0]) - (4-rock_height) + 7
        self.board.grid[
            topleft[0]:topleft[0]+4,
            topleft[1]:topleft[1]+rock_width
        ] += rock_mass[:,:rock_width]
        self.board.extend_grid(new_height)

    @cache
    def get_rock_mass(self, rock):
        if rock == '-':
            mass_coords = np.array([[0]*4 for _ in range(3)] + [[1]*4])
        elif rock == 'I':
            mass_coords = np.array([[1,0,0,0] for _ in range(4)])
        elif rock == 's':
            mass_coords = np.array([
                [0,0,0,0],
                [0,0,0,0],
                [1,1,0,0],
                [1,1,0,0],
             ])
        elif rock == 'L':
            mass_coords = np.array([
                [0,0,0,0],
                [0,0,1,0],
                [0,0,1,0],
                [1,1,1,0],
             ])
        elif rock == '+':
            mass_coords = np.array([
                [0,0,0,0],
                [0,1,0,0],
                [1,1,1,0],
                [0,1,0,0],
             ])
        return mass_coords

def get_answer(path:str, part:int) -> int:
    tetris_game = TetrisGame(path)
    if part == 1:
        return tetris_game.tower_height(2022)
    elif part == 2:
        pass #To drop 1 trillion rocks, would need to rewrite most of this.
    else:
        raise Exception('not part 1 or 2')

if __name__ == "__main__":
    input_path = utils.get_input_path(__file__)
    test_path = utils.get_test_path(__file__)
    test_part1_answer = get_answer(test_path, part=1)
    assert test_part1_answer == 3068, f"got tower height of {test_part1_answer} on {test_path}, should be 3068"
    part1_answer = get_answer(input_path, part=1)
    # test_part2_answer = get_answer(test_path, part=2)
    # # assert test_part2_answer == 3068, f"got tower height of {test_part2_answer} on {test_path}, should be 3068"
    # part2_answer = get_answer(input_path, part=2)

    print(
        f"Test Part 1 Answer: {test_part1_answer},",
        f"Part 1 Answer: {part1_answer},",
        # f"Test Part 2 Answer: {test_part2_answer},",
        # f"Part 2 Answer: {part2_answer}"
    )
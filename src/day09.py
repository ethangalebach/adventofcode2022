import utils

class Rope:
    def __init__(self, knots:int):
        self.loc = (0,0)
        self.visited_locs = {(0,0)}
        self.knot_num = knots
        self.child = Rope(knots-1) if knots > 1 else None

    def travel_route(self, input_path:str):
        with open(input_path) as f:
            for num, line in enumerate(f):
                if line.strip():
                    dir = line[0]
                    steps = int(line.strip()[2:])
                    self.move(dir, steps)

    def move(self, dir:str, steps:int=1):
        for i in range(steps):
            if dir == 'U':
                self._move_up()
            if dir == 'D':
                self._move_down()
            if dir == 'L':
                self._move_left()
            if dir == 'R':
                self._move_right()
            if dir == 'UR':
                self._move_up_and_right()
            if dir == 'DR':
                self._move_down_and_right()
            if dir == 'UL':
                self._move_up_and_left()
            if dir == 'DL':
                self._move_down_and_left()
            self.visited_locs.add(self.loc)

    def _move_up(self):
        self.loc = (self.loc[0], self.loc[1]+1)
        if self.child and self.loc[1] - self.child.loc[1] == 2:
            if self.child.loc[0] == self.loc[0]:
                self.child.move('U')
            if self.child.loc[0] > self.loc[0]:
                self.child.move('UL')
            if self.child.loc[0] < self.loc[0]:
                self.child.move('UR')

    def _move_down(self):
        self.loc = (self.loc[0], self.loc[1]-1)
        if self.child and self.child.loc[1] - self.loc[1] == 2:
            if self.child.loc[0] == self.loc[0]:
                self.child.move('D')
            if self.child.loc[0] > self.loc[0]:
                self.child.move('DL')
            if self.child.loc[0] < self.loc[0]:
                self.child.move('DR')

    def _move_right(self):
        self.loc = (self.loc[0]+1, self.loc[1])
        if self.child and self.loc[0] - self.child.loc[0] == 2:
            if self.child.loc[1] == self.loc[1]:
                self.child.move('R')
            if self.child.loc[1] > self.loc[1]:
                self.child.move('DR')
            if self.child.loc[1] < self.loc[1]:
                self.child.move('UR')

    def _move_left(self):
        self.loc = (self.loc[0]-1, self.loc[1])
        if self.child and self.child.loc[0] - self.loc[0] == 2:
            if self.child.loc[1] == self.loc[1]:
                self.child.move('L')
            if self.child.loc[1] > self.loc[1]:
                self.child.move('DL')
            if self.child.loc[1] < self.loc[1]:
                self.child.move('UL')

    def _move_up_and_right(self):
        self.loc = (self.loc[0]+1, self.loc[1]+1)
        if self.child and self.loc[1] - self.child.loc[1] == 2:
            if self.child.loc[0] == self.loc[0]:
                self.child.move('U')
            if self.loc[0] > self.child.loc[0]:
                self.child.move('UR')
        if self.child and self.loc[0] - self.child.loc[0] == 2:
            if self.child.loc[1] == self.loc[1]:
                self.child.move('R')
            if self.loc[1] > self.child.loc[1]:
                self.child.move('UR')

    def _move_down_and_right(self):
        self.loc = (self.loc[0]+1, self.loc[1]-1)
        if self.child and self.child.loc[1] - self.loc[1] == 2:
            if self.child.loc[0] == self.loc[0]:
                self.child.move('D')
            if self.loc[0] > self.child.loc[0]:
                self.child.move('DR')
        if self.child and self.loc[0] - self.child.loc[0] == 2:
            if self.child.loc[1] == self.loc[1]:
                self.child.move('R')
            if self.child.loc[1] > self.loc[1]:
                self.child.move('DR')

    def _move_up_and_left(self):
        self.loc = (self.loc[0]-1, self.loc[1]+1)
        if self.child and self.loc[1] - self.child.loc[1] == 2:
            if self.child.loc[0] == self.loc[0]:
                self.child.move('U')
            if self.child.loc[0] > self.loc[0]:
                self.child.move('UL')
        if self.child and self.child.loc[0] - self.loc[0] == 2:
            if self.child.loc[1] == self.loc[1]:
                self.child.move('L')
            if self.loc[1] > self.child.loc[1]:
                self.child.move('UL')

    def _move_down_and_left(self):
        self.loc = (self.loc[0]-1, self.loc[1]-1)
        if self.child and self.child.loc[1] - self.loc[1] == 2:
            if self.child.loc[0] == self.loc[0]:
                self.child.move('D')
            if self.child.loc[0] > self.loc[0]:
                self.child.move('DL')
        if self.child and self.child.loc[0] - self.loc[0] == 2:
            if self.child.loc[1] == self.loc[1]:
                self.child.move('L')
            if self.child.loc[1] > self.loc[1]:
                self.child.move('DL')

def get_answer(input_path: str, part: int) -> str:
    if part == 1:
        knots = 2
    elif part == 2:
        knots = 10
    else:
        raise Exception('not part 1 or 2')

    rope = Rope(knots)
    rope.travel_route(input_path)
    while rope.child:
        rope = rope.child
    return len(rope.visited_locs)

if __name__ == "__main__":
    input_path = utils.get_input_path(__file__)
    part1_answer = get_answer(input_path, part=1)
    part2_answer = get_answer(input_path, part=2)

    print(
        f"Part 1 Answer: {part1_answer},",
        f"Part 2 Answer: {part2_answer}"
    )

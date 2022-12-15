import utils
from typing import Callable

class Monkey:
    def __init__(
        self,
        items:tuple[int,...],
        operation:Callable[[int],int],
        relief_factor:int,
        divisor:int,
        target1:int,
        target2:int
    ):
        self.items = list(items)
        self._operation = operation
        self._relief_factor = relief_factor
        self._divisor = divisor
        self._target1 = target1
        self._target2 = target2
        self.num_inspections = 0

    def inspect(self):
        self.items[0] = self._operation(self.items[0]) // self._relief_factor
        self.num_inspections += 1

    def thrown_item_and_target(self) -> tuple[int,int]:
        item = self.items.pop(0)
        target = self._target1 if item % self._divisor == 0 else self._target2
        return item, target

    def catch_item(self, item:int):
        self.items.append(item)

class KeepAwayGame:
    def __init__(self, path:str, rounds:int,relief_factor:int=1):
        self.rounds = rounds
        self.current_round = 1
        self._relief_factor = relief_factor
        self._divisor_product = 1
        self.monkeys = {}
        self._parse_monkeys(path)

    def _parse_monkeys(self, path:str):
        monkey_no = None
        items = None
        operation = None
        divisor = None
        target1 = target2 = None

        with open(path) as f:
            for line in f:
                if not line.strip():
                    continue
                key, value = line.strip().split(':')
                if key.startswith('Monkey'):
                    monkey_no = int(key.split(' ')[-1])
                elif key == 'Starting items':
                    items = tuple(map(int, value.strip().split(', ')))
                elif key == 'Operation':
                    op = value.split(' ')[-2]
                    var = value.split(' ')[-1]
                    if var == 'old':
                        if op == '+':
                            operation = lambda x: x + x
                        if op == '*':
                            operation = lambda x: x * x
                    else:
                        const = int(var)
                        if op == '+':
                            operation = lambda x,y=const: x + y
                        if op == '*':
                            operation = lambda x,y=const: x * y
                elif key == 'Test':
                    divisor = int(value.split(' ')[-1])
                elif key == 'If true':
                    target1 = int(value.split(' ')[-1])
                elif key == 'If false':
                    target2 = int(value.split(' ')[-1])
                    self.monkeys[monkey_no] = Monkey(items,operation,self._relief_factor,divisor,target1,target2)
                    self._divisor_product *= divisor

    def _play_game(self):
        while self.current_round <= self.rounds:
            self._play_round()

    def _play_round(self):
        for _,monkey in self.monkeys.items():
            self._take_turn(monkey)
        self.current_round += 1

    def _take_turn(self, monkey:Monkey):
        while monkey.items:
            monkey.inspect()
            item, target = monkey.thrown_item_and_target()
            self.monkeys[target].catch_item(item % self._divisor_product)

    def get_monkey_business(self) -> int:
        max1 = max2 = 0
        self._play_game()
        for _,monkey in self.monkeys.items():
            if monkey.num_inspections > max1:
                max2 = max1
                max1 = monkey.num_inspections
            elif monkey.num_inspections > max2:
                max2 = monkey.num_inspections
        return max1 * max2

def get_answer(input_path: str, part: int) -> int:
    if part == 1:
        game = KeepAwayGame(input_path, rounds=20, relief_factor=3)
        return game.get_monkey_business()
    elif part == 2:
        game = KeepAwayGame(input_path, rounds=10_000)
        return game.get_monkey_business()
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

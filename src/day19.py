import utils
from functools import cached_property, lru_cache

class FactoryBlueprints:
    def __init__(self, path:str):
        self.path = path
        self.blueprints = self._parse_blueprints(path)

    def _parse_blueprints(self, path):
        blueprints = {}
        with open(path) as f:
            for line in f:
                chars = str.split(line.strip(), ' ')
                num = int(chars[1][:-1])
                ore_robot_cost_ore = int(chars[6])
                clay_robot_cost_ore = int(chars[12])
                obsidian_robot_cost_ore = int(chars[18])
                obsidian_robot_cost_clay = int(chars[21])
                geode_robot_cost_ore = int(chars[27])
                geode_robot_cost_obsidian = int(chars[30])
                blueprints[num] = (
                    ore_robot_cost_ore,
                    clay_robot_cost_ore,
                    obsidian_robot_cost_ore,
                    obsidian_robot_cost_clay,
                    geode_robot_cost_ore,
                    geode_robot_cost_obsidian
                )
        return blueprints

    def get_blueprint_geodes(self):
        geodes = []
        quality_sum = 0
        for num, blueprint in self.blueprints.items():
            factory = Factory(blueprint)
            max_geode_num = factory.get_max_geodes()
            geodes.append((num, max_geode_num))
            quality_sum += num * max_geode_num
        return quality_sum, geodes

class Factory:
    def __init__(self, blueprint):
        self.ore_robots = 1
        self.clay_robots = 0
        self.obsidian_robots = 0
        self.geode_robots = 0
        self.ore = self.clay = self.obsidian = self.geodes = 0
        self.cost_ore_robot = blueprint[0]
        self.cost_clay_robot = blueprint[1]
        self.cost_obsidian_robot = (blueprint[2], blueprint[3])
        self.cost_geode_robot = (blueprint[4], blueprint[5])

    @lru_cache
    def get_max_geodes(self, moves=24, minerals=None, robots=None):
        if not minerals: minerals = (self.ore, self.clay, self.obsidian, self.geodes)
        if not robots: robots = (self.ore_robots, self.clay_robots, self.obsidian_robots, self.geode_robots)
        max_geodes = 0
        if moves == 0: return minerals[3]
        build_options = self._get_build_options(minerals)
        if len(build_options) == 0: build_options = {(0,0,0,0)}
        #if moves>12: print(build_options, minerals, robots)
        minerals = self._mine(minerals,robots)
        # print(moves,build_options, minerals)
        for build in build_options:
            new_robots = tuple(sum(r) for r in zip(build,robots))
            new_minerals = (
                minerals[0] - build[0]*self.cost_ore_robot - build[1]*self.cost_clay_robot - build[2]*self.cost_obsidian_robot[0] - build[3]*self.cost_geode_robot[0],
                minerals[1] - build[2]*self.cost_obsidian_robot[1],
                minerals[2] - build[3]*self.cost_geode_robot[1],
                minerals[3])
            #if moves>12:print(moves, new_minerals, new_robots)
            option_geodes = self.get_max_geodes(moves-1, new_minerals, new_robots)
            max_geodes = max(max_geodes,option_geodes)
        return max_geodes

    @lru_cache
    def _get_build_options(self, minerals, robots=(0,0,0,0)):
        options = set()
        #print(minerals, robots, self.cost_ore_robot)
        ore, clay, obsidian, geodes = minerals
        ore_robots, clay_robots, obsidian_robots, geode_robots = robots
        if ore >= self.cost_geode_robot[0] and obsidian >= self.cost_geode_robot[1]:
            return self._get_build_options(
                    (ore-self.cost_geode_robot[0], clay, obsidian-self.cost_geode_robot[1], geodes),
                    (ore_robots, clay_robots, obsidian_robots, geode_robots+1)
            )
        if ore >= self.cost_obsidian_robot[0] and clay >= self.cost_obsidian_robot[1]:
            return self._get_build_options(
                (ore-self.cost_obsidian_robot[0], clay-self.cost_obsidian_robot[1], obsidian, geodes),
                (ore_robots, clay_robots, obsidian_robots+1, geode_robots)
            )
        if ore >= self.cost_clay_robot:
            options.update(
                self._get_build_options(
                    (ore-self.cost_clay_robot, clay, obsidian, geodes),
                    (ore_robots, clay_robots+1, obsidian_robots, geode_robots)
                )
            )
        if ore >= self.cost_ore_robot:
            options.update(
                self._get_build_options(
                    (ore-self.cost_ore_robot, clay, obsidian, geodes),
                    (ore_robots+1, clay_robots, obsidian_robots, geode_robots)
                )
            )
        if (
            ore < self.cost_ore_robot and
            ore < self.cost_clay_robot and
            (ore < self.cost_obsidian_robot[0] or clay < self.cost_obsidian_robot[1]) and
            (ore < self.cost_geode_robot[0] or obsidian < self.cost_geode_robot[1])
        ):
            options.add((ore_robots, clay_robots, obsidian_robots, geode_robots))

        return options

    def _mine(self, minerals=None, robots=None):
        return tuple(sum(m) for m in zip(minerals,robots))


def get_answer(input_path:str, part:int) -> int:
    factory_blueprints = FactoryBlueprints(input_path)
    factory = Factory(factory_blueprints.blueprints[1])
    if part == 1:
        return factory_blueprints.get_blueprint_geodes()
        # return factory.get_max_geodes()
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
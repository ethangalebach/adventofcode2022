import utils
import itertools

class Diamond:
    def __init__(self, sx:int, sy:int, d:int):
        self.center = (sx,sy)
        self.distance = d
        self.cvtop = (sx, sy+d)
        self.cvbottom = (sx, sy-d)
        self.cvleft = (sx-d,sy)
        self.cvright = (sx+d, sy)

class SensorBeaconMap:
    def __init__(self, path:str):
        self.sbmap, self.sdmap = self._parse_sbmap(path)

    def _parse_sbmap(self, path:str):
        sbmap = {}
        sdmap = {}
        with open(path) as f:
            for line in f:
                words = str.split(line,' ')
                sx = int(words[2][2:-1])
                sy = int(words[3][2:-1])
                bx = int(words[8][2:-1])
                by = int(words[9][2:])
                sbmap[(sx,sy)] = (bx,by)
                sdmap[(sx,sy)] = Diamond(sx,sy, d=abs(sx-bx) + abs(sy-by))
        return sbmap, sdmap

    def get_no_beacon_x_coords(self, y_coord:int):
        x_coords = set()
        for (sx,sy),(bx,by) in self.sbmap.items():
            d = abs(sx-bx) + abs(sy-by)
            h = abs(sy-y_coord)
            if d >= h:
                x_coords |= set(range(sx-(d-h), sx+(d-h)))
        return x_coords

    def get_distress_beacon_frequency(self):
        diamonds = [v for k, v in self.sdmap.items()]
        neg_diagonals = []
        pos_diagonals = []

        for di1,di2 in itertools.product(diamonds, repeat=2):
            di1x,di1y = di1.center
            di2x,di2y = di2.center
            if abs(di1x-di2x) + abs(di1y-di2y) == di1.distance + di2.distance + 2:
                if (di1x < di2x and di1y < di2y) or (di1x > di2x and di1y > di2y):
                    neg_diagonals += [(di1x+di1.distance+1,di1y)]
                else:
                    pos_diagonals += [(di1x+di1.distance+1,di1y)]

        for (nx,ny), (px,py) in itertools.product(neg_diagonals, pos_diagonals):
            p_diff = px - py
            n_total = nx + ny
            test_y = int((n_total - p_diff)/2)
            test_x = test_y + p_diff
            if test_y > 4_000_000 or test_x > 4_000_000 or test_y < 0 or test_x < 0:
                continue
            if test_x not in self.get_no_beacon_x_coords(test_y):
                beacon_x = test_x
                beacon_y = test_y

        return 4_000_000*beacon_x + beacon_y

def get_answer(input_path:str, part:int) -> int:
    sbmap = SensorBeaconMap(input_path)
    if part == 1:
        return len(sbmap.get_no_beacon_x_coords(2_000_000))
    elif part == 2:
        return sbmap.get_distress_beacon_frequency()
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
class Tile:
    def __init__(self, position, passable, entity=None):
        self.position = position
        self.passable = passable
        self.entity = entity

    def has_entity(self):
        return self.entity is not None

    def __str__(self):
        if not self.passable:
            return "#"
        elif not self.has_entity():
            return "."
        else:
            return "({})".format(self.entity)


class Entity:
    def __init__(self, allegiance, tile, hit_points, attack_points):
        self.allegiance = allegiance
        self.tile = tile
        self.hit_points = hit_points
        self.attack_points = attack_points
        self.start_tile = tile

    def __str__(self):
        return "{}({},{})".format(self.allegiance, self.hit_points, self.attack_points)

    def reset(self):
        self.tile.entity = None
        self.tile = self.start_tile
        if self.tile.has_entity():
            self.tile.entity.reset()
        self.tile.entity = self
        self.hit_points = 200


inp = """################################
###.GG#########.....#.....######
#......##..####.....G.G....#####
#..#.###...######..........#####
####...GG..######..G.......#####
####G.#...########....G..E.#####
###.....##########.........#####
#####..###########..G......#####
######..##########.........#####
#######.###########........###.#
######..########G.#G.....E.....#
######............G..........###
#####..G.....G#####...........##
#####.......G#######.E......#..#
#####.......#########......E.###
######......#########........###
####........#########.......#..#
#####.......#########.........##
#.#.E.......#########....#.#####
#............#######.....#######
#.....G.G.....#####.....########
#.....G.................########
#...G.###.....#.....############
#.....####E.##E....##.##########
##############.........#########
#############....#.##..#########
#############.#######...########
############.E######...#########
############..####....##########
############.####...E###########
############..####.E.###########
################################"""

# inp = """#########
# #G..G..G#
# #.......#
# #.......#
# #G..E..G#
# #.......#
# #.......#
# #G..G..G#
# #########"""
#
# inp = """#######
# #.G...#
# #...EG#
# #.#.#G#
# #..G#E#
# #.....#
# #######"""
#
# inp = """#######
# #.E...#
# #.#..G#
# #.###.#
# #E#G#G#
# #...#G#
# #######"""
#
# inp = """#########
# #G......#
# #.E.#...#
# #..##..G#
# #...##..#
# #...#...#
# #.G...G.#
# #.....G.#
# #########"""

directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]


def detect_enemy(entity, tile_map):
    y, x = entity.tile.position
    enemies = []
    for dy, dx in directions:
        tile = tile_map[(y + dy, x + dx)]
        if tile.has_entity() and tile.entity.allegiance != entity.allegiance:
            enemies.append(tile.entity)
    if len(enemies) > 0:
        return min(enemies, key=lambda enemy: enemy.hit_points)
    else:
        return None


def find_enemy(entity, tile_map):
    first_steps = dict()
    new_frontier = [entity.tile.position]
    while len(new_frontier) > 0:
        frontier = sorted(new_frontier)
        new_frontier = []
        for y, x in frontier:
            for dy, dx in directions:
                cy, cx = y + dy, x + dx
                if ((cy, cx) in tile_map) and tile_map[(cy, cx)].passable:
                    tile = tile_map[(cy, cx)]
                    if tile.has_entity():
                        if tile.entity.allegiance != entity.allegiance:
                            return first_steps[(y, x)]
                    elif (cy, cx) not in first_steps:
                        if (y, x) in first_steps:
                            first_steps[(cy, cx)] = first_steps[(y, x)]
                        else:
                            first_steps[(cy, cx)] = (cy, cx)
                        new_frontier.append((cy, cx))
    return None


def attack(entity, enemy):
    enemy.hit_points -= entity.attack_points
    if enemy.hit_points <= 0:
        return True
    return False


def print_tile_map(tile_map):
    y = 0
    x = 0
    s = []
    sy = []
    while True:
        if (y, x) in tile_map:
            tile = tile_map[(y, x)]
            if not tile.passable:
                sy.append("#")
            elif not tile.has_entity():
                sy.append(".")
            elif tile.entity.allegiance == "E":
                sy.append("E")
            else:
                sy.append("G")
        else:
            s.append(''.join(sy))
            sy = []
            y += 1
            x = -1
            if (y, x + 1) not in tile_map:
                break
        x += 1
    print('\n'.join(s) + '\n')


def process_inp(inp):
    tile_map = dict()
    entities = set()

    y = 0
    x = 0
    for tile_char in inp:
        if tile_char == "#":
            tile_map[(y, x)] = Tile(position=(y, x), passable=False)
        elif tile_char == ".":
            tile_map[(y, x)] = Tile(position=(y, x), passable=True)
        elif tile_char == "E" or tile_char == "G":
            tile = Tile(position=(y, x), passable=True)
            tile_map[(y, x)] = tile
            entity = Entity(tile_char, tile=tile, hit_points=200, attack_points=3)
            tile.entity = entity
            entities.add(entity)

        if tile_char == "\n":
            y += 1
            x = 0
        else:
            x += 1
    return tile_map, entities


def combat(tile_map, entities):
    killed = set()
    i = 0
    while True:
        old_entities = sorted(entities, key=lambda entity: entity.tile.position)
        for entity in old_entities:
            if entity not in entities:
                continue

            try:
                filter(lambda ent: ent.allegiance == "G", entities).__next__()
            except StopIteration:
                return True, sum(map(lambda ent: ent.hit_points, entities)) * i

            enemy = detect_enemy(entity, tile_map)
            if enemy is None:
                new_c = find_enemy(entity, tile_map)
                if new_c is not None:
                    new_tile = tile_map[new_c]
                    entity.tile.entity = None
                    entity.tile = new_tile
                    new_tile.entity = entity
                else:
                    continue
            enemy = detect_enemy(entity, tile_map)
            if enemy is not None:
                if attack(entity, enemy):
                    if enemy.allegiance == "E":
                        return False, 0
                    enemy.tile.entity = None
                    entities.remove(enemy)
        # print_tile_map(tile_map)
        i += 1


def combat_situations(tile_map, entities):
    ap = 4
    while True:
        print(ap)
        for entity in entities:
            entity.reset()
            if entity.allegiance == "E":
                entity.attack_points += 1
        entities_copy = entities.copy()
        success, res = combat(tile_map, entities_copy)
        print_tile_map(tile_map)
        if success:
            return res
        ap += 1


print(combat_situations(*process_inp(inp)))

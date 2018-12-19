from collections import defaultdict
from time import sleep

inp = """.#...#..|.#||.|.......##.|#|.....#|...#.|.....#.|.
|..|.#.|.#....#.|..#..|#....#|#.|||.....|...#....#
|..|..|.||.....#..#||..#..#..|.#.|..|..||...|#...#
..##|.||.|.#.###.....#....#...#.|.|..||||.....|.|.
.....#.......|..|#.|...|.|#..........#|.|..|.||.##
.#|....|..|..#.#|.|..||#...|....##||..|.||....#.#.
|##......#.#..|.|..##|#...|...|.##|...|#...|...##|
...|...|||.#|..|#.#....#|....|..||..|...|#|..#|.|.
|.|##....#.|.|.#..#...##.#......#.#.|......|...|||
..#.||..#.....#.|##..#..|##...|#|..|##|..|.|#..##.
..||#...#..|...|#.#....#...#...|#.||.|.##|.#....#|
.#...#.#|#|.#....#..|....|.|...|.|.#...#.||....|..
.#...........##.#...#..||...#...|###...|...#.|.#..
....|.|...##|#...#..#|#......##....#...|.#.....|#|
.##..#.#.##.....#......|....#...|.#.#......#...##.
...#.#..|#|#..#.....||.##|#....|.#.|...#||#.|#...|
.#..##||.#|....|.||.||...|..|....|#..#|..##.#|.|.#
.#.||.|##.|..|..#..|#|..###.||#........||#|.||##|.
.|.##|.#....#.#..|..|...#...|.#.|......|##..#.....
..||...|.|##.||..|.|...|#..|.........#.|.#.....|##
#..|..|#.......#.||#.|#..|#|#.##.|||....#.#...|..|
|..|#|...||..|..||...#......##..|.|#..##....#.##.|
#|.#...|..|.....||.|###..#|.|..#.|..|||.#.#....|..
..#.||....##|.##.#.##..#||......#.#.....|.....#...
#.#...||..|..|#...|#..||#.|..|..|..||.|.#...|...#.
..|.#.#.|.#|#...#.||.|#|#..#..#.#|....##||#..|.|.#
.#...|....#...|.||#.|.#...|.......#..|.#........|.
..|.#|#||#....|..|#.#...#....#..|.|.|..||#|..##...
......|........|......||................|...##..#.
#|.......|.|.|.|..####..#.|#....|..|#|#....#....|.
||.||#.||#....|.#..#.....|..#.|#.|.|...|....####..
..........#|..|||..#|..|..|||##|#||#|....||.|...||
....|....#.|......#|....###....|.##|.#||||||..#.|#
.|#|.#.##||......#.#.||.|.##...|.|.|#........#.#|.
.......|...|..|.|.....|.#|.|.#...#...#|...#.||...#
.||.#..|.##.#..##...#....|...|#..##|.|.#..|#|#|..|
.#..|.|##|....#|###.....|...||.|.|||......#|....|.
.|#.#.....|.##.##.|........|...|...|||....#....##.
...##|||.|##|.|..#......#.......|##|.|..|.......|.
...#.....#|.#.||.....|....#.#|......##.....##..|#|
..|.|...|....#|....###.|##..........|#..#|.#|..|#.
..|..#.|.....|...|...#|.||#|..#.#..#.#|..|........
..|..||.#.......|##|..|..|..|..##|.|...#.#..|.....
#.#..#.|###...#...||.#..#|...|.##...|..#|.......|.
..##.|..#|...#...|..#.|..|#.|.....#..#.#..#|#|...#
#......|..|.#.|.|...........#......||..#.||..#....
...#|......#.#|.....#....|..|......|.#.#.|.|......
#|.##...#.##..|#..|...#.....#|.#.............|..|#
.....|.|..|.||.#|.||##...#|.##|#.....#..#..#|.#...
..|..|.#.....#.##|.##|.||..#..#|#.||..||#.###..||."""

# inp = """.#.#...|#.
# .....#|##|
# .|..|...#.
# ..|#.....#
# #.#|||#|#|
# ...#.||...
# .|....|...
# ||...#|.#|
# |.||||..|.
# ...#.|..|."""

acre_map = dict()
y = 0
x = 0

max_x = 0

for acre in inp:
    if acre == ".":
        acre_map[(y, x)] = 0
    elif acre == "|":
        acre_map[(y, x)] = 1
    elif acre == "#":
        acre_map[(y, x)] = 2

    if acre == "\n":
        max_x = x
        x = 0
        y += 1
    else:
        x += 1

max_y = y + 1


def print_acre_map(m):
    chars = [".", "|", "#"]
    ss = []
    for y in range(max_y):
        s = []
        for x in range(max_x):
            s.append(chars[m[(y, x)]])
        ss.append("".join(s))
    print('\n'.join(ss))
    print()


neighbours = dict()
neighbour_vecs = {(0, 1), (1, 1), (1, 0), (-1, 0), (-1, 1), (-1, -1), (0, -1), (1, -1)}

for y in range(max_y):
    for x in range(max_x):
        neighbour_set = set()
        for dy, dx in neighbour_vecs:
            cy, cx = y + dy, x + dx
            if 0 <= cy < max_y and 0 <= cx < max_x:
                neighbour_set.add((cy, cx))
        neighbours[(y, x)] = neighbour_set

scores = defaultdict(lambda: set())
acre_maps = dict()

for i in range(1000000000):
    new_acre_map = dict()
    # print_acre_map(acre_map)
    # sleep(0.05)
    for c, v in acre_map.items():
        if v == 0:
            treed_neighbour_count = 0
            for neighbour_c in neighbours[c]:
                if acre_map[neighbour_c] == 1:
                    treed_neighbour_count += 1
                    if treed_neighbour_count >= 3:
                        new_acre_map[c] = 1
                        break
            else:
                new_acre_map[c] = 0
        elif v == 1:
            lumbered_neighbour_count = 0
            for neighbour_c in neighbours[c]:
                if acre_map[neighbour_c] == 2:
                    lumbered_neighbour_count += 1
                    if lumbered_neighbour_count >= 3:
                        new_acre_map[c] = 2
                        break
            else:
                new_acre_map[c] = 1
        elif v == 2:
            has_treed_neighbour = False
            has_lumbered_neighbour = False
            for neighbour_c in neighbours[c]:
                if acre_map[neighbour_c] == 1:
                    if has_lumbered_neighbour:
                        new_acre_map[c] = 2
                        break
                    has_treed_neighbour = True
                elif acre_map[neighbour_c] == 2:
                    if has_treed_neighbour:
                        new_acre_map[c] = 2
                        break
                    has_lumbered_neighbour = True
            else:
                new_acre_map[c] = 0
    score = sum(map(lambda x: 1 if x == 1 else 0, new_acre_map.values())) \
            * sum(map(lambda x: 1 if x == 2 else 0, new_acre_map.values()))
    if score in scores.keys():
        other_is = scores[score]
        for other_i in other_is:
            if acre_maps[other_i] == new_acre_map:
                acre_map = new_acre_map
                print_acre_map(new_acre_map)
                print_acre_map(acre_maps[other_i])
                break
        else:
            scores[score].add(i)
            acre_maps[i] = new_acre_map
            acre_map = new_acre_map
            continue
        break
    scores[score].add(i)
    acre_maps[i] = new_acre_map
    acre_map = new_acre_map

cycle_length = i - other_i
cycle_start = other_i
endpoint = 1000000000 - 1

cycle_tail = (endpoint - cycle_start) % cycle_length
print(i, other_i, cycle_length, cycle_tail)

final_acre_map = acre_maps[cycle_start + cycle_tail]

score = sum(map(lambda x: 1 if x == 1 else 0, final_acre_map.values())) \
        * sum(map(lambda x: 1 if x == 2 else 0, final_acre_map.values()))
print(score)

final_acre_map = acre_maps[cycle_start + cycle_tail + 1]

score = sum(map(lambda x: 1 if x == 1 else 0, final_acre_map.values())) \
        * sum(map(lambda x: 1 if x == 2 else 0, final_acre_map.values()))
print(score)

final_acre_map = acre_maps[cycle_start + cycle_tail - 1]

score = sum(map(lambda x: 1 if x == 1 else 0, final_acre_map.values())) \
        * sum(map(lambda x: 1 if x == 2 else 0, final_acre_map.values()))
print(score)

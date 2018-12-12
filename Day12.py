import re
from collections import defaultdict

inp = """initial state: ##.#...#.#.#....###.#.#....##.#...##.##.###..#.##.###..####.#..##..#.##..#.......####.#.#..#....##.#

#.#.# => #
..#.# => .
.#.## => #
.##.. => .
##... => #
##..# => #
#.##. => #
.#..# => #
.#### => .
....# => .
#.... => .
#.### => .
###.# => #
.#.#. => .
#...# => .
.#... => #
##.#. => #
#..## => #
..##. => .
####. => #
.###. => .
##### => .
#.#.. => .
...#. => .
..#.. => .
###.. => #
#..#. => .
.##.# => .
..... => .
##.## => #
..### => #
...## => #"""


# inp = """initial state: #..#.#..##......###...###
#
# ...## => #
# ..#.. => #
# .#... => #
# .#.#. => #
# .#.## => #
# .##.. => #
# .#### => #
# #.#.# => #
# #.### => #
# ##.#. => #
# ##.## => #
# ###.. => #
# ###.# => #
# ####. => #"""

class Pot:
    def __init__(self, val, prv=None, nxt=None, i=-3):
        self.val = val
        self.prv = prv
        self.nxt = nxt
        self.i = i

    def append_left(self, val):
        node = Pot(val, nxt=self, i=self.i - 1)
        self.prv = node
        return node

    def append_right(self, val):
        node = Pot(val, prv=self, i=self.i + 1)
        self.nxt = node
        return node

    def step_left(self, n=1):
        if n == 0:
            return self
        else:
            return self.prv.step_left(n - 1)

    def step_right(self, n=1):
        if n == 0:
            return self
        else:
            return self.nxt.step_right(n - 1)

    def has_nxt(self):
        return self.nxt is not None

    def has_prv(self):
        return self.prv is not None

    def list_str(self, i):
        s = []
        node = self
        while node is not None:
            s.append("#" if node.val[i] else ".")
            node = node.nxt
        return ''.join(map(str, s))


inpl = inp.splitlines()

inp_reg1 = re.compile(r"initial state: ([#.]+)")
inp_reg2 = re.compile(r"([#.]{5}) => ([#.])")

rules_raw = inp_reg2.findall(inp)

rules = defaultdict(lambda: False)

for rule_l, rule_r in rules_raw:
    rules[tuple(map(lambda x: x == "#", rule_l))] = (rule_r == "#")

init_state = inp_reg1.findall(inp)[0]

potlll = Pot([False])
potll = potlll.append_right([False])
potl = potll.append_right([False])
prevPot = potl

for pot in init_state:
    prevPot = prevPot.append_right([pot == "#"])

potr = prevPot.append_right([False])
potrr = potr.append_right([False])
potrrr = potrr.append_right([False])

root = potlll

n = 99

for i in range(n):
    print(i, ":", root.list_str(i), "(", root.i, ")")
    potll, potl, pot, potr = root, root.nxt, root.nxt.nxt, root.nxt.nxt.nxt
    potll.val.append(False)
    potl.val.append(False)
    while potr.has_nxt():
        potrr = potr.nxt
        pot.val.append(rules[(potll.val[i], potl.val[i], pot.val[i], potr.val[i], potrr.val[i])])
        if pot.val[i + 1]:
            if (not potll.has_prv()) or (root == potll):
                root = potll.append_left([False] * (i + 2))
            if not potrr.has_nxt():
                potrr.append_right([False] * (i + 1))
        elif (not potl.val[i + 1]) and (not potll.val[i + 1]) and (root == potll.prv):
            root = potll
        potll, potl, pot, potr = potl, pot, potr, potrr
    pot.val.append(False)
    potr.val.append(False)

print(n, ":", root.list_str(n), "(", root.i, ")")
pot = root
_s = 0
s = 0
c = 0

while True:
    if pot.val[n]:
        _s += pot.i
        s += pot.i - root.i
        c += 1
    if not pot.has_nxt():
        break
    pot = pot.nxt

print(_s)
print((50000000000 + root.i - n) * c + s)
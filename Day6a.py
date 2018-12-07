import re
from collections import *
from functools import *

inp = """61, 90
199, 205
170, 60
235, 312
121, 290
62, 191
289, 130
131, 188
259, 82
177, 97
205, 47
302, 247
94, 355
340, 75
315, 128
337, 351
73, 244
273, 103
306, 239
261, 198
355, 94
322, 69
308, 333
123, 63
218, 44
278, 288
172, 202
286, 172
141, 193
72, 316
84, 121
106, 46
349, 77
358, 66
309, 234
289, 268
173, 154
338, 57
316, 95
300, 279
95, 285
68, 201
77, 117
313, 297
259, 97
270, 318
338, 149
273, 120
229, 262
270, 136"""

inp_reg = re.compile(r"(\d*), (\d*)")

inpr = map(partial(map, int), inp_reg.findall(inp))
coords = list(map(tuple, inpr))

l_bound = min(min(coords, key=min))
u_bound = max(max(coords, key=max))

# map = defaultdict(lambda: defaultdict(int))
actions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
area = dict()
frontier = deque()
claimed = defaultdict(lambda: False)
infinite = defaultdict(lambda: False)
names = dict()

i = 0

for x, y in coords:
    area[(x, y)] = 1
    claimed[(x, y)] = (x, y)
    frontier.append(((x, y), x, y))
    names[(x, y)] = chr(i + 48)
    i += 1

claim_pending = defaultdict(lambda: False)

while True:
    if len(frontier) == 0:
        if len(claim_pending) > 0:
            for claim, name in claim_pending.items():
                claimed[claim] = name
                if name is not "multiple" and name is not False:
                    area[name] += 1
                    x, y = claim
                    frontier.append((name, x, y))
                    if x == l_bound or x == u_bound or y == l_bound or y == u_bound:
                        infinite[name] = True
            claim_pending = defaultdict(lambda: False)
        if len(frontier) == 0:
            break
    name, x, y = frontier.popleft()
    for xact, yact in actions:
        xnew, ynew = xact + x, yact + y
        if (xnew >= l_bound) and (ynew >= l_bound) and (xnew < u_bound) and (ynew < u_bound) \
                and (claimed[(xnew, ynew)] is False):
            if claim_pending[(xnew, ynew)] is False:
                claim_pending[(xnew, ynew)] = name
            elif claim_pending[(xnew, ynew)] != name:
                claim_pending[(xnew, ynew)] = "multiple"

for x in range(l_bound, u_bound):
    s = []
    for y in range(l_bound, u_bound):
        if claimed[(x, y)] is False:
            s.append('!')
        elif claimed[(x, y)] == "multiple":
            s.append('.')
        else:
            s.append(names[claimed[(x, y)]])
    print(''.join(s))

print(max(area.items(), key=lambda item: item[1] if not infinite[item[0]] else 0))

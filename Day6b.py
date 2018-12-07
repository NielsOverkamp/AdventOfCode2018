import re
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

area = 0

for x0 in range(l_bound, u_bound):
    for y0 in range(l_bound, u_bound):
        if x0 == 270 and y0 == 136:
            print("yas")
        s = 0
        for x1, y1 in coords:
            s += abs(x0-x1)
            s += abs(y0-y1)
            if s >= 10000:
                break
        else:
            area += 1

print(area)

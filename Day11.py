serial_id_str = """7857"""
serial_id = int(serial_id_str)

grid = dict()

for x in range(1, 301):
    for y in range(1, 301):
        rack_id = x + 10
        power_level = (rack_id * y + serial_id) * rack_id
        if power_level < 100:
            power_level = -5
        else:
            power_level = int(str(power_level)[-3]) - 5
        grid[(x, y)] = power_level

print()

max_res = None
max_s = -60000

for x in range(1, 301):
    for y in range(1, 301):
        s = 0
        for size in range(0, 301 - max(x, y)):
            for dx in range(x, x + size):
                s += grid[(dx, y + size)]
            for dy in range(y, y + size):
                s += grid[(x + size, dy)]
            s += grid[(x + size, y + size)]
            if s > max_s:
                max_res = (x, y, size + 1)
                max_s = s
        print(x, y, max_res, max_s)

print(max_res)

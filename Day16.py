import re
from collections import defaultdict

with open("Day16inp") as f:
    inp = f.read()

# inp = """Before: [3, 2, 1, 1]
# 9 2 1 2
# After:  [3, 2, 2, 1]"""

inp_reg = re.compile(
    r"Before: \[(\d+), (\d+), (\d+), (\d+)\]\n(\d+) (\d+) (\d+) (\d+)\nAfter:  \[(\d+), (\d+), (\d+), (\d+)\]")

inpr = map(lambda a: tuple(map(int, a)), inp_reg.findall(inp))


def addr(regs, a, b, c):
    regs[c] = regs[a] + regs[b]
    return regs


def addi(regs, a, b, c):
    regs[c] = regs[a] + b
    return regs


def mulr(regs, a, b, c):
    regs[c] = regs[a] * regs[b]
    return regs


def muli(regs, a, b, c):
    regs[c] = regs[a] * b
    return regs


def banr(regs, a, b, c):
    regs[c] = regs[a] & regs[b]
    return regs


def bani(regs, a, b, c):
    regs[c] = regs[a] & b
    return regs


def borr(regs, a, b, c):
    regs[c] = regs[a] | regs[b]
    return regs


def bori(regs, a, b, c):
    regs[c] = regs[a] | b
    return regs


def setr(regs, a, _, c):
    regs[c] = regs[a]
    return regs


def seti(regs, a, _, c):
    regs[c] = a
    return regs


def gtir(regs, a, b, c):
    regs[c] = int(a > regs[b])
    return regs


def gtri(regs, a, b, c):
    regs[c] = int(regs[a] > b)
    return regs


def gtrr(regs, a, b, c):
    regs[c] = int(regs[a] > regs[b])
    return regs


def eqir(regs, a, b, c):
    regs[c] = int(a == regs[b])
    return regs


def eqri(regs, a, b, c):
    regs[c] = int(regs[a] == b)
    return regs


def eqrr(regs, a, b, c):
    regs[c] = int(regs[a] == regs[b])
    return regs


operators = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

operators_ = [None] * 16

operator_opcode_map = defaultdict(lambda: set(range(16)))
opcode_operator_map = defaultdict(lambda: set(operators))

for reg0, reg1, reg2, reg3, opcode, a, b, c, reg0_, reg1_, reg2_, reg3_ in inpr:
    regs = [reg0, reg1, reg2, reg3]
    regs_res = [reg0_, reg1_, reg2_, reg3_]
    operator_set = set()
    for operator in operators:
        if regs_res == operator(regs.copy(), a, b, c):
            operator_set.add(operator)
            operator_opcode_map[operator].add(opcode)
    opcode_operator_map[opcode].intersection_update(operator_set)

final_opcode_operator_map = dict()
found_operators = set()

while len(final_opcode_operator_map) < 16:
    unique_solutions = filter(lambda l: len(l[1]) == 1, opcode_operator_map.items())
    for opcode, operator_set in unique_solutions:
        final_opcode_operator_map[opcode] = operator_set.pop()
        found_operators.add(final_opcode_operator_map[opcode])
    for operator_set in opcode_operator_map.values():
        operator_set.difference_update(found_operators)

programr = re.compile(r"(?:\d+ \d+ \d+ \d+\n)+(?:\d+ \d+ \d+ \d+)")
program_str = programr.findall(inp)[0]

linesr = re.compile(r"(\d+) (\d+) (\d+) (\d+)")
lines = map(lambda a: tuple(map(int, a)), linesr.findall(program_str))

regs = [0, 0, 0, 0]
for opcode, a, b, c in lines:
    print(opcode, a, b, c, final_opcode_operator_map[opcode], regs)
    regs = final_opcode_operator_map[opcode](regs, a, b, c)
    print(regs)

print(regs)

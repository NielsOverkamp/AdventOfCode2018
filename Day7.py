import re
from collections import *

inp = """Step G must be finished before step X can begin.
Step X must be finished before step B can begin.
Step A must be finished before step I can begin.
Step D must be finished before step H can begin.
Step O must be finished before step T can begin.
Step H must be finished before step C can begin.
Step S must be finished before step E can begin.
Step U must be finished before step M can begin.
Step M must be finished before step Z can begin.
Step R must be finished before step N can begin.
Step C must be finished before step Q can begin.
Step T must be finished before step P can begin.
Step I must be finished before step W can begin.
Step W must be finished before step N can begin.
Step P must be finished before step J can begin.
Step N must be finished before step F can begin.
Step Y must be finished before step J can begin.
Step J must be finished before step L can begin.
Step L must be finished before step E can begin.
Step E must be finished before step B can begin.
Step Q must be finished before step B can begin.
Step F must be finished before step K can begin.
Step V must be finished before step K can begin.
Step Z must be finished before step B can begin.
Step B must be finished before step K can begin.
Step G must be finished before step U can begin.
Step E must be finished before step V can begin.
Step A must be finished before step Z can begin.
Step C must be finished before step V can begin.
Step R must be finished before step B can begin.
Step Q must be finished before step Z can begin.
Step R must be finished before step K can begin.
Step T must be finished before step B can begin.
Step L must be finished before step B can begin.
Step M must be finished before step K can begin.
Step T must be finished before step Z can begin.
Step W must be finished before step B can begin.
Step I must be finished before step E can begin.
Step A must be finished before step M can begin.
Step V must be finished before step Z can begin.
Step Y must be finished before step B can begin.
Step Q must be finished before step F can begin.
Step W must be finished before step Y can begin.
Step U must be finished before step K can begin.
Step D must be finished before step F can begin.
Step P must be finished before step F can begin.
Step N must be finished before step L can begin.
Step H must be finished before step T can begin.
Step H must be finished before step L can begin.
Step C must be finished before step T can begin.
Step H must be finished before step I can begin.
Step Z must be finished before step K can begin.
Step L must be finished before step Z can begin.
Step Y must be finished before step K can begin.
Step I must be finished before step V can begin.
Step P must be finished before step K can begin.
Step P must be finished before step N can begin.
Step G must be finished before step D can begin.
Step I must be finished before step J can begin.
Step H must be finished before step K can begin.
Step L must be finished before step Q can begin.
Step D must be finished before step M can begin.
Step O must be finished before step V can begin.
Step R must be finished before step L can begin.
Step D must be finished before step W can begin.
Step M must be finished before step J can begin.
Step O must be finished before step R can begin.
Step N must be finished before step Z can begin.
Step Y must be finished before step V can begin.
Step W must be finished before step L can begin.
Step U must be finished before step Y can begin.
Step S must be finished before step V can begin.
Step M must be finished before step P can begin.
Step X must be finished before step A can begin.
Step A must be finished before step E can begin.
Step A must be finished before step L can begin.
Step A must be finished before step R can begin.
Step V must be finished before step B can begin.
Step P must be finished before step B can begin.
Step E must be finished before step F can begin.
Step T must be finished before step V can begin.
Step S must be finished before step R can begin.
Step T must be finished before step F can begin.
Step P must be finished before step Y can begin.
Step A must be finished before step C can begin.
Step J must be finished before step F can begin.
Step H must be finished before step B can begin.
Step C must be finished before step E can begin.
Step P must be finished before step E can begin.
Step D must be finished before step I can begin.
Step X must be finished before step F can begin.
Step T must be finished before step Q can begin.
Step J must be finished before step B can begin.
Step C must be finished before step B can begin.
Step P must be finished before step Q can begin.
Step H must be finished before step R can begin.
Step F must be finished before step B can begin.
Step T must be finished before step J can begin.
Step A must be finished before step W can begin.
Step N must be finished before step K can begin.
Step T must be finished before step E can begin."""
# inp = """Step C must be finished before step A can begin.
# Step C must be finished before step F can begin.
# Step A must be finished before step B can begin.
# Step A must be finished before step D can begin.
# Step B must be finished before step E can begin.
# Step D must be finished before step E can begin.
# Step F must be finished before step E can begin."""
inp_reg = re.compile(r"Step (.) must be finished before step (.) can begin\.")

inpr = inp_reg.findall(inp)

to_graph = defaultdict(list)
frm_graph = defaultdict(list)

todo = dict()
for frm, to in inpr:
    to_graph[frm].append(to)
    frm_graph[to].append(frm)
    frm_graph[frm] = frm_graph[frm]
    to_graph[to] = to_graph[to]
    todo[frm] = True
    todo[to] = True

frontier = []

for to, frms in frm_graph.items():
    if len(frms) == 0:
        frontier.append(to)

t = 0
working = dict()
workers = [None] * 5
todo = len(todo.keys())
done = []
while todo > 0:
    for frm, info in list(working.items()):
        t_end, worker = info
        if t_end == t:
            working.pop(frm)
            workers[worker] = None
            done.append(frm)
            todo -= 1
            tos = to_graph[frm]
            for to in tos:
                frms = frm_graph[to]
                frms.remove(frm)
                if len(frms) == 0:
                    frontier.append(to)
    frontier = sorted(frontier, reverse=True)
    for worker, work in enumerate(workers):
        if (work is None) and len(frontier) > 0:
            frm = frontier.pop()
            working[frm] = (t + 61 + ord(frm) - ord('A'), worker)
            workers[worker] = frm
    print(str(t) + '\t' + ('.' if workers[0] is None else workers[0]) + '\t'
          + ('.' if workers[1] is None else workers[1]) + '\t'
          + ('.' if workers[2] is None else workers[2]) + '\t'
          + ('.' if workers[3] is None else workers[3]) + '\t'
          + ('.' if workers[4] is None else workers[4]) + '\t'
          + ''.join(done) + '\t'
          + ''.join(frontier))
    t += 1

t -= 1
print(t)

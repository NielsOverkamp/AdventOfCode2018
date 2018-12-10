import re

inp = """9 players; last marble is worth 25 points"""
inp = """10 players; last marble is worth 1618 points"""
inp = "459 players; last marble is worth 7132000 points"
# inp = "13 players; last marble is worth 7999 points"
# inp = "17 players; last marble is worth 1104"
# inp = "21 players; last marble is worth 6111"
# inp = "30 players; last marble is worth 5807 points"

inp_reg = re.compile(r"(\d+)")

inpr = inp_reg.findall(inp)


class Node:
    def __init__(self, val, prv=None, nxt=None):
        self.val = val
        if prv is None:
            prv = self
            nxt = self
        self.prv = prv
        self.nxt = nxt

    def append_left(self, val):
        node = Node(val, prv=self.prv, nxt=self)
        self.prv.nxt, self.prv = node, node
        return node

    def append_right(self, val):
        node = Node(val, self, self.nxt)
        self.nxt.prv, self.nxt = node, node
        return node

    def pop_left(self):
        popped = self.prv
        self.prv.prv.nxt, self.prv = self, self.prv.prv
        return popped

    def pop_right(self):
        popped = self.nxt
        self.nxt.nxt.prv, self.nxt = self, self.nxt.nxt
        return popped

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

    def list_str(self):
        s = [self.val]
        node = self
        while True:
            node = node.nxt
            if node is self:
                break
            s.append(node.val)
        return '\t'.join(map(str, s))


player_count = int(inpr[0])
marble_count = int(inpr[1])

current_marble = Node(0)
player = 0
score = [0] * player_count

for i in range(1, marble_count + 1):
    if i % 23 == 0:
        current_marble = current_marble.step_left(6)
        score[player] += (i + current_marble.pop_left().val)
    else:
        current_marble = current_marble.step_right().append_right(i)
        player = (player + 1) % player_count
    # print(current_marble.list_str())

print('\t'.join(map(str, score)))
print(max(score))

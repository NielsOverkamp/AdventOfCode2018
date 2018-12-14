_inp = 165061
inp = [1, 6, 5, 0, 6, 1]
# inp = [5, 1, 5, 8, 9]
# inp = [5,9,4,1,4]
# inp = [9, 2, 5, 1, 0]
# inp = [0,1,2,4,5]

inp_length = len(inp)

i1 = 0
i2 = 1

scores = [3, 7]
length = 2

while True:
    score1 = scores[i1]
    score2 = scores[i2]
    new_score = score1 + score2
    if new_score >= 10:
        scores.append(1)
        if scores[-inp_length:] == inp:
            print(length + 1 - len(inp))
            break
        scores.append(new_score - 10)
        length += 2
        if scores[-inp_length:] == inp:
            print(length - len(inp))
            break
    else:
        scores.append(new_score)
        length += 1
        if scores[-inp_length:] == inp:
            print(length - len(inp))
            break
    i1 = (i1 + 1 + score1) % length
    i2 = (i2 + 1 + score2) % length

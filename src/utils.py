import random


def generate_field(rows, cols, bomb_number, seed):
    field = [0 for x in range(cols * rows)]
    random.seed(a=seed)
    bomb_indexes = random.sample(range(cols * rows),
                                 bomb_number)
    for i in range(bomb_number):
        x = bomb_indexes[i] % rows
        y = bomb_indexes[i] // rows
        for j in range(max(0, x - 1), min(x + 2, rows)):
            for k in range(max(0, y - 1), min(y + 2, cols)):
                index = k * rows + j
                field[index] = field[index] + 1
    for i in range(bomb_number):
        field[bomb_indexes[i]] = -1
    return field

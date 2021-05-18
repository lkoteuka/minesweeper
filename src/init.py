import src.gui as gui
import src.constants as const
import src.handlers as handlers
import random


def generate_field(size_x, size_y, bomb_number):
    field = [0 for x in range(size_x * size_y)]
    bomb_indexes = random.sample(range(size_x * size_y), bomb_number)
    for i in range(bomb_number):
        x = bomb_indexes[i] % size_y
        y = bomb_indexes[i] // size_y
        for j in range(max(0, x - 1), min(x + 2, size_y)):
            for k in range(max(0, y - 1), min(y + 2, size_x)):
                index = k * size_y + j
                field[index] = field[index] + 1
    for i in range(bomb_number):
        field[bomb_indexes[i]] = -1
    for i in range(size_x * size_y):
        if field[i] == -1:
            field[i] = handlers.bomb
        elif field[i] == 0:
            field[i] = handlers.none
        else:
            field[i] = handlers.number(field[i])
    return field


def initialize(size_x=const.HEIGHT, size_y=const.WIDTH,
               bomb_number=const.BOMBS):
    field = gui.FieldFrame(gui.root, cols=size_y, rows=size_x)
    field.set_buttons(generate_field(size_x, size_y, bomb_number))
    gui.root.mainloop()

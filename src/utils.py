"""Utils."""
import random


def generate_field(rows, cols, bomb_number, seed):
    """
    Generate game field.

    :param rows: the number of rows in field
    :type rows: int
    :param cols: the number of columns in field
    :type cols: int
    :param bomb_number: the number of bombs in field
    :type bomb_number: int
    :param seed: the seed to random for randomize bomb places
    :type seed: float
    :return: game field
    :rtype: list
    """
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


def open_all_field(cols, rows, cells):
    """
    Open all cells of field.

    :param rows: the number of rows in field
    :type rows: int
    :param cols: the number of columns in field
    :type cols: int
    :param cells: cells of field
    :rtype: None
    """
    for i in range(cols):
        for j in range(rows):
            index = j * cols + i
            cells[index].open()


def open_bombs(cols, rows, cells):
    """
    Open bombs.

    :param cols: the number of columns
    :type cols: int
    :param rows: the number of rows
    :type rows: int
    :param cells: cells of field
    :type cells: list
    """
    for i in range(cols):
        for j in range(rows):
            index = j * cols + i
            cells[index].is_marked = False
            cells[index].mark()
            cells[index].is_marked = False


def open_empty_cell(col, row, cols, rows, cells):
    """
    Open the empty cell that player chooses and others empty neighboring cells that are empty too.

    :param col: the column number of cell that player chose
    :type col: int
    :param: row: the row number of cell that player chose
    :type row: int
    :param cols: the number of columns
    :type cols: int
    :param rows: the number of rows
    :type rows: int
    :param cells: the array of cells of field
    :type cells: list
    """
    for i in range(max(0, col - 1), min(cols, col + 2)):
        for j in range(max(0, row - 1), min(rows, row + 2)):
            index = j * cols + i
            cells[index].open()


def reset_field(cols, rows, cells, field):
    """
    Reset all cells to match new field.

    :param cols: the number of columns
    :type cols: int
    :param rows: the number of rows
    :type rows: int
    :param cells: the array of cells of old field
    :type cells: list
    :param field: new field
    :type field: list
    :rtype: None
    """
    for i in range(cols):
        for j in range(rows):
            index = j * cols + i
            cells[index].reset(field[index])

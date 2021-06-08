from unittest import TestCase
from src.utils import generate_field


class Test(TestCase):
    def test_generate_field_small_size(self):
        cols = 4
        rows = 4
        num_bombs = 4
        seed = 0
        correct_field = [-1, 2, 1, 1,
                         1, 2, -1, 1,
                         1, 2, 2, 2,
                         -1, 1, 1, -1]
        field = generate_field(rows, cols, num_bombs, seed)
        for i in range(cols * rows):
            if correct_field[i] != field[i]:
                self.fail()

    def test_generate_field_big_size(self):
        cols = 10
        rows = 10
        num_bombs = 10
        seed = 0.5
        correct_field = [0, 0, 0, 1, -1, 2, 2, 2, 1, 0,
                         0, 0, 0, 2, 2, 3, -1, -1, 1, 0,
                         1, 1, 0, 1, -1, 3, 3, 2, 1, 0,
                         -1, 1, 0, 1, 2, -1, 1, 0, 0, 0,
                         1, 1, 0, 0, 1, 2, 2, 1, 0, 0,
                         1, 1, 1, 0, 0, 1, -1, 1, 0, 0,
                         1, -1, 2, 1, 1, 2, 2, 1, 0, 0,
                         1, 2, -1, 1, 1, -1, 1, 0, 0, 0,
                         0, 1, 1, 1, 1, 1, 1, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        field = generate_field(rows, cols, num_bombs, seed)
        for i in range(cols * rows):
            if correct_field[i] != field[i]:
                self.fail()

    def test_generate_field_big_bomb_number(self):
        cols = 7
        rows = 7
        num_bombs = 40
        seed = 1
        correct_field = [-1, -1, 4, -1, -1, 5, -1,
                         -1, -1, 6, -1, -1, -1, -1,
                         -1, 6, -1, -1, -1, -1, -1,
                         3, -1, -1, -1, -1, -1, -1,
                         -1, 7, -1, -1, -1, -1, -1,
                         -1, -1, -1, -1, -1, -1, -1,
                         -1, -1, -1, 4, 3, 4, -1]
        field = generate_field(rows, cols, num_bombs, seed)
        for i in range(cols * rows):
            if correct_field[i] != field[i]:
                self.fail()

    def test_generate_field_small_bomb_number(self):
        cols = 6
        rows = 6
        num_bombs = 3
        seed = 2
        correct_field = [0, 0, 1, -1, 2, -1,
                         0, 0, 1, 1, 2, 1,
                         0, 0, 0, 0, 1, 1,
                         0, 0, 0, 0, 1, -1,
                         0, 0, 0, 0, 1, 1,
                         0, 0, 0, 0, 0, 0]
        field = generate_field(rows, cols, num_bombs, seed)
        for i in range(cols * rows):
            if correct_field[i] != field[i]:
                self.fail()

    def test_open_all_field(self):
        from src import gui
        from src.utils import open_all_field

        def is_not_opened(cell):
            return not cell.is_disabled or cell.button['background'] != gui.Cell.BACKGROUND_COLOR_DISABLED

        cols = 4
        rows = 4
        bomb_number = 4
        field_frame = gui.FieldFrame(gui.root, cols=cols, rows=rows, bomb_number=bomb_number)
        gui.TopFrame(gui.root, cols=cols)
        open_all_field(field_frame.cols, field_frame.rows, field_frame.cells)
        for i in range(cols * rows):
            c = field_frame.cells[i]
            if is_not_opened(c):
                self.fail()

    def test_open_bombs(self):

        from src import gui
        from src.utils import open_bombs

        def is_not_opened(cell):
            return cell.is_bomb and not cell.is_disabled

        cols = 6
        rows = 6
        bomb_number = 6
        field_frame = gui.FieldFrame(gui.root, cols=cols, rows=rows, bomb_number=bomb_number)
        gui.TopFrame(gui.root, cols=cols)
        open_bombs(field_frame.cols, field_frame.rows, field_frame.cells)
        for i in range(cols * rows):
            c = field_frame.cells[i]
            if is_not_opened(c):
                self.fail()

    def test_reset_bombs(self):
        from src import gui
        from src.utils import reset_field
        cols = 6
        rows = 6
        bomb_number = 6
        seed = 1
        field_frame = gui.FieldFrame(gui.root, cols=cols, rows=rows, bomb_number=bomb_number)
        gui.TopFrame(gui.root, cols=cols, field_restart=field_frame.restart)
        field_frame.field = generate_field(rows, cols, bomb_number, seed)
        reset_field(cols, rows, field_frame.cells, field_frame.field)
        for i in range(cols * rows):
            cell = field_frame.cells[i]
            value = field_frame.field[i]
            if cell.value != value:
                self.fail()

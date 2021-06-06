from unittest import TestCase
from src.utils import generate_field


class Test(TestCase):
    def test_generate_field(self):
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

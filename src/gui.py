import src.constants as const
from src.handlers import Timer
import tkinter as tk
import random


class Cell():
    TEXT_BOMB = u"\u2738"
    TEXT_MARK = u"\u2690"
    TEXT_NONE = ""
    BACKGROUND_COLOR_NORMAL = "#DDDDDD"
    BACKGROUND_COLOR_DISABLED = "#BBBBBB"

    def __init__(self, button, value, loss_func, count_func, empty_cell_func):
        button["background"] = self.BACKGROUND_COLOR_NORMAL
        button.bind("<Button-1>", self.open)
        button.bind("<Button-3>", self.mark)
        button.pack(expand=True, fill=tk.BOTH)
        self.button = button
        self.loss_func = loss_func
        self.count_func = count_func
        self.empty_cell_func = empty_cell_func
        self.reset(value)

    def open(self, event=None):
        if self.is_disabled:
            return
        self.is_disabled = True
        self.button["background"] = self.BACKGROUND_COLOR_DISABLED
        self.button.config(state=tk.DISABLED, disabledforeground="#0000FF")
        if self.is_bomb:
            self.button.config(text=self.__class__.TEXT_BOMB,
                               disabledforeground='black')
            self.loss_func()
            return
        if self.is_empty:
            self.empty_cell_func()
        else:
            self.button.config(text=self.value,
                               disabledforeground=const.COLORS[self.value])
        self.count_func()

    def mark(self, event=None):
        if self.is_disabled and not self.is_marked:
            return
        if self.is_marked:
            self.is_disabled = False
            self.is_marked = False
            self.button.config(state=tk.NORMAL)
            self.button.config(text=self.__class__.TEXT_NONE)
            flag_counter.set(flag_counter.get() + 1)
        else:
            self.is_disabled = True
            self.is_marked = True
            self.button.config(state=tk.DISABLED, disabledforeground="#FF0000")
            self.button.config(text=self.__class__.TEXT_MARK)
            flag_counter.set(flag_counter.get() - 1)

    def reset(self, value):
        self.value = value
        self.is_bomb = (value < 0)
        self.is_empty = (value == 0)
        self.is_marked = False
        self.is_disabled = False
        self.button.config(state=tk.NORMAL, text="")
        self.button["background"] = self.BACKGROUND_COLOR_NORMAL


class FieldFrame(tk.Frame, object):
    TEXT_WIN = u"\u263a" + 'YOU WIN!'
    TEXT_LOSE = u"\u2639" + 'YOU LOSE!'

    def __init__(self, root, cols=const.WIDTH, rows=const.HEIGHT,
                 bomb_number=const.BOMBS):
        super(FieldFrame, self).__init__(root,
                                         width=const.BTN_SIZE_RATIO * cols,
                                         height=const.BTN_SIZE_RATIO * rows)
        self.grid(row=1, column=0, sticky=tk.NSEW)
        self.grid_propagate(False)
        self.cells = []
        self.cols = cols
        self.rows = rows
        self.bomb_number = bomb_number
        self.is_loser = False
        self.undefined_cells = cols * rows - bomb_number
        self.generate_field()
        self.set_buttons()
        flag_counter.set(self.bomb_number)

    def set_buttons(self):
        def loss_func():
            if self.is_loser:
                return
            self.is_loser = True
            for i in range(self.cols):
                for j in range(self.rows):
                    index = j * self.cols + i
                    self.cells[index].open()
            timer.stop_clock()
            label_flag_counter["foreground"] = "red"
            flag_counter_text.set(self.TEXT_LOSE)
            return

        def count_func():
            self.undefined_cells = self.undefined_cells - 1
            if self.undefined_cells == 0 and not self.is_loser:
                for i in range(self.cols):
                    for j in range(self.rows):
                        index = j * self.cols + i
                        self.cells[index].is_marked = False
                        self.cells[index].mark()
                        self.cells[index].is_marked = False
                timer.stop_clock()
                label_flag_counter["foreground"] = "green"
                flag_counter_text.set(self.TEXT_WIN)

        def empty_cell_func(col, row):
            def result():
                for i in range(max(0, col - 1), min(self.cols, col + 2)):
                    for j in range(max(0, row - 1), min(self.rows, row + 2)):
                        index = j * self.cols + i
                        self.cells[index].open()

            return result

        for j in range(self.rows):
            for i in range(self.cols):
                btnframe = tk.Frame(self, width=const.BTN_SIZE_RATIO,
                                    height=const.BTN_SIZE_RATIO)
                btnframe.grid_propagate(False)
                btnframe.propagate(False)
                btnframe.grid(row=j, column=i, sticky=tk.NSEW)
                cell = Cell(tk.Button(btnframe), self.field[j * self.cols + i],
                            loss_func, count_func, empty_cell_func(i, j))
                self.cells.append(cell)

    def generate_field(self):
        field = [0 for x in range(self.cols * self.rows)]
        bomb_indexes = random.sample(range(self.cols * self.rows),
                                     self.bomb_number)
        for i in range(self.bomb_number):
            x = bomb_indexes[i] % self.rows
            y = bomb_indexes[i] // self.rows
            for j in range(max(0, x - 1), min(x + 2, self.rows)):
                for k in range(max(0, y - 1), min(y + 2, self.cols)):
                    index = k * self.rows + j
                    field[index] = field[index] + 1
        for i in range(self.bomb_number):
            field[bomb_indexes[i]] = -1
        self.field = field

    def restart(self):
        self.is_loser = False
        self.undefined_cells = self.cols * self.rows - self.bomb_number
        self.generate_field()
        timer.reset_clock()
        flag_counter.set(self.bomb_number)
        label_flag_counter["foreground"] = "black"
        for i in range(self.cols):
            for j in range(self.rows):
                index = j * self.cols + i
                self.cells[index].reset(self.field[j * self.cols + i])


class TopFrame(tk.Frame, object):
    def __init__(self, root, cols=const.WIDTH, field_restart=None):
        super(TopFrame, self).__init__(root, width=const.BTN_SIZE_RATIO * cols)
        self.grid(row=0, column=0)
        timer_label = tk.Label(self, textvariable=timer_text)
        timer_label.grid(row=0, column=0, sticky=tk.W)
        self.restart_button = tk.Button(self, text="Restart game",
                                        command=field_restart)
        self.restart_button.grid(row=0, column=1)
        global label_flag_counter
        label_flag_counter = tk.Label(self, textvariable=flag_counter_text)
        label_flag_counter.grid(row=0, column=2, sticky=tk.W)


def show_settings_window(*_):
    sw = tk.Toplevel(root)
    sw.focus_set()
    sw.grab_set()
    sw.resizable(False, False)
    sw.title(const.TEXTS['settings.caption'])

    label_mines = tk.Label(sw, text=const.TEXTS['settings.mines'])
    label_mines.grid(row=0, column=0)

    spinbox_mines = tk.Spinbox(
        sw, from_=1, to=const.WIDTH * const.HEIGHT,
        textvariable=tk.IntVar(sw, const.BOMBS),
    )

    def set_mines():
        const.BOMBS = spinbox_mines.get()

    spinbox_mines.grid(row=0, column=1)
    spinbox_mines.config(command=set_mines)

    label_width = tk.Label(sw, text=const.TEXTS['settings.width'])
    label_width.grid(row=1, column=0)
    spinbox_width = tk.Spinbox(
        sw, from_=1, to=99,
        textvariable=tk.IntVar(sw, const.WIDTH),
    )

    def set_width():
        const.BOMBS = spinbox_width.get()

    spinbox_width.grid(row=1, column=1)
    spinbox_width.config(command=set_width)

    label_height = tk.Label(sw, text=const.TEXTS['settings.height'])
    label_height.grid(row=2, column=0)
    spinbox_height = tk.Spinbox(
        sw, from_=1, to=99,
        textvariable=tk.IntVar(sw, const.HEIGHT),
    )

    def set_height():
        const.BOMBS = spinbox_height.get()

    spinbox_height.grid(row=2, column=1)
    spinbox_width.config(command=set_height)


root = tk.Tk()
root.title('Minesweeper')
root.resizable(False, False)
root.bind("<o>", show_settings_window)
root.bind("<O>", show_settings_window)


def counter_text(*args):
    flag_counter_text.set("Bombs: {}".format(flag_counter.get()))


flag_counter = tk.IntVar()
flag_counter.trace("w", counter_text)
flag_counter_text = tk.StringVar(root)
flag_counter_text.set("Bombs: {}".format(flag_counter.get()))

timer_text = tk.StringVar(root)
timer = Timer(timer_text)

import src.constants as const
from src.handlers import Timer, Checker
import tkinter as tk

timer = Timer()
flag_checker = Checker(const.BOMBS)


class Cell(object):
    TEXT_BOMB = u"\u2738"
    TEXT_MARK = u"\u2690"
    TEXT_NONE = ""

    def __init__(self, button, value, loss_func, count_func, empty_cell_func):
        button.bind("<Button-1>", self.open)
        button.bind("<Button-3>", self.mark)
        button.pack(expand=True, fill=tk.BOTH)
        self.button = button
        self.value = value
        self.loss_func = loss_func
        self.count_func = count_func
        self.empty_cell_func = empty_cell_func
        self.is_bomb = (value < 0)
        self.is_empty = (value == 0)
        self.is_marked = False
        self.is_disabled = False

    def open(self, event=None):
        if self.is_disabled:
            return
        self.is_disabled = True
        self.button.config(state=tk.DISABLED, bg="#BBBBBB",
                           disabledforeground="#0000FF")
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
            flag_checker.count += 1
        else:
            self.is_disabled = True
            self.is_marked = True
            self.button.config(state=tk.DISABLED, disabledforeground="#FF0000")
            self.button.config(text=self.__class__.TEXT_MARK)
            flag_checker.count -= 1


class FieldFrame(tk.Frame, object):
    def __init__(self, root, cols=const.WIDTH, rows=const.HEIGHT):
        super(FieldFrame, self).__init__(root,
                                         width=const.BTN_SIZE_RATIO * cols,
                                         height=const.BTN_SIZE_RATIO * rows)
        self.grid(row=1, column=0, sticky=tk.NSEW)
        self.grid_propagate(False)
        self.cells = []
        self.cols = cols
        self.rows = rows
        self.is_loser = False
        self.undefined_cells = cols * rows - const.BOMBS

    def set_buttons(self, values):
        def loss_func():
            if self.is_loser:
                return
            self.is_loser = True
            for i in range(self.cols):
                for j in range(self.rows):
                    index = j * self.cols + i
                    self.cells[index].open()
            print("You have LOST!!!")
            timer.stop_clock()
            flag_checker.stop_clock(win=False)
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
                print("You have WON!!!")
                timer.stop_clock()
                flag_checker.stop_clock(win=True)

        def empty_cell_func(col, row):
            def result():
                for i in range(max(0, col - 1), min(self.cols, col + 2)):
                    for j in range(max(0, row - 1), min(self.rows, row + 2)):
                        index = j * self.cols + i
                        self.cells[index].open()

            return result

        self.values = values
        for j in range(self.rows):
            for i in range(self.cols):
                btnframe = tk.Frame(self, width=const.BTN_SIZE_RATIO,
                                    height=const.BTN_SIZE_RATIO)
                btnframe.grid_propagate(False)
                btnframe.propagate(False)
                btnframe.grid(row=j, column=i, sticky=tk.NSEW)
                cell = Cell(tk.Button(btnframe), values[j * self.cols + i],
                            loss_func, count_func, empty_cell_func(i, j))
                self.cells.append(cell)


class TopFrame(tk.Frame, object):
    def __init__(self, root, cols=const.WIDTH):
        super(TopFrame, self).__init__(root, width=const.BTN_SIZE_RATIO * cols)
        self.grid(row=0, column=0)
        timer.label = tk.Label(self, text="00:00")
        timer.label.grid(row=0, column=0, sticky=tk.W)
        self.restart_button = tk.Button(self, text="Restart game",
                                        command=self.restart_pressed)
        self.restart_button.grid(row=0, column=1)
        flag_checker.label = tk.Label(self, text='')
        flag_checker.label.grid(row=0, column=2, sticky=tk.W)

    def restart_pressed(self):
        print("To be done")


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

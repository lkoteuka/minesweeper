import src.constants as const
import tkinter as tk


class Cell():
    TEXT_BOMB = u"\u2739"
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
            self.button.config(text=self.__class__.TEXT_BOMB)
            self.loss_func()
            return
        if self.is_empty:
            self.empty_cell_func()
        else:
            self.button.config(text=self.value)
        self.count_func()

    def mark(self, event=None):
        if self.is_disabled and not self.is_marked:
            return
        if self.is_marked:
            self.is_disabled = False
            self.is_marked = False
            self.button.config(state=tk.NORMAL)
            self.button.config(text=self.__class__.TEXT_NONE)
        else:
            self.is_disabled = True
            self.is_marked = True
            self.button.config(state=tk.DISABLED, disabledforeground="#FF0000")
            self.button.config(text=self.__class__.TEXT_MARK)


class FieldFrame(tk.Frame):
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


class TopFrame(tk.Frame):
    def __init__(self, root, cols=const.WIDTH):
        super(TopFrame, self).__init__(root, width=const.BTN_SIZE_RATIO * cols)
        self.grid(row=0, column=0)
        self.timer = tk.Label(self, text="0")
        self.timer.grid(row=0, column=0, sticky=tk.W)
        self.restart_button = tk.Button(self, text="Restart game",
                                        command=self.restart_pressed)
        self.restart_button.grid(row=0, column=1)
        self.timer = tk.Label(self, text=const.BOMBS)
        self.timer.grid(row=0, column=2, sticky=tk.E)

    def restart_pressed(self):
        print("To be done")


root = tk.Tk()
root.resizable(False, False)

import src.constants as const
import tkinter as tk


class FieldFrame(tk.Frame):
    def __init__(self, root, cols=const.WIDTH, rows=const.HEIGHT):
        super(FieldFrame, self).__init__(root,
                                         width=const.BTN_SIZE_RATIO * cols,
                                         height=const.BTN_SIZE_RATIO * rows)
        self.grid(row=1, column=0, sticky=tk.NSEW)
        self.grid_propagate(False)
        self.cols = cols
        self.rows = rows

    def set_buttons(self, values):
        self.buttons = []
        self.values = values
        for j in range(self.rows):
            for i in range(self.cols):
                def button_func(col, row, **kwargs):
                    def result(**kwargs):
                        self.button_pressed(col, row, **kwargs)

                    return result

                btnframe = tk.Frame(self,
                                    width=const.BTN_SIZE_RATIO,
                                    height=const.BTN_SIZE_RATIO)
                btnframe.grid_propagate(False)
                btnframe.propagate(False)
                btnframe.grid(row=j, column=i, sticky=tk.NSEW)
                btn = tk.Button(btnframe, command=button_func(i, j))
                btn.pack(expand=True, fill=tk.BOTH)
                self.buttons.append(btn)

    def button_pressed(self, col, row, **kwargs):
        self.open_button(col, row)

    def open_button(self, col, row):
        index = row * self.cols + col
        button = self.buttons[index]
        if str(button['state']) == 'disabled':
            return
        value = self.values[index]
        button.config(state=tk.DISABLED, fg='red')
        if value > 0:
            button.config(text=value)
        elif value < 0:
            button.config(text=u"\u2620")
        else:
            for i in range(max(0, col - 1), min(self.cols, col + 2)):
                for j in range(max(0, row - 1), min(self.rows, row + 2)):
                    self.open_button(i, j)


class TopFrame(tk.Frame, object):
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

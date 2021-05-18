import src.constants as const
import tkinter as tk


class FieldFrame(tk.Frame, object):
    def __init__(self, root, cols=const.WIDTH, rows=const.HEIGHT):
        super(FieldFrame, self).__init__(root,
                                         width=const.BTN_SIZE_RATIO * cols,
                                         height=const.BTN_SIZE_RATIO * rows)
        self.grid(row=0, column=0, sticky=tk.NSEW)
        self.grid_propagate(False)
        self.cols = cols
        self.rows = rows

    def set_buttons(self, handlers):
        self.buttons = []
        for i in range(self.cols):
            for j in range(self.rows):
                index = j * self.cols + i
                btnframe = tk.Frame(self,
                                    width=const.BTN_SIZE_RATIO, height=const.BTN_SIZE_RATIO)
                btnframe.grid_propagate(False)
                btnframe.propagate(False)
                btnframe.grid(row=j, column=i, sticky=tk.NSEW)
                btn = tk.Button(btnframe, command=handlers[index])
                btn.pack(expand=True, fill=tk.BOTH)
                self.buttons.append(btn)

    def button_pressed(self, col, row, **kwargs):
        print(col, row)
        self.buttons[col][row]['background'] = 'PeachPuff'


root = tk.Tk()
root.resizable(False, False)

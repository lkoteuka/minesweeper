import constants as const
import tkinter as tk


class FieldFrame(tk.Frame, object):
    def __init__(self, root, width=const.WIDTH, height=const.HEIGHT):
        super(FieldFrame, self).__init__(root)
        self.grid(row=0, column=0, sticky=tk.NSEW)
        self.width = width
        self.height = height

    def set_buttons(self, handlers):
        self.buttons = []
        for i in range(self.width):
            for j in range(self.height):
                index = j * self.width + i
                btn = tk.Button(self, width=1, height=1, command=handlers[index])
                btn.grid(row=j, column=i)
                self.buttons.append(btn)

    def button_pressed(self, col, row, **kwargs):
        print(col, row)
        self.buttons[col][row]['background'] = 'PeachPuff'


root = tk.Tk()

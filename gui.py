from tkinter import *

WIDTH = HEIGHT = 8
class FieldFrame(Frame, object):
    def __init__(self, root, width=WIDTH, height=HEIGHT):
        super(FieldFrame, self).__init__(root)
        self.grid(row=0, column=0, sticky=NSEW)
        self.buttons = []
        for i in range(width):
            self.buttons.append([])

            for j in range(height):
                def button_func(col, row, **kwargs):
                    def result(**kwargs):
                        self.button_pressed(col, row, **kwargs)
                    return result

                btn = Button(self, width=2, height=1,
                             command=button_func(i, j))
                btn.grid(row=j, column=i)
                self.buttons[i].append(btn)

    def button_pressed(self, col, row, **kwargs):
        print(col, row)
        self.buttons[col][row]['background']='PeachPuff'
root = Tk()
field = FieldFrame(root, width=5, height=4)
root.mainloop()
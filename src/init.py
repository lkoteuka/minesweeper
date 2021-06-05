import src.gui as gui
import src.constants as const


def initialize(size_x=const.HEIGHT, size_y=const.WIDTH, bomb_number=const.BOMBS):
    """ Function initializes GUI, sets field's sizes, places bombs, sets user controls.

    :param size_x: length of map in cells
    :type size_x: int
    :param size_y: width of map in cells
    :type size_y: int
    """
    field = gui.FieldFrame(gui.root, cols=size_y, rows=size_x)
    gui.TopFrame(gui.root, cols=size_y, field_restart=field.restart)
    gui.root.mainloop()

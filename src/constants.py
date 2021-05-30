import gettext
import sys
import os

datapath = os.path.dirname(sys.argv[0])
gettext.install('minesweeper', datapath, names=("ngettext",))

HEIGHT = 10
WIDTH = 10
BOMBS = 10
BTN_SIZE_RATIO = 32

COLORS = {
    1: 'purple',
    2: 'green',
    3: 'red',
    4: 'yellow',
    5: 'brown',
    6: 'orange',
    7: 'pink',
    8: 'black'
}

TEXTS = {
    'settings.mines': _("Number of mines"),
    'settings.width': _("Width"),
    'settings.height': _("Height"),
    'settings.caption': _("Options"),
}

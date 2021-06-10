import sys
import os
import gettext
lang = gettext.translation('base', localedir='locales', languages=['ru', 'eng'])
lang.install()
_ = lang.gettext  # Russian

datapath = os.path.dirname(sys.argv[0])

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
    'settings.bombs': _("Bombs"),
    'settings.width': _("Width"),
    'settings.height': _("Height"),
    'settings.caption': _("Options"),
    'settings.win': _("YOU WIN!"),
    'settings.lose': _("YOU LOSE!"),
    'settings.restart': _("Restart game"),
    'settings.name': _("Minesweeper"),
}

import pgi
pgi.require_version('Gtk', '3.0')
pgi.install_as_gi()
# noinspection PyUnresolvedReferences
from gi.repository import Gtk, GdkPixbuf

import json

from symbols import SymbolGrid


class AacWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title='Hello Isaac')
        self.set_icon_from_file('isaac.svg')
        self.set_border_width(10)
        self.set_size_request(360, -1)
        self.set_resizable(False)

        self.notebook = Gtk.Notebook()
        self.notebook.popup_enable()
        self.add(self.notebook)

        with open('sheets.json') as f:
            sheets = json.load(f)
        for sheet_name, symbols in sheets.items():
            symbol_grid = SymbolGrid(parent=self, symbols=symbols)
            self.notebook.append_page(symbol_grid, Gtk.Label(sheet_name))

        self.show_all()
        self.connect('delete-event', Gtk.main_quit)


if __name__ == '__main__':
    win = AacWindow()
    Gtk.main()

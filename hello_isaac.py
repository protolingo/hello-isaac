import pgi
pgi.require_version('Gtk', '3.0')
pgi.install_as_gi()
# noinspection PyUnresolvedReferences
from gi.repository import Gtk, GdkPixbuf


from symbols import SymbolGrid


class AacWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title='Hello Isaac')
        self.set_icon_from_file('isaac.svg')
        self.set_border_width(10)
        self.set_size_request(500, -1)
        self.set_resizable(False)

        self.symbol_grid = SymbolGrid(parent=self)
        self.add(self.symbol_grid)
        self.show_all()
        self.connect('delete-event', Gtk.main_quit)


if __name__ == '__main__':
    win = AacWindow()
    Gtk.main()

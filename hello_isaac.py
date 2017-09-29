import pgi
pgi.require_version('Gtk', '3.0')
pgi.install_as_gi()
# noinspection PyUnresolvedReferences
from gi.repository import Gtk, GdkPixbuf

import glob
import os
import zipfile

import text_to_speech


def extract_symbols_if_necessary():
    if glob.glob('symbols/*.svg'):
        return

    print("Hold on, I'm extracting symbols...", end=' ')
    with zipfile.ZipFile('symbols.zip') as archive:
        archive.extractall('symbols')
    print('Done!')


class AacWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title='Hello Isaac')
        self.set_icon_from_file('isaac.svg')
        self.set_border_width(10)
        self.set_size_request(500, -1)
        self.set_resizable(False)

        self.create_symbol_grid()
        self.show_all()
        self.connect('delete-event', Gtk.main_quit)

    def create_symbol_grid(self):
        symbol_grid = Gtk.FlowBox()
        symbol_grid.set_selection_mode(Gtk.SelectionMode.NONE)
        self.add(symbol_grid)

        files = glob.glob('symbols/*.svg')[:24]
        for symbol in map(self.get_symbol, files):
            symbol_grid.add(symbol)

    def get_symbol(self, file):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(file, -1, 64, True)
        image = Gtk.Image.new_from_pixbuf(pixbuf)

        symbol = Gtk.Button()
        symbol.add(image)
        symbol.label = os.path.splitext(os.path.basename(file))[0]
        symbol.connect('clicked', self.on_symbol_clicked)
        return symbol

    def on_symbol_clicked(self, symbol):
        text_to_speech.say(symbol.label)


if __name__ == '__main__':
    extract_symbols_if_necessary()
    win = AacWindow()
    Gtk.main()

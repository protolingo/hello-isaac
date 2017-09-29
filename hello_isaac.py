import pgi
pgi.require_version('Gtk', '3.0')
pgi.install_as_gi()
# noinspection PyUnresolvedReferences
from gi.repository import Gtk, GdkPixbuf

import glob
import os
import zipfile

import text_to_speech


LEFT_BUTTON, RIGHT_BUTTON = 1, 3


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
        symbol.default_label = os.path.splitext(os.path.basename(file))[0]
        symbol.label = symbol.default_label
        symbol.connect('button-press-event', self.on_symbol_clicked)

        return symbol

    def on_symbol_clicked(self, symbol, event):
        if event.button == LEFT_BUTTON:
            text_to_speech.say(symbol.label)
        elif event.button == RIGHT_BUTTON:
            SymbolEditorDialog(self, symbol)


class SymbolEditorDialog(Gtk.Dialog):

    def __init__(self, parent, symbol):
        self.symbol = symbol
        super().__init__('Edit symbol', parent, True)
        self.set_border_width(10)

        # Remove the default box container and replace it with a grid.
        self.remove(self.get_content_area())
        grid = Gtk.Grid()
        self.add(grid)

        self.entry = Gtk.Entry(text=symbol.label)
        grid.attach(self.entry, 0, 0, 2, 1)

        save_button = Gtk.Button('Save')
        save_button.connect('clicked', self.on_save_button_clicked)
        grid.attach_next_to(save_button, self.entry, Gtk.PositionType.BOTTOM, 1, 1)

        reset_button = Gtk.Button('Reset')
        reset_button.connect('clicked', self.on_reset_button_clicked)
        grid.attach_next_to(reset_button, save_button, Gtk.PositionType.RIGHT, 1, 1)

        self.show_all()

    def on_save_button_clicked(self, _):
        self.symbol.label = self.entry.get_text()
        self.destroy()

    def on_reset_button_clicked(self, _):
        self.entry.set_text(self.symbol.default_label)


if __name__ == '__main__':
    extract_symbols_if_necessary()
    win = AacWindow()
    Gtk.main()

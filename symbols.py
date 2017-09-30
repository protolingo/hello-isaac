import pgi
pgi.require_version('Gtk', '3.0')
pgi.install_as_gi()
# noinspection PyUnresolvedReferences
from gi.repository import Gtk, GdkPixbuf

import glob
import os
import zipfile

import text_to_speech

from labels import labels


LEFT_BUTTON, RIGHT_BUTTON = 1, 3


def extract_symbols_if_necessary():
    if glob.glob('symbols/*.svg'):
        return

    print("Hold on, I'm extracting symbols...", end=' ')
    with zipfile.ZipFile('symbols.zip') as archive:
        archive.extractall('symbols')
    print('Done!')


class SymbolGrid(Gtk.FlowBox):

    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.set_selection_mode(Gtk.SelectionMode.NONE)

        extract_symbols_if_necessary()
        files = glob.glob('symbols/*.svg')[:24]
        for symbol in map(self.get_symbol, files):
            self.add(symbol)

    def get_symbol(self, file):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(file, -1, 64, True)
        image = Gtk.Image.new_from_pixbuf(pixbuf)

        symbol = Gtk.Button()
        symbol.add(image)
        symbol.default_label = os.path.splitext(os.path.basename(file))[0]
        symbol.label = labels[symbol.default_label]
        symbol.connect('button-press-event', self.on_symbol_clicked)

        return symbol

    def on_symbol_clicked(self, symbol, event):
        if event.button == LEFT_BUTTON:
            text_to_speech.say(symbol.label)
        elif event.button == RIGHT_BUTTON:
            SymbolEditorDialog(self.parent, symbol)


class SymbolEditorDialog(Gtk.Dialog):

    SAVE, RESET = 1, 2

    def __init__(self, parent, symbol):
        self.symbol = symbol
        super().__init__('Edit symbol', parent, True)
        self.set_border_width(10)

        self.entry = Gtk.Entry(text=symbol.label, activates_default=True)
        box = self.get_content_area()
        box.add(self.entry)

        self.add_button('_Save', self.SAVE)
        self.add_button('_Reset', self.RESET)
        self.connect('response', self.on_response)
        self.set_default_response(self.SAVE)

        self.show_all()

    def on_response(self, _, response):
        if response == self.SAVE:
            self.symbol.label = self.entry.get_text()
            labels[self.symbol.default_label] = self.symbol.label
            self.destroy()
        elif response == self.RESET:
            self.entry.set_text(self.symbol.default_label)


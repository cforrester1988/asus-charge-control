# type: ignore
import gi

gi.require_version("Gtk", "3.0")

from os.path import abspath, dirname, join
from gi.repository import Gtk, Gio

import asuscharge
from asuscharge import __version__

CURRENT_PATH = abspath(dirname(__file__))


class Application(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id="ca.cforrester.asuscharge-gtk",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
        )
        self.builder = Gtk.Builder()
        self.builder.add_from_file(join(CURRENT_PATH, "main.glade"))

        self.mainWindow: Gtk.Window = self.builder.get_object("MainWindow")
        self.builder.connect_signals(self.mainWindow)
        self.mainWindow.connect("destroy", Gtk.main_quit)

        self.aboutWindow: Gtk.AboutDialog = self.builder.get_object("AboutWindow")
        self.aboutWindow.set_version(f"v{__version__}")
        self.aboutButton: Gtk.Button = self.builder.get_object("AboutButton")
        self.aboutButton.connect("clicked", self.show_about)

        self.chargeScale: Gtk.Scale = self.builder.get_object("ChargeScale")
        self.chargeScale.connect(
            "format-value", lambda scale, value, user_data=None: f"{int(value)}%"
        )
        self.chargeScale.add_mark(100.0, Gtk.PositionType.RIGHT)
        self.chargeScale.add_mark(80.0, Gtk.PositionType.RIGHT)
        self.chargeScale.add_mark(60.0, Gtk.PositionType.RIGHT)

        self.mainWindow.present()

    def show_about(self, button):
        self.aboutWindow.run()
        self.aboutWindow.hide()


if __name__ == "__main__":
    app = Application()
    Gtk.main()

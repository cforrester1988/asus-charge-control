# type: ignore
import asyncio
import gi

gi.require_version("Gtk", "3.0")

from os.path import abspath, dirname, join
from os import getuid
from sys import argv, exit
from platform import system, release
from gi.repository import Gtk, Gio

import asuscharge
from asuscharge import __version__

_MIN_KERNEL_VERSION = "5.4"
_ASUS_MODULE_NAME = "asus_nb_wmi"
_CURRENT_PATH = abspath(dirname(__file__))
_VERSION = (
    f"{asuscharge.__name__} v{asuscharge.__version__}\n" f"{__name__} v{__version__}"
)


class Application(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id="ca.cforrester.asuscharge-gtk",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
        )
        err = None
        if not asuscharge.supported_platform():
            err = f"Unsupported platform: {system()}.\n{argv[0]} only runs on Linux systems."
        elif not asuscharge.supported_kernel():
            err = f"Unsupported kernel version: {release()}\n{argv[0]} requires a kernel version >= {_MIN_KERNEL_VERSION}"
        elif not asuscharge.module_loaded():
            err = f"Module not loaded: the '{_ASUS_MODULE_NAME}' kernel module must be running."
        if err:
            dialog = Gtk.MessageDialog(
                flags=Gtk.DialogFlags.DESTROY_WITH_PARENT,
                type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CLOSE,
                message_format=err,
            )
            dialog.run()
            exit()
        self.controller = asuscharge.ChargeThresholdController()
        self.builder = Gtk.Builder()
        self.builder.add_from_file(join(_CURRENT_PATH, "main.glade"))
        self.css = Gtk.CssProvider()
        self.css.load_from_path(join(_CURRENT_PATH, "main.css"))

        main_window: Gtk.Window = self.builder.get_object("MainWindow")
        main_window.connect("destroy", Gtk.main_quit)

        aboutButton: Gtk.Button = self.builder.get_object("AboutButton")
        aboutButton.connect("clicked", self.show_about)

        unlock_infobar: Gtk.InfoBar = self.builder.get_object("UnlockInfoBar")
        unlock_infobar.set_revealed(True)
        unlock_button: Gtk.Button = self.builder.get_object("UnlockButton")
        unlock_button.connect("clicked", self.unlock_button_clicked)

        charge_scale: Gtk.Scale = self.builder.get_object("ChargeScale")
        charge_scale.connect(
            "format-value", lambda scale, value, user_data=None: f"{int(value)}%"
        )
        charge_scale.add_mark(100.0, Gtk.PositionType.RIGHT)
        charge_scale.add_mark(80.0, Gtk.PositionType.RIGHT)
        charge_scale.add_mark(60.0, Gtk.PositionType.RIGHT)
        charge_adj: Gtk.Adjustment = self.builder.get_object("ChargeAdjustment")
        asyncio.run(self.update_threshold())
        charge_adj.connect("value-changed", self.scale_moved)

        main_window.present()

    def show_about(self, button):
        about_window: Gtk.AboutDialog = self.builder.get_object("AboutWindow")
        # about_window.set_version(f"v{__version__}")
        about_window.set_version(_VERSION)
        about_window.run()
        about_window.hide()

    def unlock_button_clicked(self, button):
        charge_scale: Gtk.ChargeScale = self.builder.get_object("ChargeScale")
        unlock_infobar: Gtk.InfoBar = self.builder.get_object("UnlockInfoBar")
        scheduler_button: Gtk.Button = self.builder.get_object("SchedulerButton")
        charge_scale.set_sensitive(True)
        unlock_infobar.set_revealed(False)
        scheduler_button.set_sensitive(True)

    def scale_moved(self, scale: Gtk.Scale):
        s: Gtk.Label = self.builder.get_object("WarningLabel")
        if not scale.get_value() in (60, 80, 100):
            s.set_visible(visible=True)
        else:
            s.set_visible(visible=False)

    async def update_threshold(self) -> None:
        charge_adj: Gtk.Adjustment = self.builder.get_object("ChargeAdjustment")
        charge_adj.set_value(self.controller.end_threshold)


if __name__ == "__main__":
    app = Application()
    Gtk.main()

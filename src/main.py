# main.py
#
# SPDX-FileCopyrightText: 2023  Benedek Dévényi
# SPDX-License-Identifier: GPL-3.0-or-later

import sys

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gio, Gtk

from .window import MidimonitorWindow

APPLICATION_ID = "io.github.rdbende.MidiMonitor"


class MidimonitorApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self, version) -> None:
        super().__init__(
            application_id=APPLICATION_ID,
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )

        self.create_action("quit", lambda *_: self.quit(), ["<primary>q"])
        self.create_action("about", self.on_about_action)

        self.version = version

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = MidimonitorWindow(application=self)
        win.present()

    def on_about_action(self, *_):
        """Callback for the app.about action."""
        Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name="MIDI Monitor",
            application_icon=APPLICATION_ID,
            version=self.version,
            developer_name="Benedek Dévényi",
            developers=["Benedek Dévényi"],
        ).present()

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = MidimonitorApplication(version)
    return app.run(sys.argv)

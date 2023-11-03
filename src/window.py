# window.py
#
# SPDX-FileCopyrightText: 2023  Benedek Dévényi
# SPDX-License-Identifier: GPL-3.0-or-later

from functools import partial
from typing import Literal

import mido
from gi.repository import Adw, GLib, Gtk


def get_pretty_inputs(raw_names) -> list[str]:
    pretty_names = []
    for name in raw_names:
        # name = "Arturia MiniLab mkII:Arturia MiniLab mkII MIDI 1 20:0"
        name = name.split(":", 1)[1]  # name = "Arturia MiniLab mkII MIDI 1 20:0"
        name = name.rsplit(" ", 1)[0]  # name = "Arturia MiniLab mkII MIDI 1"
        pretty_names.append(name)

    return pretty_names


@Gtk.Template(resource_path="/io/github/rdbende/MidiMonitor/window.ui")
class MidimonitorWindow(Adw.ApplicationWindow):
    __gtype_name__ = "MidimonitorWindow"

    listbox = Gtk.Template.Child()
    scrolledwindow = Gtk.Template.Child()
    controller_chooser = Gtk.Template.Child()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.current_port = None
        self.message_callback = partial(GLib.idle_add, self.append_message)

        self.input_ports = mido.get_input_names()
        self.controllers = Gtk.StringList(strings=get_pretty_inputs(self.input_ports))

        self.controller_chooser.props.model = self.controllers
        self.controller_chooser.connect("notify::selected", self.select_port)
        self.controller_chooser.props.selected = 1

        self.messages = Gtk.StringList()
        self.listbox.bind_model(self.messages, self.create_action_row)
        self.messages.connect("items-changed", self.scroll_to_bottom)

    def select_port(self, *_) -> None:
        try:
            self.current_port.close()
        except AttributeError:
            pass
        finally:
            port_name = self.input_ports[self.controller_chooser.props.selected]
            self.current_port = mido.open_input(
                port_name, callback=self.message_callback
            )

    def create_action_row(self, msg) -> Adw.ActionRow:
        kind, rest = msg.props.string.split(" ", 1)
        kind = " ".join(kind.split("_")).title()
        return Adw.ActionRow(title=kind, subtitle=rest)

    def append_message(self, message) -> Literal[False]:
        self.messages.append(str(message))
        return False

    def scroll_to_bottom(self, *_) -> None:
        adj = self.scrolledwindow.get_vadjustment()
        adj.set_value(adj.get_upper() + 1000)

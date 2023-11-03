# window.py
#
# SPDX-FileCopyrightText: 2023  Benedek Dévényi
# SPDX-License-Identifier: GPL-3.0-or-later

from functools import partial
from typing import Literal

import mido
from gi.repository import Adw, GLib, Gtk, Gio, GObject

from .list_item import ListItem


def get_pretty_inputs(raw_names) -> list[str]:
    pretty_names = []
    for name in raw_names:
        # name = "Arturia MiniLab mkII:Arturia MiniLab mkII MIDI 1 20:0"
        name = name.split(":", 1)[1]  # name = "Arturia MiniLab mkII MIDI 1 20:0"
        name = name.rsplit(" ", 1)[0]  # name = "Arturia MiniLab mkII MIDI 1"
        pretty_names.append(name)

    return pretty_names


class Message(GObject.GObject):
    kind = GObject.property(type=str, flags=GObject.PARAM_READWRITE)
    text = GObject.property(type=str, flags=GObject.PARAM_READWRITE)

    def __init__(self, kind, text):
        GObject.GObject.__init__(self)
        self.props.kind = kind
        self.props.text = text

GObject.type_register(Message)


@Gtk.Template(resource_path="/io/github/rdbende/MidiMonitor/window.ui")
class MidimonitorWindow(Adw.ApplicationWindow):
    __gtype_name__ = "MidimonitorWindow"

    list_view = Gtk.Template.Child()
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

        self.messages = Gio.ListStore()
        self.selection_model = Gtk.NoSelection(model=self.messages)
        self.list_view.props.model = self.selection_model

        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", lambda _, item: item.set_child(ListItem()))
        factory.connect("bind", self.display_message)

        self.list_view.props.factory = factory

    def display_message(self, _, item) -> None:
        message = item.get_item()
        box = item.get_child()
        box.kind_label.set_label(message.kind)
        box.rest_label.set_label(message.text)

    def append_message(self, message) -> Literal[False]:
        kind = " ".join(message.type.split("_")).title()
        rest = str(message).split(" ", 1)[1].replace(" ", "; ").replace("=", ": ")
        self.messages.append(Message(kind=kind, text=rest))
        GLib.idle_add(self.scroll_to_bottom)
        return False

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

    def scroll_to_bottom(self, *_) -> None:
        adj = self.scrolledwindow.get_vadjustment()
        adj.set_value(adj.get_upper())

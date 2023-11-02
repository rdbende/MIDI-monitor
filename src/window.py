# window.py
#
# SPDX-FileCopyrightText: 2023  Benedek Dévényi
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk


@Gtk.Template(resource_path="/io/github/rdbende/MidiMonitor/window.ui")
class MidimonitorWindow(Adw.ApplicationWindow):
    __gtype_name__ = "MidimonitorWindow"

    listbox = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.model = Gtk.StringList()
        self.listbox.bind_model(self.model, self.create_action_row)

    def create_action_row(self, msg):
        message = msg.props.string
        kind, *rest = message.split()
        kind = " ".join(kind.split("_")).title()
        return Adw.ActionRow(title=kind, subtitle=" ".join(rest))

    def add_message(self, msg):
        self.model.append(str(msg))
        return False

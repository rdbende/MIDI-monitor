# list_item.py
#
# SPDX-FileCopyrightText: 2023  Benedek Dévényi
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk


@Gtk.Template(resource_path="/io/github/rdbende/MidiMonitor/list_item.ui")
class ListItem(Gtk.Box):
    __gtype_name__ = "ListItem"

    kind_label = Gtk.Template.Child()
    rest_label = Gtk.Template.Child()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

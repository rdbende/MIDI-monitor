# window.py
#
# SPDX-FileCopyrightText: 2023  Benedek Dévényi
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk


@Gtk.Template(resource_path="/io/github/rdbende/MidiMonitor/window.ui")
class MidimonitorWindow(Adw.ApplicationWindow):
    __gtype_name__ = "MidimonitorWindow"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

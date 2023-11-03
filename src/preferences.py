# preferences.py
#
# SPDX-FileCopyrightText: 2023  Benedek Dévényi
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk


@Gtk.Template(resource_path="/io/github/rdbende/MidiMonitor/preferences.ui")
class PrefsWindow(Adw.PreferencesWindow):
    __gtype_name__ = "PrefsWindow"

    advanced_mode_switch = Gtk.Template.Child()
    history_items_spin = Gtk.Template.Child()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


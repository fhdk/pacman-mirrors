#!/usr/bin/env python
#
# This file is part of pacman-mirrors.
#
# pacman-mirrors is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pacman-mirrors is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pacman-mirrors.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Frede Hundewadt <echo ZmhAbWFuamFyby5vcmcK | base64 -d>

"""Pacman-Mirrors Console UI Module"""

import npyscreen

from collections import namedtuple

from pacman_mirrors.functions.conversion import list_to_tuple
from pacman_mirrors.functions.conversion import rows_from_tuple
from pacman_mirrors.constants import txt
from pacman_mirrors.translation import i18n

_ = i18n.language.gettext


class ConsoleUI(npyscreen.NPSAppManaged):
    """App"""

    def __init__(self, server_list: list, random: bool, default: bool, custom_list: list, is_done: bool):
        npyscreen.NPSAppManaged.__init__(self)
        self.title = txt.I_TITLE_RANDOM if random else txt.I_TITLE
        if default:
            self.title = "Pacman-Mirrors"

        # Server lists
        self.custom_list = custom_list
        self.is_done = is_done
        self.random = random
        self.default = default

        header_cols = {"country": txt.I_COUNTRY,
                       "speed": txt.I_RESPONSE,
                       "url": txt.I_URL}
        template = namedtuple("Server", ["country",
                                         "speed",
                                         "url"])

        main_server_list = [header_cols]

        main_server_list.extend(server_list)

        servers = (list_to_tuple(list_data=main_server_list, named_tuple=template))

        self.list_title = txt.I_LIST_TITLE
        self.server_rows = rows_from_tuple(servers=servers)
        self.header_row = ("{:<5}".format(txt.I_USE) +
                           (self.server_rows[0].replace("|", " ").strip()))
        del self.server_rows[0]

    def main(self):
        """Main"""

        # setup form
        mainform = npyscreen.Form(name=self.title)

        mainform.add(npyscreen.TitleFixedText, name=self.list_title)

        mainform.add(npyscreen.TitleFixedText, name=self.header_row)

        selected_servers = mainform.add(npyscreen.MultiSelect,
                                        max_height=0,
                                        name=self.list_title,
                                        value=[],
                                        values=self.server_rows,
                                        scroll_exit=True)
        mainform.edit()  # activate form

        self.done(selection=selected_servers.get_selected_objects())  # done

    def done(self, selection: list) -> None:
        """After editing
        :param selection:
        """
        if selection:
            for mirror in selection:
                server = mirror.split("|")
                self.custom_list.append({"country": server[0].strip(),
                                         "speed": server[1].strip(),
                                         "url": server[2].strip()})
        self.is_done = True
        self.setNextForm(None)


def run(server_list: list, random: bool, custom_list: list, is_done: bool, default: bool = False) -> object:
    """Run"""
    app = ConsoleUI(server_list, random, default, custom_list, is_done)
    app.run()
    return app

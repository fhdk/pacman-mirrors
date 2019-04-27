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

"""Pacman-Mirrors Interactive Mirror List Builder Module"""

from operator import itemgetter
from random import shuffle

from pacman_mirrors.functions.filter_mirror_status_functions import \
    filter_bad_mirrors, filter_error_mirrors, filter_poor_mirrors

from pacman_mirrors.constants import txt

from pacman_mirrors.functions.convertFn import \
    translate_interactive_to_pool, translate_pool_to_interactive

from pacman_mirrors.functions.filter_mirror_pool_functions import \
    filter_mirror_country, filter_mirror_protocols, filter_user_branch

from pacman_mirrors.functions.outputFn import \
    write_custom_mirrors_json, write_pacman_mirror_list

from pacman_mirrors.functions.sortMirrorFn import sort_mirror_pool
from pacman_mirrors.functions.testMirrorFn import test_mirror_pool
from pacman_mirrors.functions import util


def build_working_pool(self) -> list:
    """
    Apply country filter
    """
    pool_result = filter_mirror_country(mirror_pool=self.mirrors.mirror_pool, country_pool=self.selected_countries)
    """
    Apply bad mirrors filter
    """
    pool_result = filter_bad_mirrors(mirror_pool=pool_result)
    """
    Apply error mirrors filter
    """
    pool_result = filter_error_mirrors(mirror_pool=pool_result)
    """
    Apply protocol filter
    If config.protols has content, that is a user decision and as such
    it has nothing to do with the reasoning regarding mirrors
    which might or might not be up-to-date
    """
    try:
        _ = self.config["protocols"][0]
        pool_result = filter_mirror_protocols(mirror_pool=pool_result, protocols=self.config["protocols"])
    except IndexError:
        pass
    """
    Apply interval filter
    """
    if self.no_status and self.interval:
        pool_result = filter_poor_mirrors(mirror_pool=pool_result, interval=self.interval)

    return pool_result


def build_mirror_list(self) -> None:
    """
    Prompt the user to select the mirrors with a gui.
    Outputs a "custom" mirror file
    Outputs a pacman mirrorlist,
    """

    worklist = build_working_pool(self)

    # rank or shuffle the mirrorlist before showing the ui
    if not self.default:
        if self.config["method"] == "rank":
            worklist = test_mirror_pool(self=self, worklist=worklist)
            worklist = sort_mirror_pool(worklist=worklist, field="resp_time", reverse=False)
        else:
            shuffle(worklist)
    """
    Create a list for display in ui.
    The gui and the console ui expect the supplied list
    to be in the old country dictionary format.
    {
        "country": "country_name",
        "resp_time": "m.sss",
        "last_sync": "HHh MMm",
        "url": "http://server/repo/"
    }
    Therefore we have to create a list in the old format,
    thus avoiding rewrite of the ui and related functions.
    We subseqently need to translate the result into:
    a. a mirrorfile in the new json format,
    b. a mirrorlist in pacman format.
    As of version 4.8.x the last sync field contents is a string
    with the hours and minutes more human readable eg. 03h 33m
    """
    interactive_list = translate_pool_to_interactive(mirror_pool=worklist, tty=self.tty)

    # import the right ui
    if self.no_display:
        # in console mode
        from pacman_mirrors.dialogs import consoleui as ui
    else:
        # gobject introspection is present and accounted for
        from pacman_mirrors.dialogs import graphicalui as ui

    interactive = ui.run(server_list=interactive_list, random=self.config["method"] == "random",
                         default=self.default)

    # process user choices
    if interactive.is_done:
        """
        translate interactive list back to our json format
        """
        custom_pool, mirror_list = translate_interactive_to_pool(selection=interactive.custom_list,
                                                                 mirror_pool=self.mirrors.mirror_pool, tty=self.tty)
        """
        Try selected method on the mirrorlist
        """
        try:
            _ = mirror_list[0]
            if self.default:
                if self.config["method"] == "rank":
                    mirror_list = test_mirror_pool(self=self, worklist=mirror_list)
                    mirror_list = sorted(mirror_list, key=itemgetter("resp_time"))
                else:
                    shuffle(mirror_list)
        except IndexError:
            pass

        """
        Write custom mirror pool
        Write mirrorlist
        """
        try:
            _ = custom_pool[0]
            self.custom = True
            self.config["country_pool"] = ["Custom"]
            """
            Writing the custom mirror pool file
            """
            write_custom_mirrors_json(self=self, selected_mirrors=custom_pool)
            """
            Unless the user has provided the --no-status argument we only 
            write mirrors which are up-to-date for users selected branch
            """
            if self.no_status:
                pass
            else:
                mirror_list = filter_user_branch(mirror_pool=mirror_list, config=self.config)
            """
            Writing mirrorlist
            If the mirror list is empty because 
            no up-to-date mirrors exist for users branch
            raise IndexError to the outer try-catch
            """
            try:
                _ = mirror_list[0]
                write_pacman_mirror_list(self, mirror_list)
                if self.no_status:
                    util.msg(message=f"{txt.OVERRIDE_STATUS_CHOICE}", urgency=txt.WRN_CLR, tty=self.tty)
                    util.msg(message=f"{txt.OVERRIDE_STATUS_MIRROR}", urgency=txt.WRN_CLR, tty=self.tty)
            except IndexError:
                raise IndexError
        except IndexError:
            util.msg(message=f"{txt.NO_SELECTION}", urgency=txt.WRN_CLR, tty=self.tty)
            util.msg(message=f"{txt.NO_CHANGE}", urgency=txt.INF_CLR, tty=self.tty)

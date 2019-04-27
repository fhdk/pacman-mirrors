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

"""Pacman-Mirrors Common Mirror List Builder Module"""

from operator import itemgetter
from random import shuffle

from pacman_mirrors.functions.filter_mirror_status_functions import \
    filter_error_mirrors, filter_poor_mirrors, filter_bad_mirrors

from pacman_mirrors.constants import txt

from pacman_mirrors.functions.filter_mirror_pool_functions import \
    filter_user_branch, filter_mirror_protocols, filter_mirror_country

from pacman_mirrors.functions.outputFn import \
    write_pacman_mirror_list, write_custom_mirrors_json

from pacman_mirrors.functions.sortMirrorFn import sort_mirror_pool
from pacman_mirrors.functions.testMirrorFn import test_mirror_pool
from pacman_mirrors.functions import util


def build_mirror_list(self) -> None:
    """
    Generate common mirrorlist
    """
    """
    Apply country filter
    """
    mirror_selection = filter_mirror_country(mirror_pool=self.mirrors.mirror_pool, country_pool=self.selected_countries)
    """
    Apply bad mirror filter - mirrors where status.json has -1 for last_sync 9999:99
    """
    mirror_selection = filter_bad_mirrors(mirror_pool=mirror_selection)
    """
    Apply bad error filter- mirrors having a response time of 99.99 
    """
    mirror_selection = filter_error_mirrors(mirror_pool=mirror_selection)
    """
    Check the length of selected_countries against the full countrylist
    If selected_countries is the lesser then we build a custom pool file
    """
    if len(self.selected_countries) < len(self.mirrors.country_pool):
        try:
            _ = self.selected_countries[0]
            write_custom_mirrors_json(self=self, selected_mirrors=mirror_selection)
        except IndexError:
            pass
    """
    Prototol filtering if applicable
    """
    try:
        _ = self.config["protocols"][0]
        mirror_selection = filter_mirror_protocols(mirror_pool=mirror_selection, protocols=self.config["protocols"])
    except IndexError:
        pass
    """
    Unless the user has provided the --no-status argument we only 
    write mirrors which are up-to-date for users selected branch
    """
    if self.no_status:
        """
        Apply interval filter
        """
        if self.interval:
            mirror_selection = filter_poor_mirrors(mirror_pool=mirror_selection, interval=self.interval)
    else:
        mirror_selection = filter_user_branch(mirror_pool=mirror_selection, config=self.config)

    if self.config["method"] == "rank":
        mirror_selection = test_mirror_pool(self=self, worklist=mirror_selection)
        mirror_selection = sort_mirror_pool(worklist=mirror_selection, field="resp_time", reverse=False)
    else:
        shuffle(mirror_selection)

    mirror_selection = filter_error_mirrors(mirror_pool=mirror_selection)

    """
    Try to write mirrorlist
    """
    try:
        _ = mirror_selection[0]
        write_pacman_mirror_list(self=self, selected_servers=mirror_selection)
        if self.custom:
            util.msg(message=f"{txt.MIRROR_LIST_CUSTOM_RESET} 'sudo {txt.MODIFY_CUSTOM}'",
                     urgency=txt.INF_CLR, tty=self.tty)
            util.msg(message=f"{txt.REMOVE_CUSTOM_CONFIG} 'sudo {txt.RESET_ALL}'", urgency=txt.INF_CLR, tty=self.tty)
        if self.no_status:
            util.msg(message=f"{txt.OVERRIDE_STATUS_CHOICE}", urgency=txt.WRN_CLR, tty=self.tty)
            util.msg(message=f"{txt.OVERRIDE_STATUS_MIRROR}", urgency=txt.WRN_CLR, tty=self.tty)
    except IndexError:
        util.msg(message=f"{txt.NO_SELECTION}", urgency=txt.WRN_CLR, tty=self.tty)
        util.msg(message=f"{txt.NO_CHANGE}", urgency=txt.INF_CLR, tty=self.tty)

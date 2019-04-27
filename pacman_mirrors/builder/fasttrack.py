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

"""Pacman-Mirrors Interactive Fasttrack Mirror List Builder Module"""

from random import shuffle

from pacman_mirrors.builder.pool_builder import build_pool
from pacman_mirrors.constants import txt

from pacman_mirrors.functions.filter_mirror_pool_functions import \
    filter_user_branch

from pacman_mirrors.functions.outputFn import write_pacman_mirror_list
from pacman_mirrors.functions.testMirrorFn import test_mirror_pool
from pacman_mirrors.functions import util
from pacman_mirrors.functions.sortMirrorFn import sort_mirror_pool


def build_mirror_list(self, limit: int) -> None:
    """
    Fast-track the mirrorlist by filtering only up-to-date mirrors
    The function takes into account the branch selected by the user
      either on commandline or in pacman-mirrors.conf.
    The function returns a filtered list consisting of a number of mirrors
    Only mirrors from the active mirror file is used
      either mirrors.json or custom-mirrors.json
    """

    work_pool = build_pool(self)

    """
    Only pick mirrors which are up-to-date for the system branch
    by removing not up-to-date mirrors from the list
    """
    up_to_date_mirrors = filter_user_branch(mirror_pool=work_pool, config=self.config)

    """
    Shuffle the list
    """
    shuffle(up_to_date_mirrors)

    """
    # probe the mirrors
    """
    work_pool = test_mirror_pool(self=self, worklist=up_to_date_mirrors, limit=limit)

    """
    # sort the result
    """
    work_pool = sort_mirror_pool(worklist=work_pool, field="resp_time", reverse=False)

    """
    Write mirrorlist
    """
    try:
        _ = work_pool[0]
        write_pacman_mirror_list(self=self, selected_servers=work_pool)
    except IndexError:
        util.msg(message=f"{txt.NO_SELECTION}", urgency=txt.WRN_CLR, tty=self.tty)
        util.msg(message=f"{txt.NO_CHANGE}", urgency=txt.INF_CLR, tty=self.tty)



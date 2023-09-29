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

from pacman_mirrors.builder.builder import build_pool
from pacman_mirrors.constants import txt

from pacman_mirrors.functions.conversion import interactive_to_pool, pool_to_interactive

from pacman_mirrors.functions.filter_mirror_pool_functions import \
    filter_user_branch

from pacman_mirrors.functions.outputFn import \
    write_custom_mirrors_json, write_pacman_mirror_list

from pacman_mirrors.functions.sortMirrorFn import sort_mirror_pool
from pacman_mirrors.functions.testMirrorFn import test_mirror_pool
from pacman_mirrors.functions import util
from pacman_mirrors.dialogs import cutie


def build_mirror_list(self) -> None:
    """
    Prompt the user to select the mirrors with an interface.
    Outputs a "custom" mirror file
    Outputs a pacman mirrorlist,
    """
    worklist = build_pool(self)

    # rank or shuffle the mirrorlist before showing the ui
    if not self.default:
        # if not default run method before selection
        if self.config["method"] == "rank":
            worklist = test_mirror_pool(self=self, worklist=worklist)
            worklist = sort_mirror_pool(worklist=worklist, field="resp_time", reverse=False)
        else:
            shuffle(worklist)


    # process user choices
    # if interactive.is_done:

    available = []
    for m in worklist:
        for p in m["protocols"]:
            available.append(f'{p}://{m["url"]}')

    result = cutie.select_multiple(available)

    mirror_list = [select for idx, select in enumerate(available) if idx in result]

    custom_pool = [select for idx, select in enumerate(worklist) if idx in result]
    if mirror_list:
        print(f"mirrorlist {len(mirror_list)}/{len(available)}\nselection:", mirror_list)
        print(f"custompool {len(custom_pool)}/{len(custom_pool)}\nselection:", custom_pool)

    # translate interactive list back
    # custom_pool, mirror_list = interactive_to_pool(selection=custom_list,
    #                                                mirror_pool=self.mirrors.mirror_pool,
    #                                                tty=self.tty)

    # """
    # Try selected method on the mirrorlist
    # """
    # try:
    #     _ = mirror_list[0]
    #     # using the default runs method after selection
    #     if self.default:
    #         if self.config["method"] == "rank":
    #             mirror_list = test_mirror_pool(self=self, worklist=mirror_list)
    #             mirror_list = sorted(mirror_list, key=itemgetter("resp_time"))
    #         else:
    #             shuffle(mirror_list)
    # except IndexError:
    #     pass
    #
    # """
    # Write custom mirror pool
    # Write mirrorlist
    # """
    # try:
    #     _ = custom_pool[0]
    #     self.custom = True
    #     self.config["country_pool"] = ["Custom"]
    #
    #     """
    #     Writing the custom mirror pool file
    #     """
    #     write_custom_mirrors_json(self=self, selected_mirrors=custom_pool)
    #
    #     """
    #     Writing mirrorlist
    #     If the mirror list is empty because
    #     no up-to-date mirrors exist for users branch
    #     raise IndexError to the outer try-catch
    #     """
    #     try:
    #         _ = mirror_list[0]
    #         write_pacman_mirror_list(self, mirror_list)
    #         # # removed - part of refactor for new mirror-manager
    #         # if self.no_status:
    #         #     util.msg(message=f"{txt.OVERRIDE_STATUS_CHOICE}", urgency=txt.WRN_CLR, tty=self.tty)
    #         #     util.msg(message=f"{txt.OVERRIDE_STATUS_MIRROR}", urgency=txt.WRN_CLR, tty=self.tty)
    #     except IndexError:
    #         raise IndexError
    # except IndexError:
    #     util.msg(message=f"{txt.NO_SELECTION}", urgency=txt.WRN_CLR, tty=self.tty)
    #     util.msg(message=f"{txt.NO_CHANGE}", urgency=txt.INF_CLR, tty=self.tty)

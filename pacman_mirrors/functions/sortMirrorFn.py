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

"""Pacman-Mirrors Sort Mirros Functions"""
from operator import itemgetter


def sort_mirror_pool(worklist: list, field: str = "speed", reverse: bool = False) -> list:
    """
    Sort the mirror pool
    :param worklist: list to be sorted
    :param field: field to sort on
    :param reverse: direction
    :return: new list sorted by field
    """
    result = sorted(worklist, key=itemgetter(field), reverse=reverse)
    # print(f"{result[0]}")
    # for x in result:
    #     print(f"resp_time => {x['resp_time']}")
    # exit()
    return result

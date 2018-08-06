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

"""Pacman-Mirrors Converter Functions"""

from pacman_mirrors.constants import txt
from pacman_mirrors.functions import util


def translate_interactive_to_pool(custom_mirrors, mirror_pool, config):
    """
    Translate the interactive selection back to mirror pool
    :param custom_mirrors: the custom mirror selection
    :param mirror_pool: the default mirror pool
    :param config: the active pacman-mirrors configuration
    :return: custom mirror pool and mirrors for mirror list generation
    """
    custom_mirror_pool = []
    mirror_list = []

    for mirror in mirror_pool:
        try:
            _ = mirror_pool[0]
            mirror_url = util.get_server_location_from_url(mirror["url"])
            for custom_mirror in custom_mirrors:
                custom_mirror["resp_time"] = float(custom_mirror["resp_time"])
                try:
                    custom_url = util.get_server_location_from_url(custom_mirror["url"])
                    custom_protocol = util.get_protocol_from_url(custom_mirror["url"])

                    if custom_url == mirror_url:
                        pool_mirror = {
                            "country": mirror["country"],
                            "protocols": mirror["protocols"],
                            "url": mirror["url"],
                        }

                        custom_mirror_pool.append(pool_mirror)
                        custom_mirror["branches"] = mirror["branches"]
                        custom_mirror["protocols"] = [custom_protocol]

                        for m in mirror_list:
                            if m["url"].endswith(custom_url):
                                m["protocols"].append(custom_protocol)

                        if custom_mirror not in mirror_list:
                            mirror_list.append(custom_mirror)

                except KeyError:
                    print(".: {} {}! {}!".format(txt.WRN_CLR, txt.HOUSTON, txt.CUSTOM_POOL_EMPTY))
                    break

        except (KeyError, IndexError):
            print(".: {} {}! {}!".format(txt.WRN_CLR, txt.HOUSTON, txt.DEFAULT_POOL_EMPTY))
            break

    return custom_mirror_pool, mirror_list


def translate_pool_to_interactive(mirror_pool):
    """
    Translate mirror pool for interactive display
    :param mirror_pool:
    :return: list of dictionaries
            {
                "country": "country_name",
                "resp_time": "m.sss",
                "last_sync": "HHh MMm",
                "url": "http://server/repo/"
            }
    """
    interactive_list = []
    for mirror in mirror_pool:
        try:
            _ = mirror_pool[0]
            last_sync = str(mirror["last_sync"]).split(":")
            mirror_url = util.get_server_location_from_url(mirror["url"])
            for idx, protocol in enumerate(mirror["protocols"]):
                interactive_list.append({
                    "country": mirror["country"],
                    "resp_time": str(mirror["resp_time"]),
                    "last_sync": "{}h {}m".format(last_sync[0], last_sync[1]),
                    "url": "{}{}".format(protocol, mirror_url)
                })
        except (KeyError, IndexError):
            print(".: {} {}! {}!".format(txt.WRN_CLR, txt.HOUSTON, txt.MIRROR_POOL_EMPTY))
            break
    return interactive_list



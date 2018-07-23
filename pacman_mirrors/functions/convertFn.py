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


def translate_interactive_to_pool(custom_selection, mirror_pool, config):
    """
    Translate the interactive selection back to mirror pool
    :param custom_selection: the custom selection
    :param mirror_pool: the default mirror pool
    :param config: the active pacman-mirrors configuration
    :return: custom mirror pool and mirrors for mirror list generation
    """
    # return lists
    custom_mirror_pool = []
    mirror_list = []

    for mirror in mirror_pool:
        try:
            _ = mirror_pool[0]
            mirror_url = util.get_server_location_from_url(mirror["url"])
            for current in custom_selection:
                try:
                    """
                    url without protocol
                    """
                    url = util.get_server_location_from_url(current["url"])
                    """
                    protocol without url
                    """
                    protocol = util.get_protocol_from_url(current["url"])
                    if url == mirror_url:
                        """
                        Create working copy
                        """
                        work_mirror = {
                            "country": mirror["country"],
                            "branches": mirror["branches"],
                            "protocols": [],
                            "resp_time": mirror["resp_time"],
                            "last_sync": mirror["last_sync"],
                            "url": mirror["url"]
                        }
                        """
                        Append to custom mirror pool
                        """
                        custom_mirror_pool.append({
                            "country": mirror["country"],
                            "protocols": mirror["protocols"],
                            "url": mirror["url"]
                        })
                        try:
                            """
                            If a user selection of protocols exist in configuration
                            Replace the mirrors protocols with selection
                            """
                            _ = config["protocols"][0]
                            work_mirror["protocols"] = config["protocols"]
                        except IndexError:
                            pass

                        for idx, proto in enumerate(mirror["protocols"]):
                            """
                            Generate a mirror by adding selected protocol to the server
                            Avoid duplicating the protocols by keepin an internal set of protocols
                            The custom_protocols set is used for that purpose
                            """
                            if proto == protocol:
                                work_mirror["protocols"].append(proto)

                        """
                        Add to the mirrorlist
                        """
                        mirror_list.append(work_mirror)

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
                    "resp_time": mirror["resp_time"],
                    "last_sync": "{}h {}m".format(last_sync[0], last_sync[1]),
                    "url": "{}{}".format(protocol, mirror_url)
                })
        except (KeyError, IndexError):
            print(".: {} {}! {}!".format(txt.WRN_CLR, txt.HOUSTON, txt.MIRROR_POOL_EMPTY))
            break
    return interactive_list



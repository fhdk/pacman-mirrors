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


"""Pacman-Mirrors Mirror Class Module"""

from pacman_mirrors.constants import txt
from pacman_mirrors.functions.pools import get_continent
from decimal import Decimal


class Mirror:
    """Mirror Class"""

    def __init__(self):
        self.country_pool = []
        self.mirror_pool = []

    def add(self, alias: str, url: str, protocols: list, branches: list,
            resp_time: str, last_sync: str, score: int) -> None:
        """Append mirror
        :param alias:
        :param url:
        :param protocols:
        :param branches:
        :param resp_time:
        :param last_sync:
        :param score:
        """
        if branches is None:
            branches = [-1, -1, -1]
        # if last_sync is None:
        #     last_sync = "00:00"
        if resp_time is None:
            resp_time = 0
        else:
            resp_time = resp_time
        # translate negative integer in status.json
        # if last_sync == -1:
        #     last_sync = txt.SERVER_BAD  # "9999:99"
        #     resp_time = txt.SERVER_RES  # 99.99
        # sort protocols in reversed order https,http,ftps,ftp
        protocols = sorted(protocols, reverse=True)
        # fetch the correct naming for country
        # work around the data file is all lower case
        continent, country = get_continent(alias.replace("_", " "))
        if not country:
            country = "Global CDN"
        if country not in self.country_pool:
            self.country_pool.append(country)
        internal = {
            "continent": continent,
            "branches": branches,
            "country": country,
            "last_sync": last_sync,
            "protocols": protocols,
            "resp_time": resp_time,
            "score": score,
            "speed": resp_time,
            "url": url,
            "url2": f"{protocols[0]}://{url}",
        }
        self.mirror_pool.extend([internal])

    def seed(self, servers: list, arm: bool, custom: bool = False) -> None:
        """
        Seed mirrorlist
        :param servers:
        :param custom:
        :param arm:
        """
        if custom:  # clear previous data
            self.country_pool = []
            self.mirror_pool = []
        for server in servers:
            # new layout has all branches in branhes
            # take only branches matching architecture
            # assume x86_64
            branches = server["branches"][:3]
            if arm:
                # take last three instead
                branches = server["branches"][-3]
            # add server to list
            self.add(server["country"], server["url"], server["protocols"], branches,
                     server["speed"], server["last_sync"], server["score"])

    @staticmethod
    def copy_to_extern(server: dict) -> dict:
        return {
            "country": str(server["country"]).replace(" ", "_").lower(),
            "branches": server["branches"],
            "last_sync": server["last_sync"],
            "protocols": server["protocols"],
            "score": server["score"],
            "speed": server["resp_time"],
            "url": server["url"],
        }

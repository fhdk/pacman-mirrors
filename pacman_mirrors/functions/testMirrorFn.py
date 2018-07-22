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

"""Pacman-Mirrors Test Mirror Functions"""

import sys

from pacman_mirrors.constants import txt, colors as color
from pacman_mirrors.functions import httpFn
from pacman_mirrors.functions import util


def test_mirrors(self, worklist):
    """
    Query server for response time
    """
    if self.custom:
        print(".: {} {}".format(txt.INF_CLR,
                                txt.USING_CUSTOM_FILE))
    else:
        print(".: {} {}".format(txt.INF_CLR,
                                txt.USING_DEFAULT_FILE))
    print(".: {} {} - {}".format(txt.INF_CLR,
                                 txt.QUERY_MIRRORS,
                                 txt.TAKES_TIME))
    cols, lines = util.terminal_size()
    # set connection timeouts
    http_wait = self.max_wait_time
    ssl_wait = self.max_wait_time * 2
    ssl_verify = self.config["ssl_verify"]
    result = []
    for mirror in worklist:
        work_mirror = mirror_protocols(mirror)
        colon = work_mirror[0]["url"].find(":")
        url = work_mirror[0]["url"][colon:]
        for mirror_proto in work_mirror:
            proto = mirror_proto["protocols"][0]
            mirror_proto["url"] = "{}{}".format(proto, url)
            if not self.quiet:
                message = "   ..... {:<15}: {}".format(mirror_proto["country"],
                                                       mirror_proto["url"])
                print("{:.{}}".format(message, cols), end="")
                sys.stdout.flush()
            # https/ftps sometimes takes longer for handshake
            if proto.endswith("tps"):  # https or ftps
                self.max_wait_time = ssl_wait
            else:
                self.max_wait_time = http_wait
            # let's see how responsive you are
            mirror_proto["resp_time"] = httpFn.get_mirror_response(mirror_proto["url"],
                                                                   maxwait=self.max_wait_time,
                                                                   quiet=self.quiet,
                                                                   ssl_verify=ssl_verify)

            if float(mirror_proto["resp_time"]) >= self.max_wait_time:
                if not self.quiet:
                    print("\r")
            else:
                if not self.quiet:
                    print("\r   {:<5}{}{} ".format(color.GREEN,
                                                   mirror_proto["resp_time"],
                                                   color.ENDCOLOR))
        mirror = filter_bad_ssl(work_mirror)
        result.append(mirror)

    return result


def mirror_protocols(mirror):
    """
    Return a number of copies of mirror - one copy per protocol
    :param: mirror dictionary with a number of protocols
    :return: dictionaries as a copy of the mirror for probing - one per protocol
    """
    result = []
    for idx, protocol in enumerate(mirror["protocols"]):
        m = {
                "branches": mirror["branches"],
                "country": mirror["country"],
                "last_sync": mirror["last_sync"],
                "protocols": [protocol],
                "resp_time": mirror["resp_time"],
                "url": mirror["url"],
            }
        result.append(m)
    return result


def filter_bad_ssl(work):
    """
    filter bad ssl if mirror has more than one protocol
    :param work:
    :return: mirror
    """
    result = {
        "branches": work[0]["branches"],
        "country": work[0]["country"],
        "last_sync": work[0]["last_sync"],
        "protocols": [],
        "resp_time": "",
        "url": work[0]["url"]
    }
    if len(work) > 1:
        for item in work:
            if item["protocols"][0].endswith("tps") and item["resp_time"] == txt.SERVER_RES:
                continue
            try:
                result["protocols"].append(item["protocols"][0])
                result["resp_time"] = item["resp_time"]
            except IndexError:
                continue
    return result

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
import time
from operator import itemgetter
from pacman_mirrors.constants import txt, colors as color
from pacman_mirrors.functions.httpFn import get_mirror_response
from pacman_mirrors.functions import util


def test_mirror_pool(self, worklist: list, limit=None) -> list:
    """
    Query server for response time
    """
    if self.custom:
        util.msg(message=f"{txt.USING_CUSTOM_FILE}",
                 urgency=f"{txt.INF_CLR}",
                 tty=self.tty)
    else:
        util.msg(message=f"{txt.USING_DEFAULT_FILE}",
                 urgency=f"{txt.INF_CLR}",
                 tty=self.tty)
    util.msg(message=f"{txt.QUERY_MIRRORS} - {txt.TAKES_TIME}",
             urgency=f"{txt.INF_CLR}",
             tty=self.tty)
    counter = 0
    cols, lines = util.terminal_size()
    # set connection timeouts
    http_wait = self.max_wait_time
    ssl_wait = self.max_wait_time * 2
    ssl_verify = self.config["ssl_verify"]
    result = []

    for mirror in worklist:
        # get a list of mirror dictionaries ordered by protocol descending
        # mirror_protocols is monkey patched to return only the first
        work_mirror = mirror_protocols(mirror)
        # get protocol
        proto = work_mirror["protocols"][0]
        # generate url with protocol
        test_url = f"{proto}://{work_mirror['url']}"

        # create message for later display
        message = f'  ..... {work_mirror["country"]:<15}: {test_url}'

        # if self.tty do not print this
        if not self.quiet:
            if self.tty:
                pass
            else:
                print("{:.{}}".format(message, cols), end="")
                sys.stdout.flush()

        # https/ftps sometimes takes longer for handshake
        if proto.endswith("tps"):  # https or ftps
            self.max_wait_time = ssl_wait
        else:
            self.max_wait_time = http_wait

        # let's see how responsive you are
        work_mirror["speed"] = get_mirror_response(url=test_url, config=self.config, tty=self.tty,
                                                   maxwait=self.max_wait_time, quiet=self.quiet,
                                                   ssl_verify=ssl_verify)

        # create a printable string version from the response with appended zeroes
        r_str = str(work_mirror["speed"])
        while len(r_str) < 5:
            r_str += "0"

        # validate against the defined wait time
        if work_mirror["speed"] >= self.max_wait_time:
            # skip line - but not if tty
            if not self.quiet:
                if self.tty:
                    pass
                else:
                    print("\r")
        else:
            # only print if not tty
            if not self.quiet:
                if self.tty:
                    pass
                else:
                    print(f"\r  {color.GREEN}{r_str}{color.RESET}")

        # we have tty then we print with response time
        if self.tty:
            util.msg(message=message.replace(".....", r_str), tty=self.tty)
            sys.stdout.flush()

        work_mirror["url"] = test_url

        if limit is not None:
            if mirror["speed"] == txt.SERVER_RES:
                continue
            counter += 1
            result.append(work_mirror)
        else:
            result.append(work_mirror)
        """
        Equality check will stop execution
        when the desired number is reached.
        In the possible event the first mirror's
        response time exceeds the predefined response time,
        the loop would stop execution if the check for zero is not present
        """
        if limit is not None and counter != 0 and counter == limit:
            break

    return result


def mirror_protocols(mirror: dict) -> dict:
    """
    Return a number of copies of mirror - one copy per protocol
    :param: mirror dictionary with a number of protocols
    :return: mirror
    """
    result = []
    for idx, protocol in enumerate(mirror["protocols"]):
        m = {
            "branches": mirror["branches"],
            "country": mirror["country"],
            "protocols": [protocol],
            "speed": mirror["speed"],
            "url": mirror["url"],
        }
        result.append(m)
    # -------------------------------------------------
    # monkey patch - sort by protocol desc
    # return the first to avoid testing all protocols for one mirror
    result = sorted(result, key=itemgetter("protocols"), reverse=True)
    return result[0]


def filter_bad_http(work: list) -> dict:
    """
    filter bad http/ssl if mirror has more than one protocol
    :param work: list of mirror dictionaries with one protocol per dictionary
    :return: mirror dictionary with invalid ssl removed
    """
    result = {
        "branches": work[0]["branches"],
        "country": work[0]["country"],
        "protocols": [],
        "speed": "",
        "url": work[0]["url"]
    }
    if len(work) > 1:
        for item in work:
            if (item["protocols"][0].endswith("tps")
                    and item["speed"] == txt.SERVER_RES or
                    sum(item["branch"] == 0)):
                continue
            result["protocols"].append(item["protocols"][0])
            result["speed"] = item["speed"]
        return result
    return work[0]

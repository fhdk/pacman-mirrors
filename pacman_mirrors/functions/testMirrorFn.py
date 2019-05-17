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
from concurrent.futures import ThreadPoolExecutor, as_completed

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
    # I don't know how to properly fix this yet
    # counter = 0
    cols, lines = util.terminal_size()
    # set connection timeouts
    # http_wait = self.max_wait_time
    # ssl_wait  = self.max_wait_time * 2
    # ssl_verify = self.config["ssl_verify"]
    result = []
    # Create the threadpool and submit a tasks per mirror
    with ThreadPoolExecutor(max_workers=50) as executor:
        mirrors_future = {executor.submit(mirror_fn,
                                          self,
                                          executor,
                                          mirror,
                                          limit,
                                          cols):
                          mirror for mirror in worklist}
        # Get results as they resolve
        for mirror in as_completed(mirrors_future):
            mirror_result = mirror.result()
            if mirror_result is not None:
                result.append(mirror_result)

    return result


def mirror_fn(self, executor, mirror: dict, limit, cols) -> dict:
    """
    This function will be scheduled for every mirror to
    run asynchronously. Yielding the mirrors as all the petitions
    to its supported protocols resolve
    :param executor: The executor to be used to resolve the IO petitions
    :param mirror: The mirror to be queried
    """
    # create a list for the mirrors available protocols
    probe_items = list_with_protocols(mirror)
    # locate position of protocols separator
    colon = probe_items[0]["url"].find(":")
    # create an url for the mirror without protocol
    url = probe_items[0]["url"][colon:]
    probed_items = []
    # Loop protocols available and schedule function
    protocols_future = {executor.submit(protocol_fn,
                                        self,
                                        executor,
                                        protocol,
                                        url,
                                        cols):
                        protocol for protocol in probe_items}
    for protocol_result in as_completed(protocols_future):
        probed_items.append(protocol_result.result())

    # check the protocols
    probed_mirror = filter_bad_response(work=probe_items)

    if limit is not None:
        if mirror["resp_time"] == txt.SERVER_RES:
            return None
        # counter += 1
        mirror["result"] = probed_mirror
    else:
        mirror["result"] = probed_mirror
    """
    Equality check will stop execution
    when the desired number is reached.
    In the possible event the first mirror's
    response time exceeds the predefined response time,
    the loop would stop execution if the check for zero is not present
    """
    # if limit is not None and counter is not 0 and counter == limit:
    #     return

    return mirror


def protocol_fn(self, executor, protocol, url, cols):
    """
    This function will be scheduled to run
    for every protocol in a mirror.
    """
    # get protocol
    probe_proto = protocol["protocols"][0]

    # generate url with protocol
    protocol["url"] = f"{probe_proto}{url}"

    http_wait = self.max_wait_time
    ssl_wait = self.max_wait_time * 2
    ssl_verify = self.config["ssl_verify"]

    # https/ftps sometimes takes longer for handshake
    if probe_proto.endswith("tps"):  # https or ftps
        self.max_wait_time = ssl_wait
    else:
        self.max_wait_time = http_wait

    # let's see see time spent
    protocol["resp_time"] = get_mirror_response(url=protocol["url"],
                                                config=self.config,
                                                tty=self.tty,
                                                maxwait=self.max_wait_time,
                                                quiet=self.quiet,
                                                ssl_verify=ssl_verify)

    # create a printable string version from the response with appended zeroes
    r_str = str(protocol["resp_time"])
    while len(r_str) < 5:
        r_str += "0"

    # validate against the defined wait time
    if protocol["resp_time"] >= self.max_wait_time:
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
                print(f"\r  {color.GREEN}{r_str}{color.RESET} - {protocol['url']}")

    # we have tty then we print with response time
    if self.tty:
        util.msg(message=message.replace(".....", r_str), tty=self.tty)
        sys.stdout.flush()


def list_with_protocols(mirror: dict) -> list:
    """
    Return a number of copies of mirror - one copy per protocol
    :param: mirror dictionary with a number of protocols
    :return: list of mirror dictionaries with one protocol per dictionary
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


def filter_bad_response(work: list) -> dict:
    """
    filter bad http/ssl if mirror has more than one protocol
    :param work: list of mirror dictionaries with one protocol per dictionary
    :return: mirror dictionary with invalid protocols removed
    """
    result = {
        "branches": work[0]["branches"],
        "country": work[0]["country"],
        "last_sync": work[0]["last_sync"],
        "protocols": [],
        "resp_time": 99.99,
        "url": work[0]["url"]
    }
    for item in work:
        if item["resp_time"] == txt.SERVER_RES:
            continue
        result["protocols"].append(item["protocols"][0])
        if item["resp_time"] < result["resp_time"]:
            result["resp_time"] = item["resp_time"]
    return result

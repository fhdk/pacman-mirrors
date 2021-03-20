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

"""Manjaro-Mirrors HTTP Functions"""

import collections
import filecmp
import json
import os
import ssl
import time
from os import system as system_call
import socket
from socket import timeout

# import urllib.request
# import urllib.parse
# from urllib.error import URLError
from http.client import HTTPException
import requests

from pacman_mirrors import __version__
from pacman_mirrors.config import configuration as conf
from pacman_mirrors.constants import timezones
from pacman_mirrors.constants import txt
from pacman_mirrors.functions import fileFn
from pacman_mirrors.functions import jsonFn
from pacman_mirrors.functions import util

USER_AGENT = {"User-Agent": "{}{}".format(conf.USER_AGENT, __version__)}


def download_mirrors(config: object) -> tuple:
    """Retrieve mirrors from manjaro.org
    :param config:
    :returns: tuple with bool for mirrors.json and status.json
    :rtype: tuple
    """
    fetchmirrors = False
    fetchstatus = False
    try:
        # mirrors.json
        resp = requests.get(url=config["url_mirrors_json"],
                            headers=USER_AGENT,
                            timeout=config["timeout"])
        resp.raise_for_status()
        mirrorlist = resp.json()
        fetchmirrors = True
        tempfile = config["work_dir"] + "/.temp.file"
        jsonFn.json_dump_file(mirrorlist, tempfile)
        filecmp.clear_cache()
        if fileFn.check_file(conf.USR_DIR, folder=True):
            if not fileFn.check_file(config["mirror_file"]):
                jsonFn.json_dump_file(mirrorlist, config["mirror_file"])
            elif not filecmp.cmp(tempfile, config["mirror_file"]):
                jsonFn.json_dump_file(mirrorlist, config["mirror_file"])
        os.remove(tempfile)
    except (json.JSONDecodeError,):
        pass
    try:
        # status.json
        resp = requests.get(url=config["url_status_json"],
                            headers=USER_AGENT,
                            timeout=config["timeout"])
        statuslist = resp.json()
        fetchstatus = True
        jsonFn.write_json_file(statuslist, config["status_file"])
    except (json.JSONDecodeError,):
        pass
    # result
    return fetchmirrors, fetchstatus


def get_ip_country(maxwait: int = 2) -> str:
    """
    Get the user country from connection IP (might be VPN who knows)
    :return: country name
    """
    # noinspection PyBroadException
    try:
        resp = requests.get("https://get.geojs.io/v1/ip/country/full",
                            timeout=maxwait)
        resp.raise_for_status()
        return resp.text
    finally:
        return ""


def get_mirror_response(url: str, config: object, tty: bool = False, maxwait: int = 2,
                        count: int = 1, quiet: bool = False, ssl_verify: bool = True) -> float:
    """Query mirror by downloading a file and measuring the time taken
    :param config:
    :param ssl_verify:
    :param tty:
    :param url:
    :param maxwait:
    :param count:
    :param quiet:
    :returns always return a float value with response time
    """
    response_time = txt.SERVER_RES  # prepare default return value
    probe_stop = None
    message = ""
    # context = ssl.create_default_context()
    arch = "x86_64"
    if config["arm"]:
        arch = "aarch64"
    probe_url = f"{url}{config['branch']}/core/{arch}/{config['test_file']}"
    if not ssl_verify:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
    probe_start = time.time()
    # noinspection PyBroadException
    try:
        for _ in range(count):
            resp = requests.get(url=probe_url, headers=USER_AGENT, timeout=maxwait)
            resp.raise_for_status()
            _ = resp.text
        probe_stop = time.time()
    except timeout:
        message = f"{txt.TIMEOUT} '{url}'"
    except ssl.CertificateError:
        message = f"{ssl.CertificateError} '{url}'"
    except Exception as e:
        message = f"{e}"

    if message and not quiet:
        util.msg(message=message, urgency=txt.ERR_CLR, tty=tty, newline=True)
    if probe_stop:
        response_time = round((probe_stop - probe_start), 3)
    return response_time


def check_internet_connection(tty: bool = False, maxwait: int = 2) -> bool:
    """Check for internet connection
    :param maxwait:
    :param tty:
    """
    resp = None
    hosts = conf.INET_CONN_CHECK_URLS
    for host in hosts:
        # noinspection PyBroadException
        try:
            resp = requests.get(host, timeout=maxwait)
            break
        except Exception as e:
            util.msg(f"{host} '{e}'", urgency=txt.WRN_CLR, tty=tty)
    return bool(resp)


def ping_host(host: str, tty: bool = False, count: int = 1) -> bool:
    """Check a hosts availability
    :param host:
    :param count:
    :param tty:
    :rtype: boolean
    """
    util.msg(f"ping {host} x {count}", urgency=txt.INF_CLR, tty=tty)
    return system_call("ping -c{} {} > /dev/null".format(count, host)) == 0


def download_mirror_pool(config: object, tty: bool = False, quiet: bool = False) -> tuple:
    """Download updates from repo.manjaro.org
    :param config:
    :param quiet:
    :param tty:
    :returns: tuple with True/False for mirrors.json and status.json
    :rtype: tuple
    """
    result = None
    connected = check_internet_connection(tty=tty)
    if connected:
        if not quiet:
            util.msg(message=f"{txt.DOWNLOADING_MIRROR_FILE} {txt.REPO_SERVER}",
                     urgency=txt.INF_CLR,
                     tty=tty)
        result = download_mirrors(config)
    else:
        if not fileFn.check_file(config["status_file"]):
            if not quiet:
                util.msg(message=f"{txt.MIRROR_FILE} {config['status_file']} {txt.IS_MISSING}",
                         urgency=txt.WRN_CLR,
                         tty=tty)
                util.msg(message=f"{txt.FALLING_BACK} {conf.MIRROR_FILE}",
                         urgency=txt.WRN_CLR,
                         tty=tty)
            result = (True, False)
        if not fileFn.check_file(config["mirror_file"]):
            if not quiet:
                util.msg(message=f"{txt.HOUSTON}",
                         urgency=txt.HOUSTON,
                         tty=tty)
            result = (False, False)
    return result

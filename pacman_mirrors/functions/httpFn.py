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

import filecmp
import json
import os
import ssl
import time
from os import system as system_call

import shutil
import urllib.request as request
from contextlib import closing
from urllib.error import URLError
import requests

from pacman_mirrors import __version__
from pacman_mirrors.config import configuration as conf
from pacman_mirrors.constants import txt
from pacman_mirrors.functions import fileFn
from pacman_mirrors.functions import jsonFn
from pacman_mirrors.functions import util

USER_AGENT = {"User-Agent": "{}{}".format(conf.USER_AGENT, __version__)}


def download_mirrors(config: dict) -> bool:
    """Retrieve mirrors from manjaro.org
    :param config:
    :returns: tuple with bool for mirrors.json and status.json
    :rtype: tuple
    """
    fetchmirrors = True
    message = ""
    try:
        # mirrors.json
        util.msg(message=f"=> Mirror pool: {config['url_mirrors_json']}", urgency=txt.INF_CLR)
        resp = requests.get(url=config["url_mirrors_json"],
                            headers=USER_AGENT,
                            timeout=config["timeout"])
        resp.raise_for_status()
        mirrorlist = resp.json()
        tempfile = config["work_dir"] + "/.temp.file"
        jsonFn.json_dump_file(mirrorlist, tempfile)
        filecmp.clear_cache()
        if fileFn.check_file(conf.WORK_DIR, folder=True):
            if not fileFn.check_file(config["mirror_file"]):
                jsonFn.json_dump_file(mirrorlist, config["mirror_file"])
            elif not filecmp.cmp(tempfile, config["mirror_file"]):
                jsonFn.json_dump_file(mirrorlist, config["mirror_file"])
        os.remove(tempfile)
    except (json.JSONDecodeError,) as jsonError:
        message = f"Invalid JSON data: {jsonError}"
    except (requests.exceptions.ConnectionError,) as connError:
        message = f"Connection: {connError}"
    except (requests.exceptions.SSLError,) as sslError:
        message = f"Certificate: {sslError}"
    except (requests.exceptions.Timeout,) as connTimeout:
        message = f"Connection: {connTimeout}"
    except (requests.exceptions.HTTPError,) as httpError:
        message = f"Connection {httpError}"
    except Exception as e:
        message = f"{e}"
    if message != "":
        fetchmirrors = False
        util.msg(message=message, urgency=txt.ERR_CLR, newline=True)
        message = ""

    # result
    return fetchmirrors


def get_ip_country(maxwait: int = 2) -> str:
    """
    Get the user country from connection IP (might be VPN who knows)
    :return: country name
    """
    try:
        resp = requests.get("https://get.geojs.io/v1/ip/country/full", timeout=maxwait)
        resp.raise_for_status()
    except requests.exceptions.ConnectionError:
        return ""
    return resp.text


def get_http_response(url: str, maxwait: int) -> str:
    """
    Used for http mirrors
    :return: bool
    """
    message = ""
    try:
        resp = requests.get(url=url, headers=USER_AGENT, timeout=maxwait)
        resp.raise_for_status()
        # _ = resp.text
    except (requests.exceptions.ConnectionError,) as connError:
        message = f"ERROR: {connError}"
    except (requests.exceptions.SSLError,) as sslError:
        message = f"ERROR: {sslError}"
    except (requests.exceptions.Timeout,) as connTimeout:
        message = f"ERROR: {connTimeout}"
    except (requests.exceptions.HTTPError,) as httpError:
        message = f"ERROR: {httpError}"
    except Exception as e:
        message = f"ERROR: {e}"

    return message


def get_ftp_response(url: str, maxwait: int) -> str:
    """
    Used for ftp response
    :return:
    """
    message = ""

    # noinspection PyBroadException
    try:
        with closing(request.urlopen(url, timeout=maxwait)) as ftpReq:
            with open(conf.WORK_DIR + '/.testresponse', 'wb') as testFile:
                shutil.copyfileobj(ftpReq, testFile)
            os.remove(conf.WORK_DIR + '/.testresponse')
    except URLError as e:
        if e.reason.find('No such file or directory') >= 0:
            message = f"ERROR: FileNotFound"
        else:
            message = f"ERROR: {e.reason}"
    except:
            message = "ERROR:"

    return message


def get_mirror_response(url: str, config: dict, tty: bool = False, maxwait: int = 2,
                        quiet: bool = False, ssl_verify: bool = True) -> float:
    """Query mirror by downloading a file and measuring the time taken
    :param config:
    :param ssl_verify:
    :param tty:
    :param url:
    :param maxwait:
    :param quiet:
    :returns: always return a float value with response time
    """
    response_time = txt.SERVER_RES  # prepare default return value
    probe_stop = None
    message = ""
    context = ssl.create_default_context()
    arch = "x86_64"
    if config["arm"]:
        arch = "aarch64"
    probe_url = f"{url}{config['branch']}/core/{arch}/{config['test_file']}"
    if not ssl_verify:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

    probe_start = time.time()
    if probe_url.startswith("http"):
        message = get_http_response(url=probe_url, maxwait=maxwait)
        probe_stop = time.time()
    if probe_url.startswith("ftp"):
        message = get_ftp_response(url=probe_url, maxwait=maxwait)
        probe_stop = time.time()

    if message.startswith("ERROR:") and not quiet:
        util.msg(message=f"{message}", urgency=txt.ERR_CLR, tty=tty, newline=True)

    if probe_stop and not message:
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

        except (requests.exceptions.ConnectionError,) as connError:
            message = f"Connection: {connError}"
        except (requests.exceptions.SSLError,) as sslError:
            message = f"Certificate: {sslError}"
        except (requests.exceptions.Timeout,) as connTimeout:
            message = f"Connection: {connTimeout}"
        except (requests.exceptions.HTTPError,) as httpError:
            message = f"Connection {httpError}"
        except Exception as e:
            message = f"{e}"

        util.msg(f"{host} '{message}'", urgency=txt.WRN_CLR, tty=tty)
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


def download_mirror_pool(config: dict, tty: bool = False, quiet: bool = False) -> bool:
    """Download updates from mirror-manager.manjaro.org
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
            util.msg(message=f"{txt.DOWNLOADING_MIRROR_FILE} Manjaro",
                     urgency=txt.INF_CLR,
                     tty=tty)
        result = download_mirrors(config)
    else:
        if not fileFn.check_file(config["mirror_file"]):
            if not quiet:
                util.msg(message=f"{txt.HOUSTON}",
                         urgency=txt.HOUSTON,
                         tty=tty)
            result = False
    return result

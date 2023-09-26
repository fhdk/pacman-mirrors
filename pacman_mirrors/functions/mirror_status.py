#!/usr/bin/env python

from urllib import request
from urllib import error
import json
from pacman_mirrors.constants import colors
from pacman_mirrors.functions import printFn
from pacman_mirrors.functions.util import strip_protocol
from pacman_mirrors.functions.util import msg
from datetime import datetime
from pacman_mirrors.functions.jsonFn import read_json_file

C_KO = colors.RED
C_OK = colors.GREEN
C_NONE = colors.RESET


def get_local_mirrors(mirror_list: str) -> tuple:
    urls = []
    try:
        with open(mirror_list, "r") as f_list:
            for line in f_list:
                if not line.startswith("Server"):
                    continue
                line = line.split("=")[1].strip()
                line = line.split("$")[0]
                mirror_url = line.split('/')
                mirror_url.pop()
                mirror_branch = mirror_url.pop()
                line = "/".join(mirror_url)
                urls.append(line + "/",)
        return mirror_branch, urls
    except (FileNotFoundError, UnboundLocalError):
        return "", []


def get_state(states: list, branch: str) -> tuple:
    ret_color = C_OK
    status_text = "OK"
    x = states[0]
    if branch == "testing":
        x = states[1]
    if branch == "unstable":
        x = states[2]
    if x == 0:
        ret_color = C_KO
        status_text = "--"
    if x == -1:
        ret_color = C_KO
        status_text = "--"
    return ret_color, status_text


def print_status(self) -> int:
    """
    Printe mirror status
    :param self:
    :return:
    """
    # // --- BEGING ---------------------------------------------------------------------
    # configuration is enterprise
    # - pacman-mirrors.conf
    # - Ent = http(s)://ent.mirror.tld:8080
    if self.config["enterprise"]:
        color = C_OK
        text = "OK"
        now = datetime.now()
        mirror = self.config["static"]
        print(f"Mirror #1", color, f"{text}", C_NONE, f"Enterprise {mirror['url']}")
        return 0
    # // --- END ---------------------------------------------------------------------

    system_branch, mirrors_pacman = get_local_mirrors(self.config["mirror_list"])
    # bug out when no local mirrorlist exist or branch is deprecated
    if system_branch == "" or system_branch == "stable-staging":
        print(C_KO, "MIRRORLIST ERROR", C_NONE)
        return 1

    try:
        with request.urlopen(self.config["url_mirrors_json"]) as f_url:
            req = f_url.read()
    except error.URLError:
        msg("Downloading mirror status failed!", color=colors.BLUE)
        msg("Please check you network connection ...", color=colors.YELLOW)
        return 1  # return failure
    json_data = json.loads(req)
    mirrors = []
    for mirror in json_data:
        for protocol in mirror["protocols"]:
            temp = mirror.copy()
            temp["url"] = f"{protocol}://{strip_protocol(temp['url'])}"
            mirrors.append(temp)

    mirrors = [m for m in mirrors if m['url'] in mirrors_pacman]

    printFn.yellow_msg(f"Local mirror status for {system_branch} branch")
    exit_code = 0  # up-to-date
    for i, url in enumerate(mirrors_pacman):  # same order as pacman-conf
        try:
            mirror = [m for m in mirrors if m['url'] == url][0]
            color, text = get_state(mirror["branches"], system_branch)
            len_country = max(len(m['country']) for m in mirrors) + 1
            print(f"Mirror #{str(i + 1):2}", color, f"{text}", C_NONE,
                  f"{mirror['country']:{len_country}} {mirror['url']}")
            if i == 0 and color == C_KO:
                exit_code = 4  # first mirror not sync !
        except IndexError:
            print(C_KO, f"Mirror #{i + 1:2}", f"{url} does not exist{C_NONE}")
            exit_code = 5  # not found

    return exit_code

#!/usr/bin/env python

from urllib import request
from urllib import error
import json
from pacman_mirrors.constants import colors
from pacman_mirrors.functions import printFn
from pacman_mirrors.functions.util import msg
from pacman_mirrors.functions.jsonFn import read_json_file
from pacman_mirrors.functions.defaultFn import mirror_seed_from_data

C_KO = colors.RED
C_OK = colors.GREEN
C_NONE = colors.RESET


def get_local_mirrors(mirrorlist: str) -> tuple:
    urls = []
    try:
        with open(mirrorlist, "r") as f_list:
            for line in f_list:
                if not line.startswith("Server"):
                    continue
                line = line.split("=")[1].strip()
                line = line.split("$")[0]
                mirror_url = line.split('/')
                mirror_url.pop()
                mirror_branch = mirror_url.pop()
                # line = "/".join(mirror_url)
                line = f"{mirror_url[2]}/{mirror_url[3]}/"
                urls.append(line)
        print(mirror_branch, mirror_url)
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
    if self.config["enterprise"]:
        # write enterprise config
        color = C_OK
        text = "OK"
        fake = "00:00"
        print(f"Mirror #1", color, f"{text}", C_NONE, f"{fake} Enterprise {self.config['static']}")
        return 0
    # // --- END ---------------------------------------------------------------------

    system_branch, mirrors_pacman = get_local_mirrors(self.config["mirror_list"])
    # bug out when no local mirrorlist exist or branch is deprecated
    if system_branch == "" or system_branch == "stable-staging":
        print(C_KO, "MIRRORLIST ERROR", C_NONE)
        return 1

    try:
        # // --- DEBUG ---------------------------------------------------------------
        # with request.urlopen('http://localhost:8000/status.json') as f_url:
        with request.urlopen(self.config["mirror_manager"]) as f_url:
            req = f_url.read()
    except error.URLError:
        msg("Downloading status failed!", color=colors.BLUE)
        msg("Please check you network connection ...", color=colors.YELLOW)
        return 1  # return failure
    json_data = json.loads(req)
    data = mirror_seed_from_data(self, json_data)
    mirrors = []

    for mirror in data:
        for protocol in mirror["protocols"]:
            temp = mirror.copy()
            temp["url"] = temp['url']
            mirrors.append(temp)

    mirrors = [m for m in mirrors if m['url'] in mirrors_pacman]

    printFn.yellow_msg(f"Local mirror status for {system_branch} branch")
    exit_code = 0  # up-to-date
    for i, url in enumerate(mirrors_pacman):  # same order as pacman-conf
        try:
            mirror = [m for m in mirrors if m['url'] == url][0]
            color, text = get_state(mirror["branches"], system_branch)
            len_country = max(len(m['country']) for m in mirrors) + 1
            last_sync = mirror["last_sync"]
            if last_sync == "-1":
                last_sync = "--:--"
                color = C_KO
                text = "--"
            print(f"Mirror #{str(i + 1):2}", color, f"{text}", C_NONE,
                  f"{last_sync:7} {mirror['country']:{len_country}} {mirror['url']}")
            if i == 0 and color == C_KO:
                exit_code = 4  # first mirror not sync !
        except IndexError:
            print(C_KO, f"Mirror #{i + 1:2}", f"{url} does not exist{C_NONE}")
            exit_code = 5  # not found

    return exit_code


# def get_static_mirror(filename: str) -> dict:
#     """
#     Get first mirror from mirror pool
#     :param filename:
#     :return:
#     """
#     mirror = read_json_file(filename)
#     return mirror[0]

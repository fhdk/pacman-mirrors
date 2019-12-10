#!/usr/bin/env python

from urllib import request
import json
from pacman_mirrors.constants import colors

C_KO = colors.RED
C_OK = colors.GREEN
C_NONE = colors.RESET


def get_local_mirrors() -> tuple:
    urls = []
    with open("/etc/pacman.d/mirrorlist", "r") as f_list:
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


def get_state(states: list, branch: str) -> str:
    ret_color = C_OK
    x = states[0]
    if branch == "testing":
        x = states[1]
    if branch == "unstable":
        x = states[2]
    if x == 0:
        ret_color = C_KO
    return ret_color


system_branch, mirrors_pacman = get_local_mirrors()
with request.urlopen('https://repo.manjaro.org/status.json') as f_url:
    req = f_url.read()

mirrors = json.loads(req)
mirrors = [m for m in mirrors if m['url'] in mirrors_pacman]

print("Branch:", system_branch)
exit_code = 0  # up-to-date
for i, url in enumerate(mirrors_pacman):  # same order as pacman-conf
    try:
        mirror = [m for m in mirrors if m['url'] == url][0]
        color = get_state(mirror["branches"], system_branch)
        print(color, f"{i + 1:2}", C_NONE, f"{mirror['last_sync']:7} {mirror['country']:26} {mirror['url']}")
        if i == 0 and color == C_KO:
            exit_code = 4  # first mirror not sync !
    except IndexError:
        print(C_KO, f"{i + 1:2}", C_NONE, f"{C_KO}{url}{C_NONE} not exists")
        exit_code = 5  # not found

# print("pacman config:")
# for mirror in mirrors_pacman:
#    print("  " + mirror)

exit(exit_code)

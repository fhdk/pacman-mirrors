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
# Authors: Frede Hundewadt <frede@hundewadt.dk>

"""Manjaro-Mirrors File Functions"""

import os
import datetime
from .configuration import FALLBACK, MIRROR_FILE, REPO_ARCH, STATUS_FILE
from .jsonfn import JsonFn
from . import txt


class FileFn:
    """FileMethods class"""

    @staticmethod
    def check_file(filename):
        """Check if file exist"""
        return os.path.isfile(filename)

    @staticmethod
    def dir_must_exist(dir_name):
        """Check necessary directory"""
        os.makedirs(dir_name, mode=0o755, exist_ok=True)

    @staticmethod
    def return_mirror_filename():
        """Load default mirror file
        :returns tuple with file and status
        """
        filename = ""
        status = False  # status.json or mirrors.json
        # decision on file avaiablity
        if FileFn.check_file(STATUS_FILE):
            status = True
            filename = STATUS_FILE
        elif FileFn.check_file(MIRROR_FILE):
            filename = MIRROR_FILE
        else:
            if FileFn.check_file(FALLBACK):
                filename = FALLBACK
        if not filename:
            print("\n{}.:! {}{}\n".format(txt.RS,
                                          txt.HOUSTON,
                                          txt.CE))
            exit(1)
        result = (filename, status)
        return result

    @staticmethod
    def output_mirror_list(branch, mirrorlistfile, servers, custom=False, quiet=False):
        """Write servers to /etc/pacman.d/mirrorlist
        :param: servers: list of servers to write
        """
        try:
            with open(mirrorlistfile, "w") as outfile:
                print(".: {} {}".format(txt.INF_CLR, txt.WRITING_MIRROR_LIST))
                # write list header
                FileFn.write_mirrorlist_header(outfile, custom=custom)
                for server in servers:
                    url = server["url"]
                    for protocol in enumerate(server["protocols"]):
                        pos = url.find(":")
                        server["url"] = "{}{}{}{}".format(protocol[1],
                                                          url[pos:],
                                                          branch,
                                                          REPO_ARCH)
                        # write list entry
                        FileFn.write_mirrorlist_entry(outfile, server)
                        if not quiet:
                            print("   {}{:<15}{} : {}".format(txt.YS,
                                                              server["country"],
                                                              txt.CE,
                                                              server["url"]))
                print(".: {} {}: {}".format(txt.INF_CLR,
                                            txt.MIRROR_LIST_SAVED,
                                            mirrorlistfile))
        except OSError as err:
            print(".: {} {}: {}: {}".format(txt.ERR_CLR,
                                            txt.CANNOT_WRITE_FILE,
                                            err.filename,
                                            err.strerror))
            exit(1)

    @staticmethod
    def read_mirror_file(filename):
        """Read a mirror file
        :returns: list of mirrors
        """
        return JsonFn.read_json_file(filename, dictionary=True)

    @staticmethod
    def write_mirrorlist_header(handle, custom=False):
        """Write mirrorlist header
        :param handle: handle to a file opened for writing
        :param custom: controls content of the header
        """
        handle.write("##\n")
        if custom:
            handle.write("## Manjaro Linux Custom mirrorlist\n")
            handle.write("## Generated on {}\n".format(
                datetime.datetime.now().strftime("%d %B %Y %H:%M")))
            handle.write("##\n")
            handle.write("## Use 'pacman-mirrors -c all' to reset\n")
        else:
            handle.write("## Manjaro Linux mirrorlist\n")
            handle.write("## Generated on {}\n".format(
                datetime.datetime.now().strftime("%d %B %Y %H:%M")))
            handle.write("##\n")
            handle.write("## Use pacman-mirrors to modify\n")
        handle.write("##\n\n")

    @staticmethod
    def write_mirrorlist_entry(handle, mirror):
        """Write mirror to mirror list or file
        :param handle: handle to a file opened for writing
        :param mirror: mirror object
        """
        workitem = mirror
        handle.write("## Country       : {}\n".format(workitem["country"]))
        handle.write("Server = {}\n\n".format(workitem["url"]))

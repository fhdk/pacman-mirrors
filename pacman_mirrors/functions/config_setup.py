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

"""Pacman-Mirrors Configuration Functions"""

import sys

from pacman_mirrors.config import configuration
from pacman_mirrors.constants import txt
from pacman_mirrors.functions import util


def setup_config(self) -> tuple:
    """Get config information
    :returns: config, custom
    :rtype: tuple
    """
    custom = False
    # default config
    config = {
        "arm": False,
        "branch": "stable",
        "branches": configuration.BRANCHES,
        "config_file": configuration.CONFIG_FILE,
        "country_pool": [],
        "custom_file": configuration.CUSTOM_FILE,
        "enterprise": False,  # refactor - part of refactor for new mirror-manager
        "method": "rank",
        "mirror_file": configuration.MIRROR_FILE,
        "mirror_list": configuration.MIRROR_LIST,
        "mirror_manager": configuration.MIRROR_MANAGER,
        "no_update": False,
        "protocols": [],
        "repo_arch": configuration.REPO_ARCH,
        "ssl_verify": True,
        "static": "",
        # "status_file": conf.STATUS_FILE, # removed - part of refactor for new mirror-manager
        "test_file": configuration.TEST_FILE,
        "timeout": 2,
        # "url_status_json": conf.URL_STATUS_JSON, #  removed - part of refactor for new mirror-manager
        "var_dir": configuration.VAR_DIR,
    }
    # try to replace default entries by reading conf file
    try:
        with open(configuration.CONFIG_FILE) as conf_file:
            for line in conf_file:
                line = line.strip()
                if line.startswith("#") or "=" not in line:
                    continue
                (key, value) = line.split("=", 1)
                key = key.lstrip().rstrip().lower()
                value = value.lstrip()
                if key and value:
                    if value.startswith("\"") and value.endswith("\""):
                        value = value[1:-1]
                    if key == "method":
                        config["method"] = value
                    if key == "branch":
                        config["branch"] = value
                    if key == "protocols":
                        if "," in value:
                            config["protocols"] = value.split(",")
                        else:
                            config["protocols"] = value.split(" ")
                    if key == "sslverify":
                        config["ssl_verify"] = value.lower().capitalize()
                    if key == "TestFile":
                        config["test_file"] = value
                        if not config["test_file"]:
                            config["test_file"] = configuration.TEST_FILE
                    # refactor Enterprise mirror option
                    if key == "static":
                        custom = False
                        config["enterprise"] = True
                        config["static"] = value

    except (PermissionError, OSError) as err:
        util.msg(message=f"{txt.CANNOT_READ_FILE}: {err.filename}: {err.strerror}", urgency=txt.ERR_CLR, tty=self.tty)
        sys.exit(2)
    return config, custom


def sanitize_config(config: dict) -> bool:
    """
    Verify configuration
    :param config:
    """
    errors = []
    header = f".: {txt.ERR_CLR}: {txt.INVALID_SETTING_IN} `{configuration.CONFIG_FILE}`"
    # Check Method
    if config["method"] not in configuration.METHODS:
        errors.append("     'Method = {}'; {} {}".format(
            config["method"], txt.EXP_CLR, "|".join(configuration.METHODS)))
    # Check Branch
    if config["arm"]:
        if config["branch"] not in configuration.ARM_BRANCHES:
            errors.append("     'Branch = {}'; {} {}".format(
                config["branch"], txt.EXP_CLR, "|".join(configuration.ARM_BRANCHES)))
    else:
        if config["branch"] not in configuration.BRANCHES:
            errors.append("     'Branch = {}'; {} {}".format(
                config["branch"], txt.EXP_CLR, "|".join(configuration.BRANCHES)))
    # Check SSLVerify
    if str(config["ssl_verify"]) not in configuration.SSL:
        errors.append("     'SSLVerify = {}'; {} {}".format(
            config["ssl_verify"], txt.EXP_CLR, "|".join(configuration.SSL)))
    # Check Protocols
    for p in config["protocols"]:
        if p not in configuration.PROTOCOLS:
            errors.append("     'Protocols = {}'; {} {}".format(
                config["protocols"], txt.EXP_CLR, ",".join(configuration.PROTOCOLS)))
    if config["enterprise"]:
        # check static mirror - simple validation
        if "://" or "." not in config["static"]:
            errors.append("     'Static = {}'; {} (e.g. 'http://domain.tld/manjaro/')".format(
                config["static"], txt.EXP_CLR))

    if len(errors):
        print(header)
        for e in errors:
            print(e)
        return False
    return True

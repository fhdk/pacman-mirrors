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

"""Pacman-Mirrors Default Pool/Mirror Functions"""

from operator import itemgetter
from pacman_mirrors.functions import pools
from pacman_mirrors.functions import customFn
from pacman_mirrors.functions import fileFn


def load_config_mirror_pool(self) -> None:
    """
    Load mirrors from configured mirror pool
    @param self:
    """
    if self.geoip or self.continent:
        customFn.delete_custom_pool(self)
    if customFn.check_custom_pool(self) and not self.config["country_pool"]:
        customFn.load_custom_pool(self)
        self.selected_countries = self.mirrors.country_pool
    else:
        if self.config["country_pool"]:
            self.selected_countries = self.config["country_pool"]
        # load default mirrors
        load_default_mirror_pool(self)
    """
    Validate the list of selected countries
    """
    self.selected_countries = pools.build_country_list(self)


def load_default_mirror_pool(self) -> None:
    """
    Load all available mirrors
    @param self:
    """
    file = fileFn.return_mirror_filename(config=self.config, tty=self.tty)
    # seed mirrors
    seed_mirrors(self, file)


def seed_mirrors(self, file: str) -> None:
    """
    Seed mirrors
    @param self:
    @param file:
    """
    if self.config["enterprise"]:
        import random
        from decimal import Decimal
        x = list(range(1,2000))
        m = {
            "branches": [1, 1, 1, 1, 1, 1],
            "country": "Enterprise",
            "protocols": [str.split(self.config["static"], ":")[0]],
            "url": str.split(self.config["static"], "//")[-1],
            "speed": Decimal(int(random.shuffle(x))) / 1000
        }
        mirrors = [m]
    else:
        mirrors = fileFn.read_mirror_file(file)

    self.mirrors.seed(mirrors)
    sort_mirror_countries(self)


def sort_mirror_countries(self) -> None:
    self.mirrors.mirror_pool = sorted(self.mirrors.mirror_pool, key=itemgetter("country"))
    self.mirrors.country_pool = sorted(self.mirrors.country_pool)


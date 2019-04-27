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

"""Pacman-Mirrors Country Functions"""
from pacman_mirrors.constants.timezones import countries

from pacman_mirrors.functions.httpFn import get_ip_country
from pacman_mirrors.functions.validFn import country_list_is_valid, custom_config_is_valid


def build_country_list(country_selection: list, country_pool: list, tty: bool = False, geoip: bool = False) -> list:
    """
    Do a check on the users country selection
    :param country_selection:
    :param country_pool:
    :param tty:
    :param geoip:
    :return: list of valid countries
    :rtype: list
    """
    """
    # Dear Fellow Manjaro Maintainer:
    # When I wrote this code, only I knew how it worked.
    # Now, no one knows!
    # 
    # Therefore if you are trying to optimize 
    # this routine and it fails (most surely),
    # please increase this counter as a warning for the next person.
    # 
    # total_hours_wasted_here = 1
    """
    result = []
    if country_selection:
        if country_selection == ["all"]:
            result = country_pool
        else:
            if country_list_is_valid(onlycountry=country_selection,
                                     countrylist=country_pool,
                                     tty=tty):
                result = country_selection
    if not result:
        if geoip:
            country = get_geoip_country(country_pool)
            if country:
                result = country
            else:
                result = country_pool
        else:
            result = country_pool
    return result


def get_geoip_country(country_pool: list) -> str:
    """
    Check if geoip is possible
    :param country_pool:
    :return: country name if found
    """
    country_name = get_ip_country().replace(" ", "_")
    selection = (x for x in country_pool if country_name in x["country"])
    for select in selection:
        return select["country"]
    return ""


def get_continent(country: str) -> str:
    """
    get continent for country
    :param country:
    :return:
    """
    continents = (x for x in countries if country in x["name"])
    for continent in continents:
        return continent["continent"]
    return ""


def get_country() -> str:
    """
    Check country
    :return: country name
    """
    return get_ip_country().replace(" ", "_")

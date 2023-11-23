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
# from https://wiki.maemo.org/Internationalize_a_Python_application

"""Pacman-Mirrors Translation Module"""

import os
import sys
import locale
import gettext

#  The translation files will be under
#  @LOCALE_DIR@/@LANGUAGE@/LC_MESSAGES/@APP_NAME@.mo
APP_NAME = "pacman_mirrors"
APP_DIR = os.path.join(sys.prefix, "share")
LOCALE_DIR = os.path.join(APP_DIR, "locale")


def get_language():
    if locale.getlocale()[0] is not None:
        return locale.getlocale()[0]

    elif os.environ.get("LC_ALL") is not None:
        return os.environ.get("LC_ALL").split(".")[0]

    elif os.environ.get("LANGUAGE") is not None:
        return os.environ.get("LANGUAGE").split(".")[0]

    elif os.environ.get("LANG") is not None:
        return os.environ.get("LANG").split(".")[0]

    elif os.environ.get("GDM_LANG") is not None:
        return os.environ.get("GDM_LANG").split(".")[0]

    else:
        print("No translations found for your language, using english")
        return "en_US"


# Let us tell those details to gettext
#  (nothing to change here for you)
gettext.install(APP_NAME, LOCALE_DIR)
gettext.bindtextdomain(APP_NAME, LOCALE_DIR)
gettext.textdomain(APP_NAME)
language = gettext.translation(APP_NAME, LOCALE_DIR, [get_language()], fallback=True)

# Add this to every module:
#
# import i18n
# _ = i18n.language.gettext

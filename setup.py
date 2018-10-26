#!/bin/env python

import collections
import io
import json
import re
import os
from urllib.request import urlopen
from http.client import HTTPException
from socket import timeout
from urllib.error import URLError

from setuptools import setup


def update_mirror_file():
    """update mirrors.json from github"""
    countries = list()
    try:
        with urlopen(
            "https://gitlab.manjaro.org/tools/maintenance-tools/manjaro-web-repo/blob/master/mirrors.json") as \
             response:
            countries = json.loads(response.read().decode("utf8"), object_pairs_hook=collections.OrderedDict)
    except (HTTPException, json.JSONDecodeError, URLError, timeout):
        pass
    if countries:
        with open("share/mirrors.json", "w") as outfile:
            json.dump(countries, outfile, sort_keys=True, indent=4)


def read(*names, **kwargs):
    """read"""
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    """find version"""
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open('README.md') as readme_file:
    README = readme_file.read()

with open('CHANGELOG.md') as changelog_file:
    CHANGELOG = changelog_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

update_mirror_file()

setup(
    name='pacman-mirrors',
    version=find_version("pacman_mirrors", "__init__.py"),
    description="Package that provides all mirrors for Manjaro Linux.",
    long_description=README + '\n\n' + CHANGELOG,
    author="Roland Singer, Esclapion, Philip Müller, Ramon Buldó, Hugo Posnic, Frede Hundewadt",
    author_email='fh@manjaro.org',
    url='https://github.com/manjaro/pacman-mirrors',
    packages=['pacman_mirrors',
              'pacman_mirrors.api',
              'pacman_mirrors.builder',
              'pacman_mirrors.config',
              'pacman_mirrors.constants',
              'pacman_mirrors.dialogs',
              'pacman_mirrors.functions',
              'pacman_mirrors.mirrors',
              'pacman_mirrors.translation'],
    package_dir={'pacman_mirrors': 'pacman_mirrors'},
    data_files=[('/etc', ['conf/pacman-mirrors.conf']),
                ('/etc/pacman.d', []),
                ('share/man/man8', ['man/pacman-mirrors.8.gz']),
                ('share/pacman-mirrors', ['share/mirrors.json']),
                ('share/locale/az_AZ/LC_MESSAGES', ['locale/az_AZ/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/be/LC_MESSAGES', ['locale/be/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/bg/LC_MESSAGES', ['locale/bg/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/ca/LC_MESSAGES', ['locale/ca/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/cs/LC_MESSAGES', ['locale/cs/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/cy/LC_MESSAGES', ['locale/cy/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/da/LC_MESSAGES', ['locale/da/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/de/LC_MESSAGES', ['locale/de/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/el/LC_MESSAGES', ['locale/el/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/eo/LC_MES SAGES', ['locale/eo/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/es/LC_MESSAGES', ['locale/es/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/es_419/LC_MESSAGES', ['locale/es_419/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/es_ES/LC_MESSAGES', ['locale/es_ES/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/et/LC_MES SAGES', ['locale/et/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/fr/LC_MESSAGES', ['locale/fr/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/he/LC_MESSAGES', ['locale/he/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/hr/LC_MESSAGES', ['locale/hr/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/hr_HR/LC_MESSAGES', ['locale/hr_HR/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/hu/LC_MESSAGES', ['locale/hu/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/id_ID/LC_MESSAGES', ['locale/id_ID/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/is/LC_MESSAGES', ['locale/is/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/is_IS/LC_MESSAGES', ['locale/is_IS/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/it/LC_MESSAGES', ['locale/it/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/ja/LC_MESSAGES', ['locale/ja/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/lt/LC_MESSAGES', ['locale/lt/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/nb/LC_MESSAGES', ['locale/nb/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/nl/LC_MESSAGES', ['locale/nl/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/pl/LC_MESSAGES', ['locale/pl/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/pt/LC_MESSAGES', ['locale/pt/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/pt_BR/LC_MESSAGES', ['locale/pt_BR/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/pt_PT/LC_MESSAGES', ['locale/pt_PT/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/ro/LC_MESSAGES', ['locale/ro/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/ru_RU/LC_MESSAGES', ['locale/ru_RU/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/sk/LC_MESSAGES', ['locale/sk/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/sr/LC_MES SAGES', ['locale/sr/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/sv/LC_MESSAGES', ['locale/sv/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/tr/LC_MESSAGES', ['locale/tr/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/tr_TR/LC_MESSAGES', ['locale/tr_TR/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/uk/LC_MESSAGES', ['locale/uk/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/uk_UA/LC_MESSAGES', ['locale/uk_UA/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/zh_CN/LC_MESSAGES', ['locale/zh_CN/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/zh_TW/LC_MESSAGES', ['locale/zh_TW/LC_MESSAGES/pacman_mirrors.mo']),
                ],
    scripts=["scripts/pacman-mirrors"],
    install_requires=requirements,
    license="GPL3",
    zip_safe=False,
    keywords='pacman-mirrors',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End User/Desktop',
        'License :: OSI Approved :: GPL3 License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Environment :: Console'
    ],
    test_suite='tests',
    tests_require=test_requirements
)

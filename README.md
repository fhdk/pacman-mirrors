# Dev env:
```
poetry install
poetry shell
poetry pytest
poetry run pacman-mirrors
```

# pacman-mirrors

Package that provides all mirrors for Manjaro Linux.

- Free software: GPL license

## Features

- A GUI for selecting mirror/protocol combinations used to generate a custom list.
- Generate a new mirror list by using several options:
    - method      : rank or random.
    - country     : a single, a list or all.
    - fasttrack   : limited ranked list of `x` up-to-date mirrors.
    - geoip       : mirrors for country if available.
- Information
    - get-branch  : get current branch from config
    - country-list: list of countries with mirrors
- API
    - prefix      : prefix for files handled by pacman-mirrors.
    - set-branch  : set branch from supplied branch option to config
    - protocols:
        - set protocol limitation in config
        - remove protocol limitation from config

## Technologies

pacman-mirrors is build with Python and Gtk3.

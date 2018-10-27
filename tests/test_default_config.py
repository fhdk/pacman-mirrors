#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors.functions import configFn
from pacman_mirrors.pacman_mirrors import PacmanMirrors
from . import mock_configuration as mock

test_conf = {
    "to_be_removed": mock.TO_BE_REMOVED,
    "branch": "stable",
    "branches": mock.BRANCHES,
    "config_file": mock.CONFIG_FILE,
    "custom_file": mock.CUSTOM_FILE,
    "method": "rank",
    "work_dir": mock.WORK_DIR,
    "mirror_file": mock.MIRROR_FILE,
    "mirror_list": mock.MIRROR_LIST,
    "no_update": False,
    "country_pool": [],
    "protocols": [],
    "repo_arch": mock.REPO_ARCH,
    "status_file": mock.STATUS_FILE,
    "ssl_verify": True,
    "test_file": mock.TEST_FILE,
    "url_mirrors_json": mock.URL_MIRROR_JSON,
    "url_status_json": mock.URL_STATUS_JSON,
    "x32": False
}


class TestDefaultConfig(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    @patch("os.getuid")
    @patch.object(configFn, "setup_config")
    def test_default_branch(self, mock_build_config, mock_os_getuid):
        """TEST: config[branch] = stable"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-f1"]):
            app = PacmanMirrors()
            app.config["config_file"] = mock.CONFIG_FILE
            app.config = configFn.setup_config()
            assert app.config["branch"] == "stable"

    @patch("os.getuid")
    @patch.object(configFn, "setup_config")
    def test_default_method(self, mock_build_config, mock_os_getuid):
        """TEST: config[method] = rank"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-f1"]):
            app = PacmanMirrors()
            app.config["config_file"] = mock.CONFIG_FILE
            app.config = configFn.setup_config()
            assert app.config["method"] == "rank"

    @patch("os.getuid")
    @patch.object(configFn, "setup_config")
    def test_default_mirrordir(self, mock_build_config, mock_os_getuid):
        """TEST: config[mirror_dir] = tests/mock/var/"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-f1"]):
            app = PacmanMirrors()
            app.config = configFn.setup_config()
            assert app.config["work_dir"] == "tests/mock/var/"

    @patch("os.getuid")
    @patch.object(configFn, "setup_config")
    def test_default_mirrorfile(self, mock_build_config, mock_os_getuid):
        """TEST: config[mirror_file] = tests/mock/usr/mirrors.json"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-f1"]):
            app = PacmanMirrors()
            app.config = configFn.setup_config()
            assert app.config["mirror_file"] == "tests/mock/usr/mirrors.json"

    @patch("os.getuid")
    @patch.object(configFn, "setup_config")
    def test_default_mirrorlist(self, mock_build_config, mock_os_getuid):
        """TEST: config[mirror_list] = tests/mock/etc/mirrorlist"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-f1"]):
            app = PacmanMirrors()
            app.config = configFn.setup_config()
            assert app.config["mirror_list"] == "tests/mock/etc/mirrorlist"

    @patch("os.getuid")
    @patch.object(configFn, "setup_config")
    def test_default_noupdate(self, mock_build_config, mock_os_getuid):
        """TEST: config[no_update] = False"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-f1"]):
            app = PacmanMirrors()
            app.config = configFn.setup_config()
            assert app.config["no_update"] is False

    @patch("os.getuid")
    @patch.object(configFn, "setup_config")
    def test_default_onlycountry(self, mock_build_config, mock_os_getuid):
        """TEST: config[only_country] = []"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-f1"]):
            app = PacmanMirrors()
            app.config["config_file"] = mock.CONFIG_FILE
            app.config = configFn.setup_config()
            assert app.config["country_pool"] == []

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors.functions import config_setup
from pacman_mirrors.pacman_mirrors import PacmanMirrors
from . import mock_configuration as mock

test_conf = {
    "arm": False,
    "branch": "stable",
    "branches": mock.BRANCHES,
    "config_file": mock.CONFIG_FILE,
    "country_pool": [],
    "custom_file": mock.CUSTOM_FILE,
    "enterprise": False,  # refactor - part of refactor for new mirror-manager
    "method": "rank",
    "mirror_file": mock.MIRROR_FILE,
    "mirror_list": mock.MIRROR_LIST,
    "mirror_manager": mock.MIRROR_MANAGER,
    "no_update": False,
    "protocols": [],
    "repo_arch": mock.REPO_ARCH,
    "ssl_verify": True,
    "static": None,
    # "status_file": conf.STATUS_FILE, # removed - part of refactor for new mirror-manager
    "test_file": mock.TEST_FILE,
    "timeout": 2,
    # "url_status_json": conf.URL_STATUS_JSON, #  removed - part of refactor for new mirror-manager
    "var_dir": mock.VAR_DIR,
}


class TestDefaultConfig(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    @patch("os.getuid")
    @patch.object(config_setup, "setup_config")
    def test_default_branch(self, mock_build_config, mock_os_getuid):
        """TEST: config[branch] = stable"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-f1"]):
            app = PacmanMirrors()
            app.config["config_file"] = mock.CONFIG_FILE
            app.config = config_setup.setup_config(self)
            assert app.config["branch"] == "stable"

    @patch("os.getuid")
    @patch.object(config_setup, "setup_config")
    def test_default_method(self, mock_build_config, mock_os_getuid):
        """TEST: config[method] = rank"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-f1"]):
            app = PacmanMirrors()
            app.config["config_file"] = mock.CONFIG_FILE
            app.config = config_setup.setup_config(self)
            assert app.config["method"] == "rank"

    @patch("os.getuid")
    @patch.object(config_setup, "setup_config")
    def test_default_mirrordir(self, mock_build_config, mock_os_getuid):
        """TEST: config[mirror_dir] = tests/mock/var/"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-f1"]):
            app = PacmanMirrors()
            app.config = config_setup.setup_config(self)
            assert app.config["var_dir"] == "tests/mock/var/"

    @patch("os.getuid")
    @patch.object(config_setup, "setup_config")
    def test_default_mirrorfile(self, mock_build_config, mock_os_getuid):
        """TEST: config[mirror_file] = tests/mock/var/status.json"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-f1"]):
            app = PacmanMirrors()
            app.config = config_setup.setup_config(self)
            assert app.config["mirror_file"] == "tests/mock/var/status.json"

    @patch("os.getuid")
    @patch.object(config_setup, "setup_config")
    def test_default_mirrorlist(self, mock_build_config, mock_os_getuid):
        """TEST: config[mirror_list] = tests/mock/etc/mirrorlist"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-f1"]):
            app = PacmanMirrors()
            app.config = config_setup.setup_config(self)
            assert app.config["mirror_list"] == "tests/mock/etc/mirrorlist"

    @patch("os.getuid")
    @patch.object(config_setup, "setup_config")
    def test_default_noupdate(self, mock_build_config, mock_os_getuid):
        """TEST: config[no_update] = False"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-f1"]):
            app = PacmanMirrors()
            app.config = config_setup.setup_config(self)
            assert app.config["no_update"] is False

    @patch("os.getuid")
    @patch.object(config_setup, "setup_config")
    def test_default_onlycountry(self, mock_build_config, mock_os_getuid):
        """TEST: config[only_country] = []"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-f1"]):
            app = PacmanMirrors()
            app.config["config_file"] = mock.CONFIG_FILE
            app.config = config_setup.setup_config(self)
            assert app.config["country_pool"] == []

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors.functions import cliFn
from pacman_mirrors.functions import configFn
from pacman_mirrors.pacman_mirrors import PacmanMirrors
from . import mock_configuration as mock

test_conf = {
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


class TestCommandLineParse(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    # @patch("os.getuid")
    # @patch.object(configFn, "setup_config")
    # def test_arg_branch_unstable(self, mock_build_config, mock_os_getuid):
    #     """TEST: CLI config[branch] from ARG '-b unstable'"""
    #     mock_os_getuid.return_value = 0
    #     mock_build_config.return_value = test_conf
    #     with unittest.mock.patch("sys.argv",
    #                              ["pacman-mirrors",
    #                               "-b", "unstable"]):
    #         app = PacmanMirrors()
    #         app.config["config_file"] = mock.CONFIG_FILE
    #         app.config = configFn.setup_config()
    #         cli.parse_command_line(app, True)
    #         assert app.config["branch"] == "unstable"
    #
    # @patch("os.getuid")
    # @patch.object(configFn, "setup_config")
    # def test_arg_branch_testing(self, mock_build_config, mock_os_getuid):
    #     """TEST: CLI config[branch] from ARG '-b testing'"""
    #     mock_os_getuid.return_value = 0
    #     mock_build_config.return_value = test_conf
    #     with unittest.mock.patch("sys.argv",
    #                              ["pacman-mirrors",
    #                               "-b", "testing"]):
    #         app = PacmanMirrors()
    #         app.config["config_file"] = mock.CONFIG_FILE
    #         app.config = configFn.setup_config()
    #         cli.parse_command_line(app, True)
    #         assert app.config["branch"] == "testing"

    @patch("os.getuid")
    @patch.object(configFn, "setup_config")
    def test_arg_method(self, mock_build_config, mock_os_getuid):
        """TEST: CLI config[method] from ARG '-m random'"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-m", "random"]):
            app = PacmanMirrors()
            app.config["config_file"] = mock.CONFIG_FILE
            app.config = configFn.setup_config()
            cliFn.parse_command_line(app, True)
            assert app.config["method"] == "random"

    @patch("os.getuid")
    @patch.object(configFn, "setup_config")
    def test_arg_onlycountry(self, mock_build_config, mock_os_getuid):
        """TEST: CLI config[only_country] from ARG '-c France,Germany'"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-c", "France,Germany"]):
            app = PacmanMirrors()
            app.config["config_file"] = mock.CONFIG_FILE
            app.config = configFn.setup_config()
            cliFn.parse_command_line(app, True)
            assert app.config["country_pool"] == ["France", "Germany"]

    @patch("os.getuid")
    @patch.object(configFn, "setup_config")
    def test_arg_geoip(self, mock_build_config, mock_os_getuid):
        """TEST: CLI geoip is True from ARG '--geoip'"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "--geoip"]):
            app = PacmanMirrors()
            app.config["config_file"] = mock.CONFIG_FILE
            app.config = configFn.setup_config()
            cliFn.parse_command_line(app, True)
            assert app.geoip is True

    @patch("os.getuid")
    @patch.object(configFn, "setup_config")
    def test_arg_fasttrack(self, mock_build_config, mock_os_getuid):
        """TEST: CLI fasttrack is 5 from ARG '-f 5'"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-f5"]):
            app = PacmanMirrors()
            app.config["config_file"] = mock.CONFIG_FILE
            app.config = configFn.setup_config()
            cliFn.parse_command_line(app, True)
            assert app.fasttrack == 5

    @patch("os.getuid")
    @patch.object(configFn, "setup_config")
    def test_arg_interactive(self, mock_build_config, mock_os_getuid):
        """TEST: CLI interactive is true from ARG '-i'"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-i"]):
            app = PacmanMirrors()
            app.config["config_file"] = mock.CONFIG_FILE
            app.config = configFn.setup_config()
            cliFn.parse_command_line(app, True)
            assert app.interactive is True

    @patch("os.getuid")
    @patch.object(configFn, "setup_config")
    def test_arg_max_wait_time(self, mock_build_config, mock_os_getuid):
        """TEST: CLI max_wait_time is 5 from ARG '-t 5'"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-t5"]):
            app = PacmanMirrors()
            app.config["config_file"] = mock.CONFIG_FILE
            app.config = configFn.setup_config()
            cliFn.parse_command_line(app, True)
            assert app.max_wait_time == 5

    @patch("os.getuid")
    @patch.object(configFn, "setup_config")
    def test_arg_quiet(self, mock_build_config, mock_os_getuid):
        """TEST: CLI quiet is True from ARG '-q'"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-q"]):
            app = PacmanMirrors()
            app.config["config_file"] = mock.CONFIG_FILE
            app.config = configFn.setup_config()
            cliFn.parse_command_line(app, True)
            assert app.quiet is True

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""
import unittest
from unittest.mock import patch

from pacman_mirrors.builder import common, fasttrack
from pacman_mirrors.functions import fileFn, config_setup, cliFn, defaultFn
from pacman_mirrors.functions import httpFn
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


class TestPacmanMirrors(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    @patch("os.getuid")
    @patch.object(config_setup, "setup_config")
    def test_full_run_fasttrack(self,
                                mock_build_config,
                                mock_os_getuid):
        """TEST: pacman-mirrors -f5"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-f5"]):
            app = PacmanMirrors()
            app.config = config_setup.setup_config(self)
            fileFn.create_dir(test_conf["var_dir"])
            cliFn.parse_command_line(app, True)
            httpFn.download_mirror_pool(test_conf)
            defaultFn.load_default_mirror_pool(app)
            fasttrack.build_mirror_list(app, app.fasttrack)

    @patch("os.getuid")
    @patch.object(config_setup, "setup_config")
    def test_full_run_random(self,
                             mock_build_config,
                             mock_os_getuid):
        """TEST: pacman-mirrors -c all -m random"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-c", "all",
                                  "-m", "random"]):
            app = PacmanMirrors()
            app.config = config_setup.setup_config(self)
            fileFn.create_dir(test_conf["var_dir"])
            cliFn.parse_command_line(app, True)
            httpFn.download_mirror_pool(app.config)
            defaultFn.load_default_mirror_pool(app)
            common.build_mirror_list(app)

    @patch("os.getuid")
    @patch.object(config_setup, "setup_config")
    def test_full_run_rank(self,
                           mock_build_config,
                           mock_os_getuid):
        """TEST: pacman-mirrors -c all"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = test_conf
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "-c", "all"]):
            app = PacmanMirrors()
            app.config = config_setup.setup_config(self)
            fileFn.create_dir(test_conf["var_dir"])
            cliFn.parse_command_line(app, True)
            httpFn.download_mirror_pool(app.config)
            defaultFn.load_default_mirror_pool(app)
            common.build_mirror_list(app)

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()

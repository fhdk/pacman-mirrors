#!/usr/bin/env python

"""
test_pacman-mirrors
----------------------------------

Tests for `pacman-mirrors` module.
"""

import unittest
from unittest.mock import patch

from pacman_mirrors.functions import httpFn, config_setup, cliFn, defaultFn
from pacman_mirrors.pacman_mirrors import PacmanMirrors
from . import mock_configuration as mock

config = {
    "arm": False,
    "branch": "stable",
    "branches": mock.BRANCHES,
    "config_file": mock.CONFIG_FILE,
    "country_pool": ["Denmark"],
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


class TestHttpFn(unittest.TestCase):
    """Pacman Mirrors Test suite"""
    def setUp(self):
        """Setup tests"""
        pass

    @patch("os.getuid")
    @patch.object(httpFn, "get_ip_country")
    @patch.object(config_setup, "setup_config")
    def test_geoip_available(self,
                             mock_build_config,
                             mock_get_geoip_country,
                             mock_os_getuid):
        """TEST: geoip country IS avaiable"""
        mock_os_getuid.return_value = 0
        mock_build_config.return_value = config
        mock_get_geoip_country.return_value = ["Denmark"]
        self.config = config
        with unittest.mock.patch("sys.argv",
                                 ["pacman-mirrors",
                                  "--geoip"]):
            app = PacmanMirrors()
            app.config = config_setup.setup_config(self)
            cliFn.parse_command_line(app, True)
            defaultFn.load_default_mirror_pool(app)
            app.selected_countries = httpFn.get_ip_country()
            assert app.selected_countries == ["Denmark"]

    def tearDown(self):
        """Tear down"""
        pass


if __name__ == "__main__":
    unittest.main()

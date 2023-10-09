#!/usr/bin/env python

import subprocess
import unittest

branches = ("stable", "testing", "unstable")

def _test_command_works_properly(args):
    cmd = "sudo /usr/bin/python /usr/bin/pacman-mirrors "
    try:
        result = subprocess.run(cmd + args, check=True, capture_output=True, text=True, shell=True)
    except subprocess.CalledProcessError as error:
        print(error.stdout)
        print(error.stderr)
        raise error
    
class TestDefaultConfig(unittest.TestCase):
    
    def test_branch(self):
        args = "--api --get-branch"
        _test_command_works_properly(args)

    def test_gioip(self):
        for i in branches:
            args = f"--geoip --api -B {i}"
            _test_command_works_properly(args)

    def test_fasttrack(self):
        for i in branches:
            args = f"-f 5 --api -B {i}"
        _test_command_works_properly(args)

    def test_default(self):
        for i in branches:
            args = f"-g --api -B {i}"
            _test_command_works_properly(args)

    def test_country_stable(self):
        args = "-c Germany --api -B stable"
        _test_command_works_properly(args)

    def test_country_testing(self):
        args = "-c France --api -B testing"
        _test_command_works_properly(args)

    def test_country_unstable(self):
        args = "-c Italy --api -B unstable"
        _test_command_works_properly(args)

    def test_interactive_country(self):
        args = "-i -c Italy --api -B stable"
        _test_command_works_properly(args)

if __name__ == "__main__":
    unittest.main()

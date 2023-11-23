#!/usr/bin/env python

from subprocess import PIPE, run, CalledProcessError
import unittest

branches = ("stable", "testing", "unstable")

def _test_command_works_properly(args):
    cmd = "sudo /usr/bin/python /usr/bin/pacman-mirrors "
    result = {
        "stdout": None,
        "stderr": None,
        "error": None
    }
    try:
        shell = run(
            cmd + args,
            check=True,
            capture_output=True,
            text=True,
            shell=True
            )
        
        result["stdout"] = shell.stdout        
        return result
    except CalledProcessError as error:
        result["stdout"] = error.stdout
        result["stderr"] = error.stderr
        result["error"] = error
        return result
    
class TestDefaultConfig(unittest.TestCase):
    # TODO implement mirrorlist outputcheck using test-checkpoints.md guidelines

    def test_branch(self):
        args = "--api --get-branch"
        result = _test_command_works_properly(args)
        if result["error"]:
            raise result["error"]

    def test_gioip(self):
        for i in branches:
            args = f"--geoip --api -B {i}"
            result = _test_command_works_properly(args)
            if result["error"]:
                raise result["error"]

    def test_fasttrack(self):
        for i in branches:
            args = f"-f 5 --api -B {i}"
            result = _test_command_works_properly(args)
            if result["error"]:
                raise result["error"]

    def test_default(self):
        for i in branches:
            args = f"-g --api -B {i}"
            result = _test_command_works_properly(args)
            if result["error"]:
                raise result["error"]

    def test_country_stable(self):
        args = "-c Germany --api -B stable"
        result = _test_command_works_properly(args)
        if result["error"]:
            raise result["error"]

    def test_country_testing(self):
        args = "-c France --api -B testing"
        result = _test_command_works_properly(args)
        if result["error"]:
            raise result["error"]

    def test_country_unstable(self):
        args = "-c Italy --api -B unstable"
        result = _test_command_works_properly(args)
        if result["error"]:
            raise result["error"]

    def test_interactive_country(self):
        args = "-i -c Italy --api -B stable"
        result = _test_command_works_properly(args)
        if result["error"]:
            raise result["error"]

    def test_reset_mirrors(self):
        args = "-c all"
        result = _test_command_works_properly(args)
        if result["error"]:
            raise result["error"]

    def test_invalid_arguments(self):
        args = "--invalid-args"
        result = _test_command_works_properly(args)
        if result["error"]:
            self.assertIsNotNone(result["error"])


if __name__ == "__main__":
    unittest.main()

import unittest

from click.testing import CliRunner

from src import __version__ as version
from src.cli import cli

class TestCLI(unittest.TestCase):
    def test_cli(self):
        """Run `dmps` without arguments."""
        result = CliRunner().invoke(cli, [])

        assert result.exit_code == 0
        assert "dmps" in result.output

    def test_print_version(self):
        """Chech that `dmps --version` and `dmps -V` output contain
        the current package version."""

        result = CliRunner().invoke(cli, ["--version"])

        assert result.exit_code == 0
        assert version in result.output

        result_abr = CliRunner().invoke(cli, ["-V"])
        assert result_abr.exit_code == 0
        assert version in result_abr.output


if __name__ == '__main__':
    unittest.main()

import unittest

from click.testing import CliRunner


class TestCLI(unittest.TestCase):
    def test_cli(self):
        """Run `dmps` without arguments."""
        result = CliRunner().invoke(cli, [])

        assert result.exit_code == 0
        assert "dmps" in result.output

    def test_version(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()

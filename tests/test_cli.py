import unittest

from click.testing import CliRunner


class TestCLI(unittest.TestCase):
    def test_cli(self):
        """Run `dmps` without arguments."""
        result = CliRunner().invoke(dmps, [])

        assert result.exit_code == 0
        assert "dmps" in result.output


if __name__ == '__main__':
    unittest.main()

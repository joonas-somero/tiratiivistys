import unittest
from click.testing import CliRunner
from tiratiivistys.user_interface import command_line_interface as cli


class TestUserInterface(unittest.TestCase):
    def test_cli(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['--compress', 'tests/testfile.txt'])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, "Compressing tests/testfile.txt...\n")

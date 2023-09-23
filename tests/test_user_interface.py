import unittest
import tempfile
from click.testing import CliRunner
from tiratiivistys.user_interface import command_line_interface as cli


class TestUserInterface(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.filename = "testfile.bin"

    def test_cli_exit_code_and_stdout(self):
        command_line_arguments = ['--algorithm', 'lempel-ziv',
                                  '--compress',
                                  self.filename]
        expected_output = "Compressing " + \
                          self.filename + \
                          " using Lempel-Ziv...\n"
        with self.runner.isolated_filesystem():
            with open('testfile.bin', 'wb') as f:
                f.write(b'Some test bytes.')

            result = self.runner.invoke(cli, command_line_arguments)

            self.assertEqual(result.exit_code, 0)
            self.assertEqual(result.output, expected_output)

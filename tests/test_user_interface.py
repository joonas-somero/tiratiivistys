import unittest
from click.testing import CliRunner
from tiratiivistys.user_interface import command_line_interface as cli


class TestUserInterface(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_cli(self):
        command_line_arguments = ['--algorithm', 'huffman',
                                  '--compress',
                                  'tests/testfile.txt']
        expected_output = "Compressing tests/testfile.txt using Huffman...\n"

        result = self.runner.invoke(cli, command_line_arguments)

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, expected_output)

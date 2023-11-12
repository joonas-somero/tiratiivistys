import unittest
from unittest.mock import Mock
from tempfile import TemporaryFile

from tiratiivistys.compressor import Compressor


class TestCompressor(unittest.TestCase):
    def test_compressor_instantiates_Model_with_input_file(self):
        Model = Mock()
        input_file = TemporaryFile()
        compressor = Compressor(Model, input_file, TemporaryFile())
        compressor.deploy()

        Model.assert_called_with(input_file)

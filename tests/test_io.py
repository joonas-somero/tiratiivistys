import unittest
from random import randbytes

from bitstring import Bits

from tiratiivistys.constants import N_BITS
from tiratiivistys.classes import Codeword
from tiratiivistys.huffman.io import HuffmanReader, HuffmanWriter
from tiratiivistys.lempel_ziv.io import LempelZivReader, LempelZivWriter
from tests import helpers


class TestHuffmanReader(unittest.TestCase):
    def test_reader_methods_ignore_padding(self):
        # 10000000
        bits = b"\x07\x80"
        reader = HuffmanReader(helpers.get_named_file(bits))

        # [1]0000000
        result = reader.next_bit
        self.assertIs(bool, type(result))
        self.assertTrue(result)

        # 1[0]000000
        result = reader.next_bit
        self.assertIsNone(result)


class TestLempelZivReader(unittest.TestCase):
    def test_next_literal_returns_byte(self):
        data = b"\xAA\xFF"
        reader = LempelZivReader(helpers.get_named_file(data))

        result = reader.next_literal
        self.assertIsInstance(result, bytes)

    def test_next_token_returns_Codeword(self):
        data = randbytes((N_BITS*2) // 8)
        reader = LempelZivReader(helpers.get_named_file(data))

        result = reader.next_token
        self.assertIsInstance(result, Codeword)

    def test_next_token_returns_none_at_end_of_stream(self):
        data = b"\xFF"
        reader = LempelZivReader(helpers.get_named_file(data*2))

        control = reader.next_bit
        result = reader.next_token
        self.assertIsNotNone(control)
        self.assertIsNone(result)


class TestHuffmanWriter(unittest.TestCase):
    def test_write_to_prefixes_file_with_padding_length(self):
        with helpers.get_empty_file() as output_file:
            bit = True
            remainders = range(7, -1, -1)
            writer = HuffmanWriter()
            j = 0
            for i in remainders:
                j += 2**i
                writer.bit(bit)
                with helpers.get_empty_file() as output_file:
                    writer.write_to(output_file)
                    output_file.seek(0)

                    expectation = int.to_bytes(i) + int.to_bytes(j)
                    result = output_file.read()
                    self.assertSequenceEqual(result, expectation)

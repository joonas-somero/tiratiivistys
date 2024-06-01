import unittest

from tiratiivistys.constants import MAX_OFFSET
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
        data = b'\xAB\xCD\x00'
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

                    expectation = i.to_bytes() + j.to_bytes()
                    result = output_file.read()
                    self.assertSequenceEqual(result, expectation)


class TestLempelZivWriter(unittest.TestCase):
    def test_token_writes_codeword_as_offset_length_pair(self):
        with helpers.get_empty_file() as output_file:
            codeword = Codeword(MAX_OFFSET//5, MAX_OFFSET//3)

            writer = LempelZivWriter()
            writer.token(codeword)
            writer.write_to(output_file)
            output_file.seek(0)

            expectation = helpers.codeword_to_bytes(codeword)
            result = output_file.read()
            self.assertSequenceEqual(result, expectation)

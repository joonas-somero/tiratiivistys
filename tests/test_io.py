import unittest

from tiratiivistys.constants import BIT_WIDTH
from tiratiivistys.huffman.io import HuffmanReader, HuffmanWriter
from tiratiivistys.lempel_ziv.io import LZWReader, LZWWriter
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


class TestLZWReader(unittest.TestCase):
    def test_next_codeword_returns_int(self):
        data = b"\xFF" * helpers.get_min_bytes(BIT_WIDTH)
        reader = LZWReader(helpers.get_named_file(data))

        result = reader.next_codeword
        self.assertIsInstance(result, int)
        self.assertEqual(result, helpers.get_max_int(BIT_WIDTH))

    def test_next_codeword_returns_none_at_end_of_stream(self):
        data = b"\xFF" * helpers.get_min_bytes(BIT_WIDTH)
        reader = LZWReader(helpers.get_named_file(data))

        control = reader.next_byte
        result = reader.next_codeword
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


class TestLZWWriter(unittest.TestCase):
    def test_codeword_writes_codeword_of_bit_width(self):
        with helpers.get_empty_file() as output_file:
            data = helpers.get_max_int(BIT_WIDTH)

            writer = LZWWriter()
            writer.codeword(data)
            writer.write_to(output_file)
            output_file.seek(0)

            expectation = helpers.get_padded_bytes(BIT_WIDTH)
            result = output_file.read()
            self.assertSequenceEqual(result, expectation)

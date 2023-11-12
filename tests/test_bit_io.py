import unittest
from tempfile import NamedTemporaryFile, TemporaryFile

from tiratiivistys.classes import Codeword
from tiratiivistys.bit_io import BitReader, BitWriter
from tests import helpers


class TestBitReader(unittest.TestCase):
    def test_next_bit_returns_next_bit_as_bool(self):
        # 10000000
        bits = b"\x80"
        reader = BitReader(helpers.get_named_file(bits))

        # [1]0000000
        result = reader.next_bit
        self.assertIs(bool, type(result))
        self.assertTrue(result)

        # 1[0]000000
        result = reader.next_bit
        self.assertIs(bool, type(result))
        self.assertFalse(result)

    def test_next_byte_returns_next_byte_as_bytes(self):
        # 1010101011111111
        bits = b"\xAA\xFF"
        reader = BitReader(helpers.get_named_file(bits))

        # 1[01010101]1111111
        result = reader.next_bit and reader.next_byte
        self.assertIs(bytes, type(result))
        self.assertEqual(b"\x55", result)

    def test_reader_props_return_none_at_end_of_stream(self):
        # 11111111
        bits = b"\xFF"
        reader_b = BitReader(helpers.get_named_file(bits))
        reader_B = BitReader(helpers.get_named_file(bits))

        # 11111111[_]
        control_b = reader_b.next_byte
        result_b = reader_b.next_bit
        self.assertIsNotNone(control_b)
        self.assertIsNone(result_b)

        # 1[1111111_]
        control_B = reader_B.next_bit
        result_B = reader_B.next_byte
        self.assertIsNotNone(control_B)
        self.assertIsNone(result_B)


class TestBitWriter(unittest.TestCase):
    def test_bit_writes_bool_as_a_bit(self):
        with helpers.get_empty_file() as output_file:
            bit = True
            writer = BitWriter()

            writer.bit(bit)
            writer.write_to(output_file)
            output_file.seek(0)

            self.assertSequenceEqual(output_file.read(), b"\x80")

    def test_byte_writes_byte(self):
        with helpers.get_empty_file() as output_file:
            byte = b"\x55"
            writer = BitWriter()

            writer.byte(byte)
            writer.write_to(output_file)
            output_file.seek(0)

            self.assertSequenceEqual(output_file.read(), b"\x55")

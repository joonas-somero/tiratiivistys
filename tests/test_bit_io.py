import unittest
from tempfile import NamedTemporaryFile, TemporaryFile

from tiratiivistys.bit_io import BitReader, BitWriter


class TestBitReader(unittest.TestCase):
    def setUp(self):
        self.tempfiles = []

        def get_file(content):
            fp = NamedTemporaryFile()
            fp.write(content)
            fp.seek(0)
            self.tempfiles.append(fp)
            return fp

        self.named_file = lambda content: get_file(content)

    def test_bit_returns_next_bit_as_bool(self):
        # 10000000
        bits = b"\x80"
        reader = BitReader(self.named_file(bits))

        # [1]0000000
        result = reader.bit
        self.assertIs(bool, type(result))
        self.assertTrue(result)

        # 1[0]000000
        result = reader.bit
        self.assertIs(bool, type(result))
        self.assertFalse(result)

    def test_literal_returns_next_literal_as_bytes(self):
        # 1010101011111111
        bits = b"\xAA\xFF"
        reader = BitReader(self.named_file(bits))

        # 1[01010101]1111111
        result = reader.bit and reader.literal
        self.assertIs(bytes, type(result))
        self.assertEqual(b"\x55", result)

    def test_token_returns_next_three_bytes_as_bytes(self):
        # 10000000101010101111111110101010
        bits = b"\x80\xAA\xFF\xAA"
        reader = BitReader(self.named_file(bits))

        # 1[000000010101010111111111]0101010
        result = reader.bit and reader.token
        self.assertIs(bytes, type(result))
        self.assertEqual(b"\x01\x55\xFF", result)

    def test_reader_props_return_none_at_end_of_stream(self):
        # 11111111
        bits = b"\xFF"
        reader_b = BitReader(self.named_file(bits))
        reader_l = BitReader(self.named_file(bits))
        reader_t = BitReader(self.named_file(bits*3))

        # 11111111[_]
        control_b = reader_b.literal
        result_b = reader_b.bit
        self.assertIsNotNone(control_b)
        self.assertIsNone(result_b)

        # 1[1111111_]
        control_l = reader_l.bit
        result_l = reader_l.literal
        self.assertIsNotNone(control_l)
        self.assertIsNone(result_l)

        # 1[1111111 11111111 11111111_]
        control_t = reader_t.bit
        result_t = reader_t.token
        self.assertIsNotNone(control_t)
        self.assertIsNone(result_t)

    def test_reader_with_explicit_padding(self):
        # 10000000
        bits = b"\x07\x80"
        reader = BitReader(self.named_file(bits), True)

        # [1]0000000
        result = reader.bit
        self.assertIs(bool, type(result))
        self.assertTrue(result)

        # 1[0]000000
        result = reader.bit
        self.assertIsNone(result)

    def tearDown(self):
        for fp in self.tempfiles:
            fp.close()


class TestBitWriter(unittest.TestCase):
    def setUp(self):
        self.output_file = lambda: TemporaryFile()

    def test_bit_writes_bool_as_a_bit(self):
        with self.output_file() as of:
            bit = True
            writer = BitWriter()

            writer.bit(bit)
            writer.write_to(of)
            of.seek(0)

            self.assertSequenceEqual(of.read(), b"\x80")

    def test_byte_writes_byte(self):
        with self.output_file() as of:
            byte = b"\x55"
            writer = BitWriter()

            writer.byte(byte)
            writer.write_to(of)
            of.seek(0)

            self.assertSequenceEqual(of.read(), b"\x55")

    def test_token_writes_token_as_three_bytes(self):
        with self.output_file() as of:
            token = b"\x80\xFF\xAA"
            writer = BitWriter()

            writer.token(token)
            writer.write_to(of)
            of.seek(0)

            self.assertSequenceEqual(of.read(), b"\x80\xFF\xAA")

    def test_write_to_prefixes_file_with_padding_length(self):
        with self.output_file() as of:
            bit = True
            remainders = range(7, -1, -1)
            writer = BitWriter()
            j = 0
            for i in remainders:
                j += 2**i
                writer.bit(bit)
                with self.output_file() as of:
                    writer.write_to(of, True)
                    of.seek(0)

                    expectation = int.to_bytes(i) + int.to_bytes(j)
                    result = of.read()
                    self.assertSequenceEqual(result, expectation)

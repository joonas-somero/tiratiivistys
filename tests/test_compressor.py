import unittest
from tempfile import TemporaryFile, NamedTemporaryFile

from tiratiivistys import huffman, lempel_ziv
from tiratiivistys.compressor import Compressor


class TestCompressor(unittest.TestCase):
    def setUp(self):
        def get_file(filetype, content):
            tf = filetype()
            tf.write(content)
            tf.seek(0)
            return tf
        self.__input_file = lambda c: get_file(TemporaryFile, c)
        self.__compressed_file = lambda c: get_file(NamedTemporaryFile, c)
        self.__output_file = lambda: TemporaryFile()

    def test_compressor_encodes_appropriate_bytes_with_Huffman(self):
        data = b"ABBCCC"
        input_file = self.__input_file(data)
        output_file = self.__output_file()

        comp = Compressor(huffman.Encoder, input_file, output_file)
        comp.deploy()
        output_file.seek(0)

        result = output_file.read()
        # padding length: 00000010
        # branch C:       0 1 01000011
        # branch A:       0 1 01000001
        # branch B:       1 01000010
        # data ABBCCC:    101111000
        # padding         00
        expectation = b"\x02P\xd4\x1a\x15\xe0"
        self.assertSequenceEqual(result, expectation)

    def test_compressor_decodes_appropriate_bytes_with_huffman(self):
        data = b"\x02P\xd4\x1a\x15\xe0"
        compressed_file = self.__compressed_file(data)
        restored_file = self.__output_file()

        comp = Compressor(huffman.Decoder, compressed_file, restored_file)
        comp.deploy()
        restored_file.seek(0)

        result = restored_file.read()
        expectation = b"ABBCCC"
        self.assertSequenceEqual(result, expectation)

    def test_compressor_encodes_appropriate_literals_with_lempel_ziv(self):
        data = b"ABC"
        input_file = self.__input_file(data)
        output_file = self.__output_file()

        comp = Compressor(lempel_ziv.Encoder, input_file, output_file)
        comp.deploy()
        output_file.seek(0)

        result = output_file.read()
        # 0 01000001 0 01000010 0 01000011 (00000)
        expectation = b" \x90\x88`"
        self.assertSequenceEqual(result, expectation)

    def test_compressor_encodes_appropriate_tokens_with_lempel_ziv(self):
        data = b"ABCABCD"
        input_file = self.__input_file(data)
        output_file = self.__output_file()

        comp = Compressor(lempel_ziv.Encoder, input_file, output_file)
        comp.deploy()
        output_file.seek(0)

        result = output_file.read()
        # 0 01000001 0 01000010 0 01000011 1 00000011 00000011 01000100 (0000)
        expectation = b" \x90\x88p04@"
        self.assertSequenceEqual(result, expectation)

    def test_compressor_decodes_appropriate_bytes_with_lempel_ziv(self):
        data = b" \x90\x88p04@"
        compressed_file = self.__compressed_file(data)
        restored_file = self.__output_file()

        comp = Compressor(lempel_ziv.Decoder, compressed_file, restored_file)
        comp.deploy()
        restored_file.seek(0)

        result = restored_file.read()
        expectation = b"ABCABCD"
        self.assertSequenceEqual(result, expectation)

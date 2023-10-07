import unittest
from tempfile import TemporaryFile
from random import randbytes
from tiratiivistys.lempel_ziv import LempelZiv


class TestLempelZiv(unittest.TestCase):
    def setUp(self):
        mebibyte = randbytes(2**20)
        self.original_data = mebibyte
        self.compressed_file = TemporaryFile("wb+")
        with TemporaryFile("wb+") as original_file:
            original_file.write(self.original_data)
            original_file.seek(0)
            for byte in LempelZiv.compress(original_file):
                self.compressed_file.write(byte)
            self.compressed_file.seek(0)

    def test_restore(self):
        original = (int.to_bytes(x) for x in self.original_data)
        restored = LempelZiv.restore(self.compressed_file)
        comparison = zip(original, restored)
        self.assertTrue(all(t == r for t, r in comparison))

    def tearDown(self):
        self.compressed_file.close()

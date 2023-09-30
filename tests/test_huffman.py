import unittest
import tempfile
from random import randbytes
from tiratiivistys.huffman import Huffman


class TestHuffman(unittest.TestCase):
    def test_count_occurrences_returns_correct_total(self):
        exp = 20
        n = 1024*1024
        content = randbytes(n)

        file = tempfile.TemporaryFile()
        file.write(content)
        file.seek(0)

        _, total = Huffman.count_occurrences(file)

        file.close()

        self.assertEqual(total, n)

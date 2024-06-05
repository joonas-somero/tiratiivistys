import unittest

from tiratiivistys.lempel_ziv.dictionary import LZWDictionary


class TestLZWDictionary(unittest.TestCase):
    def test_dictionary_is_initialized_with_every_single_character_code(self):
        dictionary = LZWDictionary()
        for i in range(2**8):
            self.assertEqual(dictionary[i], i.to_bytes())

    def test_dictionary_accepts_no_entries_when_full(self):
        pass
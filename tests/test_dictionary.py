import unittest

from tiratiivistys.lempel_ziv.dictionary import LZWDictionary
from tiratiivistys.constants import BIT_WIDTH
from tests import helpers


class TestLZWDictionary(unittest.TestCase):
    def test_dictionary_is_initialized_with_every_single_character_code(self):
        dictionary = LZWDictionary()
        for i in range(2**8):
            self.assertEqual(dictionary[i], i.to_bytes())

    def test_dictionary_membership_testing(self):
        dictionary = LZWDictionary()
        first_item = b"\x00"
        last_item = b"\xFF"
        not_item = int.from_bytes(last_item) + 1

        first_result = first_item in dictionary
        last_result = last_item in dictionary
        not_result = not_item in dictionary

        self.assertTrue(first_result)
        self.assertTrue(last_result)
        self.assertFalse(not_result)

    def test_dictionary_lookup(self):
        dictionary = LZWDictionary()
        first_item = b"\x00"
        last_item = b"\xFF"
        not_item = int.from_bytes(last_item) + 1

        first_result = dictionary.index(first_item)
        last_result = dictionary.index(last_item)
        with self.assertRaises(ValueError):
            dictionary.index(not_item)

    def test_dictionary_silently_rejects_entries_when_full(self):
        dictionary = LZWDictionary()
        start = 2**8
        stop = 2**BIT_WIDTH
        for i in helpers.get_byte_range(start, stop):
            dictionary.add(i)

        control = dictionary[None]
        self.assertIsNone(control)
        control = dictionary[helpers.get_max_int(BIT_WIDTH)]
        self.assertIsNotNone(control)
        with self.assertRaises(IndexError):
            control = dictionary[2**BIT_WIDTH]

        one_more_byte = helpers.get_bytes(2**BIT_WIDTH)
        dictionary.add(one_more_byte)
        with self.assertRaises(IndexError):
            result = dictionary[2**BIT_WIDTH]

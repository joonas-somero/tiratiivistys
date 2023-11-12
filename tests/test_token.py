import unittest
from random import randbytes
from string import ascii_lowercase

from tiratiivistys.classes import Codeword
from tiratiivistys.lempel_ziv.token import LempelZivToken


class TestLempelZivToken(unittest.TestCase):
    def setUp(self):
        data_bytes = bytes(ascii_lowercase, encoding="utf8")
        start, history, buffer = (8,
                                  data_bytes[:16],
                                  data_bytes[8:])

        # History:      abcdefghijklmnop
        # Buffer:                       ijklmnopqrstuvwxyz
        # Frame:                        ijklmnop
        self.is_match = (start, data_bytes[8:16], history, buffer)
        # History:      abcdefghijklmnop
        # Buffer:                       ijklmnopqrstuvwxyz
        # Frame:                        notmatch
        self.not_match = (start, b"notmatch", history, buffer)

    def test_encode_returns_appropriate_object_if_frame_matches(self):
        expectation = LempelZivToken(8, 8)
        result = LempelZivToken.encode(*self.is_match)
        self.assertIsInstance(result, LempelZivToken)
        self.assertSequenceEqual(result.codeword, expectation.codeword)

    def test_encode_returns_none_if_frame_does_not_match(self):
        result = LempelZivToken.encode(*self.not_match)
        self.assertIsNone(result)

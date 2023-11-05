import unittest
from random import randbytes
from string import ascii_lowercase

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

    def test_literal_returns_appropriate_object(self):
        byte = randbytes(1)
        character = int.from_bytes(byte)

        expectation = b"\x00\x00" + byte
        result = LempelZivToken.literal(character)
        self.assertIsInstance(result, LempelZivToken)
        self.assertSequenceEqual(bytes(result), expectation)

    def test_decode_returns_appropriate_object(self):
        codeword = randbytes(3)

        result = LempelZivToken.decode(codeword)
        self.assertIsInstance(result, LempelZivToken)
        self.assertSequenceEqual(bytes(result), codeword)

    def test_decode_returns_none_for_inaproppriate_codeword_length(self):
        too_long = randbytes(4)
        too_short = randbytes(2)
        just_right = randbytes(3)

        result_s = LempelZivToken.decode(too_short)
        self.assertIsNone(result_s)
        result_l = LempelZivToken.decode(too_long)
        self.assertIsNone(result_l)
        result_ok = LempelZivToken.decode(just_right)
        self.assertIsNotNone(result_ok)
        self.assertIsInstance(result_ok, LempelZivToken)

    def test_encode_returns_appropriate_object_if_frame_matches(self):
        expectation = LempelZivToken(8, 8, 113)
        result = LempelZivToken.encode(*self.is_match)
        self.assertIsInstance(result, LempelZivToken)
        self.assertSequenceEqual(bytes(result), bytes(expectation))

    def test_encode_returns_none_if_frame_does_not_match(self):
        result = LempelZivToken.encode(*self.not_match)
        self.assertIsNone(result)

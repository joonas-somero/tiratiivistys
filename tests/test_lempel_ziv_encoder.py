import unittest
from string import ascii_lowercase
from tiratiivistys.lempel_ziv.encoder import EncodedRange


class TestEncodedRange(unittest.TestCase):
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
        expectation = EncodedRange(0, 0, 99)
        character = int.from_bytes(b"c")
        result = EncodedRange.literal(character)

        self.assertIsInstance(result, EncodedRange)
        self.assertEqual(bytes(result), bytes(expectation))

    def test_decode_returns_appropriate_object(self):
        expectation = EncodedRange(4, 2, 99)
        codeword = b"\x04\x02c"
        result = EncodedRange.decode(codeword)

        self.assertIsInstance(result, EncodedRange)
        self.assertEqual(bytes(result), bytes(expectation))

    def test_decode_returns_none_for_wrong_codeword_length(self):
        shorter = b"\x04\x02"
        result_s = EncodedRange.decode(shorter)
        longer = b"c\x04\x02c"
        result_l = EncodedRange.decode(longer)

        self.assertIsNone(result_s)
        self.assertIsNone(result_l)

    def test_encode_returns_appropriate_object_if_frame_matches(self):
        expectation = EncodedRange(8, 8, 113)
        result = EncodedRange.encode(*self.is_match)

        self.assertIsInstance(result, EncodedRange)
        self.assertEqual(bytes(result), bytes(expectation))

    def test_encode_returns_none_if_frame_does_not_match(self):
        result = EncodedRange.encode(*self.not_match)

        self.assertIsNone(result)

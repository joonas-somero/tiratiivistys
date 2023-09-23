import unittest
import tempfile
from unittest.mock import Mock, PropertyMock, patch
from tiratiivistys.lempel_ziv.window \
    import EncodedRange, SearchWindow, SlidingWindow


class TestEncodedRange(unittest.TestCase):
    def test_encode_returns_appropriate_object(self):
        character = int.from_bytes(b'c')
        offset = 0
        length = 0

        expectation = EncodedRange(character)
        result = EncodedRange.encode(character, offset, length)

        self.assertIsInstance(result, EncodedRange)
        self.assertEqual(bytes(result), bytes(expectation))

import unittest
import tempfile
from unittest.mock import Mock, PropertyMock, patch
from tiratiivistys.lempel_ziv.window \
    import EncodedRange, SearchWindow, SlidingWindow


class TestEncodedRange(unittest.TestCase):
    def test_encode_returns_appropriate_object(self):
        character = int.from_bytes(b'c')
        offset = length = 2

        start = 0
        frame = b'ab'
        history = b'ab'
        buffer = b'abc'

        expectation = EncodedRange(character)
        expectation.offset = offset
        expectation.length = length

        result = EncodedRange.encode(start, frame, history, buffer)

        self.assertIsInstance(result, EncodedRange)
        self.assertEqual(bytes(result), bytes(expectation))

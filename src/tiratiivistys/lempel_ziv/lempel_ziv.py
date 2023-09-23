from typing import BinaryIO
from .window import EncodedRange, SearchWindow, SlidingWindow


class LempelZiv:
    """An interface to compress and restore files using the LZ77 algorithm."""

    @classmethod
    def compress(cls, file: BinaryIO) -> None:
        search_window = SearchWindow(file, EncodedRange)
        sliding_window = SlidingWindow(search_window)
        for x in sliding_window.encoder:
            x

    @classmethod
    def restore(cls, file: BinaryIO) -> None:
        pass

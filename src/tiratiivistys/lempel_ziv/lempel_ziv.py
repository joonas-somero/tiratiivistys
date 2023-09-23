from .window import EncodedRange, SearchWindow, SlidingWindow


class LempelZiv:
    """An interface to compress and restore files using the LZ77 algorithm."""

    @classmethod
    def compress(cls, file) -> None:
        search_window = SearchWindow(file)
        sliding_window = SlidingWindow(search_window, EncodedRange.encode)
        for x in sliding_window.encoder:
            x

    @classmethod
    def restore(cls, file) -> None:
        pass

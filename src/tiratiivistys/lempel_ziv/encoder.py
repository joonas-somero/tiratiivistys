from typing import Any, Generator, BinaryIO
from tiratiivistys.classes import Encoder
from tiratiivistys.lempel_ziv.encoded_range import EncodedRange
from tiratiivistys.lempel_ziv.window import SlidingWindow


class LempelZivEncoder(Encoder):
    def __init__(self, file: BinaryIO) -> None:
        self.__input = file
        self.__window = SlidingWindow(file, EncodedRange)

    @property
    def encoder(self) -> Generator:
        window = self.__window
        while window.has_input:
            match = window.match
            window.slide(match.length+1)
            yield bytes(match)

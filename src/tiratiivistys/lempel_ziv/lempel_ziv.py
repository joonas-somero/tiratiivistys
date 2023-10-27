from typing import BinaryIO, Generator
from tiratiivistys.classes import Compressor
from .encoded_range import EncodedRange
from .window import SlidingWindow, CodeWordWindow
from .encoder import LempelZivEncoder as Encoder
from .decoder import LempelZivDecoder as Decoder


class LempelZiv(Compressor):
    """An interface to compress and restore files using the LZ77 algorithm."""
    @staticmethod
    def compress(file: BinaryIO) -> Generator:
        window = SlidingWindow(file, EncodedRange)
        return Encoder(window).encoder

    @staticmethod
    def restore(file: BinaryIO) -> Generator:
        window = CodeWordWindow(file, EncodedRange)
        return Decoder(window).decoder

from typing import Final, BinaryIO, Generator
from tiratiivistys.classes import Compressor
from .encoded_range import EncodedRange
from .window import SlidingWindow, CodeWordWindow
from .encoder import LempelZivEncoder
from .decoder import LempelZivDecoder


class LempelZiv(Compressor):
    """An interface to compress and restore files using the LZ77 algorithm."""
    @staticmethod
    def get_file_encoder(file: BinaryIO) -> Generator:
        window = SlidingWindow(file, EncodedRange)
        return LempelZivEncoder(window).encoder

    @staticmethod
    def get_file_decoder(file: BinaryIO) -> Generator:
        window = CodeWordWindow(file, EncodedRange)
        return LempelZivDecoder(window).decoder

    @classmethod
    def compress(cls, file: BinaryIO) -> Generator:
        return cls.get_file_encoder(file)

    @classmethod
    def restore(cls, file: BinaryIO) -> Generator:
        return cls.get_file_decoder(file)

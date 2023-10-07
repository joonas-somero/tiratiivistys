from typing import Final, BinaryIO, Any
from tiratiivistys.classes import Compressor
from tiratiivistys.constants import EXTENSIONS
from .encoder import LempelZivEncoder
from .decoder import LempelZivDecoder


class LempelZiv(Compressor):
    """An interface to compress and restore files using the LZ77 algorithm."""
    @staticmethod
    def get_file_encoder(file):
        return LempelZivEncoder(file).encoder

    @staticmethod
    def get_file_decoder(file):
        return LempelZivDecoder(file).decoder

    @classmethod
    def compress(cls, file: BinaryIO) -> bytes:
        return cls.get_file_encoder(file)

    @classmethod
    def restore(cls, file: BinaryIO) -> bytes:
        return cls.get_file_decoder(file)

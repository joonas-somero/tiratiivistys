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
    def compress(cls, file: BinaryIO) -> None:
        encoder = cls.get_file_encoder(file)
        filename = file.name + EXTENSIONS['lempel-ziv']
        with open(filename, "wb") as compressed_file:
            for codeword in encoder:
                compressed_file.write(codeword)

    @classmethod
    def restore(cls, file: BinaryIO) -> None:
        pass

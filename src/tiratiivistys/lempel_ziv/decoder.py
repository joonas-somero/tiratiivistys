from typing import Self, Any, Generator, BinaryIO
from tiratiivistys.classes import Decoder
from tiratiivistys.lempel_ziv.encoded_range import EncodedRange
from tiratiivistys.lempel_ziv.window import CodeWordWindow


class LempelZivDecoder(Decoder):
    def __init__(self, file: BinaryIO) -> None:
        self.__input = file
        self.__window = CodeWordWindow(file, EncodedRange)

    @property
    def decoder(self) -> Generator:
        window = self.__window
        for character in window.characters:
            yield int.to_bytes(character)

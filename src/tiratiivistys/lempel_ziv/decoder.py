from typing import BinaryIO, Generator, Callable

from tiratiivistys.classes import Model
from tiratiivistys.bit_io import BitReader as Reader
from tiratiivistys.lempel_ziv.window import TokenWindow as Window
from tiratiivistys.lempel_ziv.token import LempelZivToken as Token


class LempelZivDecoder(Model):
    def __init__(self, compressed_file: BinaryIO) -> None:
        self.__compressed_file = compressed_file

    @property
    def __data(self) -> Generator[bytes, None, None]:
        reader = Reader(self.__compressed_file)
        while (prefix := reader.bit) is not None:
            input_bytes = (reader.token
                           if prefix
                           else reader.literal)
            input_bytes and (yield input_bytes)

    @property
    def __decoded(self) -> Generator[int, None, None]:
        window = Window(self.__data, Token)
        return window.output

    def __to_file(self, output_file: BinaryIO) -> None:
        for character in self.__decoded:
            output_file.write(int.to_bytes(character))

    @property
    def executor(self) -> Callable[[BinaryIO], None]:
        return lambda f: self.__to_file(f)

from typing import BinaryIO, Generator, Callable

from tiratiivistys.classes import Model
from tiratiivistys.lempel_ziv.io import LempelZivReader as Reader
from tiratiivistys.lempel_ziv.window import TokenWindow as Window
from tiratiivistys.lempel_ziv.token import LempelZivToken as Token


class LempelZivDecoder(Model):
    def __init__(self, compressed_file: BinaryIO) -> None:
        self.__compressed_file = compressed_file

    @property
    def __data(self) -> Generator[bytes, None, None]:
        reader = Reader(self.__compressed_file)
        while (prefix := reader.next_bit) is not None:
            result = (reader.next_token
                      if prefix
                      else reader.next_literal)
            result is not None and (yield result)

    @property
    def __decoded(self) -> Generator[int, None, None]:
        window = Window(self.__data, Token)
        return window.output

    def __to_file(self, output_file: BinaryIO) -> None:
        for character in self.__decoded:
            output_file.write(character)

    @property
    def executor(self) -> Callable[[BinaryIO], None]:
        return lambda f: self.__to_file(f)

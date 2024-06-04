from typing import BinaryIO, Callable

from tiratiivistys.classes import Model
from tiratiivistys.lempel_ziv.io import LZWWriter as Writer
from tiratiivistys.lempel_ziv.dictionary import LZWDictionary as Dictionary


class LZWEncoder(Model):
    def __init__(self, input_file: BinaryIO) -> None:
        self.__input_file = input_file
        self.__writer = Writer()

    def __encode(self):
        dictionary = Dictionary()
        input_bytes = self.__input_file.read(1)
        while next_byte := self.__input_file.read(1):
            if input_bytes + next_byte in dictionary:
                input_bytes += next_byte
            else:
                self.__writer.codeword(dictionary.index(input_bytes))
                dictionary.add(input_bytes + next_byte)
                input_bytes = next_byte
        self.__writer.codeword(dictionary.index(input_bytes))

    def __to_file(self, output_file: BinaryIO) -> None:
        self.__writer.write_to(output_file)

    @property
    def executor(self) -> Callable[[BinaryIO], None]:
        self.__encode()
        return lambda f: self.__to_file(f)

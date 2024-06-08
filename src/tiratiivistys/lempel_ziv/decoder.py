from typing import BinaryIO, Generator, Callable

from tiratiivistys.classes import Model
from tiratiivistys.lempel_ziv.io import LZWReader as Reader
from tiratiivistys.lempel_ziv.dictionary import LZWDictionary as Dictionary


class LZWDecoder(Model):
    def __init__(self, compressed_file: BinaryIO) -> None:
        self.__compressed_file = compressed_file

    @property
    def __decoded(self) -> Generator[bytes, None, None]:
        def get_first_byte(bs):
            return b"%c" % bs[0]

        dictionary = Dictionary()
        reader = Reader(self.__compressed_file)

        codeword = reader.next_codeword
        output_bytes = dictionary[codeword]
        yield output_bytes

        while (codeword := reader.next_codeword) is not None:
            if decoded_word := dictionary[codeword]:
                dictionary.add(output_bytes + get_first_byte(decoded_word))
                output_bytes = decoded_word
            else:
                dictionary.add(output_bytes + get_first_byte(output_bytes))
            yield output_bytes

    def __to_file(self, output_file: BinaryIO) -> None:
        for character in self.__decoded:
            if character is not None:
                output_file.write(character)

    @property
    def executor(self) -> Callable[[BinaryIO], None]:
        return lambda f: self.__to_file(f)

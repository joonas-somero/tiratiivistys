from typing import BinaryIO, Callable
from tiratiivistys.classes import Model
from tiratiivistys.bit_io import BitWriter
from tiratiivistys.lempel_ziv.window import SlidingWindow as Window
from tiratiivistys.lempel_ziv.token import LempelZivToken as Token


class LempelZivEncoder(Model):
    def __init__(self, input_file: BinaryIO) -> None:
        self.__input_file = input_file
        self.__writer = BitWriter()

    def __encode(self):
        window = Window(self.__input_file, Token)
        for match in window.output:
            self.__writer.bit(match.is_token)
            if match.is_token:
                self.__writer.token(bytes(match))
            else:
                self.__writer.byte(int.to_bytes(match.character))

    def __to_file(self, output_file: BinaryIO) -> None:
        self.__writer.write_to(output_file)

    @property
    def executor(self) -> Callable[[BinaryIO], None]:
        self.__encode()
        return lambda f: self.__to_file(f)

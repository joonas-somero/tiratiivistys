from typing import BinaryIO

from bitstring import ConstBitStream, BitArray, Bits
from bitstring.exceptions import ReadError

from tiratiivistys.classes import Reader, Writer
from tiratiivistys.constants import TOKEN_LENGTH, LITERAL_LENGTH


class BitReader(Reader):
    def __init__(self,
                 input_file: BinaryIO,
                 padded: bool | None = False) -> None:
        padding, offset = ((None, None)
                           if not padded
                           else (int.from_bytes(input_file.read(1)), 8))
        self.__stream = ConstBitStream(filename=input_file.name,
                                       offset=offset)
        self.__max_pos = (len(self.__stream)
                          if not padded
                          else len(self.__stream) - padding)

    @property
    def __pos(self):
        return self.__stream.pos

    def __read(self, fmt: str) -> bool | bytes | None:
        try:
            value = self.__stream.read(fmt)
            if self.__pos > self.__max_pos:
                raise ReadError
            return value
        except ReadError:
            return None

    @property
    def bit(self) -> bool | None:
        return self.__read("bool")

    @property
    def literal(self) -> bytes | None:
        return self.__read(f"bytes:{LITERAL_LENGTH}")

    @property
    def token(self) -> bytes | None:
        return self.__read(f"bytes:{TOKEN_LENGTH}")


class BitWriter(Writer):
    def __init__(self) -> None:
        self.__buffer = BitArray()

    @property
    def __padding(self) -> int:
        remainder = len(self.__buffer) % 8
        padding_length = (8 - remainder) % 8
        return int.to_bytes(padding_length)

    def write_to(self,
                 output_file: BinaryIO,
                 padded: bool | None = False) -> None:
        """Writes the contents of the buffer into 'output_file'. If
        'padded' is True, the first byte will contain the length of the
        padding. Regardless, if stream is not byte-aligned, padding is
        appended to the file.

        Positional arguments:
            output_file: A writable binary I/O stream.
            padded: Boolean (defaults to False)
        """
        if padded:
            output_file.write(self.__padding)
        self.__buffer.tofile(output_file)

    def bit(self, bit: bool) -> None:
        self.__buffer.append(Bits(bool=bit))

    def byte(self, byte: bytes) -> None:
        self.__buffer.append(Bits(bytes=byte))

    def token(self, token: bytes) -> None:
        self.__buffer.append(Bits(bytes=token))

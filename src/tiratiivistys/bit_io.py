from typing import BinaryIO, Callable

from bitstring import ConstBitStream, BitArray
from bitstring.exceptions import ReadError

from tiratiivistys.classes import Reader, Writer


class BitReader(Reader):
    def __init__(self, input_file: BinaryIO, offset: int = 0) -> None:
        self._stream = ConstBitStream(filename=input_file.name,
                                      offset=offset)
        self._max_pos = len(self._stream)

    def _read(self, fmt: str) -> bool | bytes | int | None:
        try:
            if self._stream.pos >= self._max_pos:
                raise ReadError
            return self._stream.read(fmt)
        except ReadError:
            return None

    @property
    def next_bit(self) -> bool | None:
        return self._read("bool")

    @property
    def next_byte(self) -> bytes | None:
        return self._read("bytes1")


class BitWriter(Writer):
    def __init__(self) -> None:
        self._buffer = BitArray()

    def write_to(self, output_file: BinaryIO) -> None:
        self._buffer.tofile(output_file)

    def bit(self, bit: bool) -> None:
        self._buffer.append([bit])

    def byte(self, byte: bytes) -> None:
        self._buffer.append(byte[0:1])

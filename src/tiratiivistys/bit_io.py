from typing import BinaryIO, Callable

from bitstring import ConstBitStream, BitArray
from bitstring.exceptions import ReadError

from tiratiivistys.classes import Codeword, Reader, Writer


class BitReader(Reader):
    def __init__(self, input_file: BinaryIO, offset: int = 0) -> None:
        self._stream = ConstBitStream(filename=input_file.name,
                                      offset=offset)
        self._max_pos = len(self._stream)

    def _read(self,
              method: type(ConstBitStream.read)
              | type(ConstBitStream.readlist),
              fmt: str | list[str]) -> bool | bytes | Codeword | None:
        try:
            if self._stream.pos >= self._max_pos:
                raise ReadError
            return method(fmt)
        except ReadError:
            return None

    @property
    def next_bit(self) -> bool | None:
        method = self._stream.read
        fmt = "bool"
        return self._read(method, fmt)

    @property
    def next_byte(self) -> bytes | None:
        method = self._stream.read
        fmt = "bytes:1"
        return self._read(method, fmt)


class BitWriter(Writer):
    def __init__(self) -> None:
        self._buffer = BitArray()

    def write_to(self, output_file: BinaryIO) -> None:
        self._buffer.tofile(output_file)

    def bit(self, bit: bool) -> None:
        self._buffer.append([bit])

    def byte(self, byte: bytes) -> None:
        self._buffer.append(byte[0:1])

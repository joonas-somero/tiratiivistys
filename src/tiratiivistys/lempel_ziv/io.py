from bitstring import Bits

from tiratiivistys.constants import BIT_WIDTH
from tiratiivistys.bit_io import BitReader, BitWriter


class LZWReader(BitReader):
    @property
    def next_codeword(self) -> int | None:
        fmt = f"uint{BIT_WIDTH}"
        return self._read(fmt)


class LZWWriter(BitWriter):
    def codeword(self, codeword: int) -> None:
        initializer = f"uint{BIT_WIDTH}={codeword}"
        self._buffer.append(initializer)

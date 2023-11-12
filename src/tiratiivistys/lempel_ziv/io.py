from bitstring import Bits

from tiratiivistys.constants import N_BITS
from tiratiivistys.classes import Codeword
from tiratiivistys.bit_io import BitReader, BitWriter


class LempelZivReader(BitReader):
    @property
    def next_literal(self) -> bytes | None:
        result = self.next_byte
        return result

    @property
    def next_token(self) -> Codeword | None:
        method = self._stream.readlist
        fmt = [f"uint:{N_BITS}"] * 2
        result = self._read(method, fmt)
        return (result
                if result is None
                else Codeword(*result))


class LempelZivWriter(BitWriter):
    def token(self, codeword: Codeword) -> None:
        def bits(b): return f"uint{N_BITS}={b}"
        self._buffer.append(", ".join([
            bits(codeword.offset),
            bits(codeword.length)
        ]))

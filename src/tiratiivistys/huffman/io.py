from typing import BinaryIO

from tiratiivistys.bit_io import BitReader, BitWriter


class HuffmanReader(BitReader):
    def __init__(self, input_file: BinaryIO) -> None:
        super(HuffmanReader, self).__init__(input_file, 8)
        padding = int.from_bytes(input_file.read(1))
        self._max_pos -= padding


class HuffmanWriter(BitWriter):
    @property
    def __padding(self) -> int:
        remainder = len(self._buffer) % 8
        padding_length = (8 - remainder) % 8
        return int.to_bytes(padding_length)

    def write_to(self, output_file: BinaryIO) -> None:
        output_file.write(self.__padding)
        super(HuffmanWriter, self).write_to(output_file)

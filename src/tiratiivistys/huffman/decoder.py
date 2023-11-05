from typing import BinaryIO, Generator, Callable

from tiratiivistys.classes import Model
from tiratiivistys.bit_io import BitReader as Reader
from tiratiivistys.huffman.tree import HuffmanTree as Tree


class HuffmanDecoder(Model):
    def __init__(self, compressed_file: BinaryIO) -> None:
        self.__compressed_file = compressed_file
        self.__reader = Reader(compressed_file, True)

    @property
    def __decoded(self) -> Generator[bytes, None, None]:
        root = Tree.from_encoded_data(self.__reader).root
        node = root
        while node is not None:
            if node.is_leaf:
                yield node.value
                node = root
            else:
                edge = self.__reader.bit
                node = node.get_child(edge)

    def __to_file(self, output_file: BinaryIO) -> None:
        for byte in self.__decoded:
            output_file.write(byte)

    @property
    def executor(self) -> Callable[[BinaryIO], None]:
        return lambda f: self.__to_file(f)

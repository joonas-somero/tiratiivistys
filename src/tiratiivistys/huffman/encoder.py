from typing import BinaryIO, Callable

from tiratiivistys.classes import Model
from tiratiivistys.huffman.io import HuffmanWriter as Writer
from tiratiivistys.huffman.tree import HuffmanTree as Tree


class HuffmanEncoder(Model):
    def __init__(self, input_file: BinaryIO) -> None:
        self.__input_file = input_file
        self.__tree = Tree.from_input_file(input_file)
        self.__writer = Writer()

    def __encode_tree(self) -> None:
        for node in self.__tree.nodes:
            self.__writer.bit(node.is_leaf)
            node.is_leaf and self.__writer.byte(node.value)

    def __encode_data(self) -> None:
        while byte := self.__input_file.read(1):
            for edge in self.__tree.path_to(byte):
                self.__writer.bit(edge)

    def __to_file(self, output_file: BinaryIO) -> None:
        self.__writer.write_to(output_file)

    @property
    def executor(self) -> Callable[[BinaryIO], None]:
        self.__encode_tree()
        self.__encode_data()
        return lambda f: self.__to_file(f)

from typing import Generator, BinaryIO
from itertools import chain
from tiratiivistys.classes import Encoder, Tree
from collections import deque


class HuffmanEncoder(Encoder):
    def __init__(self, file: BinaryIO, tree: Tree) -> None:
        self.__file = file
        self.__tree = tree

    @property
    def __encoded_tree(self) -> Generator:
        for node, _ in self.__tree.nodes:
            yield (b"1" + node.value
                   if node.is_leaf
                   else b"0")

    @property
    def __encoded_data(self) -> Generator:
        out = ""
        while byte := self.__file.read(1):
            for edge in self.__tree.path_to(byte):
                yield bytes(str(edge), encoding="utf-8")

    @property
    def encoder(self) -> Generator:
        return chain(self.__encoded_tree,
                     self.__encoded_data)

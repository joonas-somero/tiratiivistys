from typing import Generator, BinaryIO
from tiratiivistys.classes import Decoder, Node, Tree


class TreeIterator:
    def __init__(self, file: BinaryIO, root: Node) -> None:
        self.__file = file
        self.__root = root
        self.__node = self.__root.get_child(file.read(1))
        self.__end = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.__end:
            raise StopIteration
        if not (bit := self.__file.read(1)):
            self.__end = True
        node = self.__node
        if node.is_leaf:
            self.__node = self.__root.get_child(bit)
        else:
            self.__node = node.get_child(bit)
        return node


class HuffmanDecoder(Decoder):
    def __init__(self, file: BinaryIO, tree: Tree) -> None:
        self.__file = file
        self.__tree = tree

    @property
    def decoder(self) -> Generator:
        file = self.__file
        root = self.__tree.root
        ti = TreeIterator(file, root)
        for node in iter(ti):
            if node.is_leaf:
                yield node.value

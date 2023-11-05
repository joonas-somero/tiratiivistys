from collections import deque
from typing import Self, BinaryIO, Generator

from tiratiivistys.classes import Tree, Reader, Weight
from tiratiivistys.huffman.node import HuffmanNode as Node
from tiratiivistys.huffman.node_queue import NodeQueue


class HuffmanTree(Tree):
    """A class for constructing Huffman-trees."""

    def __init__(self, root: Node, leaves: dict | None = None) -> None:
        self.root = root
        self.__leaves = leaves

    @property
    def nodes(self) -> Generator[Node, None, None]:
        """ Traverses the tree yielding it's nodes."""
        stack = deque([self.root])
        while stack and (node := stack.pop()):
            yield node
            if node.right_child is not None:
                stack.append(node.right_child)
            if node.left_child is not None:
                stack.append(node.left_child)

    def path_to(self, byte: bytes) -> tuple[bool] | None:
        """Finds a path to a leaf from the root.
        Only available when leaves are passed to constructor.
        """
        if self.__leaves is None:
            return None
        path = []
        node = self.__leaves[byte]
        while not node.is_root:
            path.append(node.edge)
            node = node.parent
        return tuple(reversed(path))

    @staticmethod
    def __count_occurrences(input_file: BinaryIO) -> Weight:
        """(Private)
        Counts the number of occurrences for bytes in 'input_file'
        and moves the file cursor back to the beginning.

        Positional arguments:
            input_file: A readable binary I/O stream.
        Returns:
            A list of tuples of the form (byte, occurrences).
        """
        occurrences = {}
        while byte := input_file.read(1):
            occurrences[byte] = (occurrences[byte] + 1
                                 if byte in occurrences
                                 else 1)
        input_file.seek(0)
        return [Weight(byte, weight) for byte, weight in occurrences.items()]

    @classmethod
    def from_input_file(cls, input_file: BinaryIO) -> Self:
        """Constructs a Huffman-tree from an input file.

        Positional arguments:
            input_file: A readable binary I/O stream.
        Returns:
            An instance of the class HuffmanTree (with 'path_to' available).
        """
        leaf_occurrences = cls.__count_occurrences(input_file)
        tree_builder = NodeQueue(leaf_occurrences, Node)
        root = tree_builder.root
        leaves = tree_builder.leaves
        return cls(root, leaves)

    @classmethod
    def from_encoded_data(cls, encoded_data: Reader) -> Self:
        """Recreates a Huffman-tree from an encoded representation.

        Positional arguments:
            encoded_data: The compressed data as a Reader object.
        Returns:
            An instance of the class HuffmanTree.
        """
        root = Node()
        stack = deque([root])
        while stack and (node := stack.pop()):
            if encoded_data.bit:
                node.value = encoded_data.literal
            else:
                node.reproduce()
                stack.extend([node.right_child, node.left_child])
        return cls(root)

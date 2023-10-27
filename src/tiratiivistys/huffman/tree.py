from typing import Self, BinaryIO, Generator
from collections import deque
from tiratiivistys.classes import Tree
from .node import HuffmanNode
from .node_queue import NodeQueue


class HuffmanTree(Tree):
    """A class for constructing Huffman-trees."""

    def __init__(self, root: Self, leaves: dict = None) -> None:
        self.root = root
        self.__leaves = leaves

    def __str__(self):
        return "\n".join("  " * depth + str(node)
                         for node, depth
                         in self.nodes)

    @property
    def nodes(self) -> Generator:
        stack = deque([(self.root, 0)])
        while stack and (item := stack.pop()):
            node, depth = item
            yield node, depth
            depth += 1
            if node.right_child:
                stack.append((node.right_child, depth))
            if node.left_child:
                stack.append((node.left_child, depth))

    def path_to(self, byte: bytes) -> tuple:
        path = []
        node = self.__leaves[byte]
        while not node.is_root:
            path.append(node.edge)
            node = node.parent
        return tuple(reversed(path))

    @staticmethod
    def __count_occurrences(file: BinaryIO) -> list[tuple]:
        """Counts the number of occurrences for bytes in a file
        and moves the cursor back to the beginning.

        Positional arguments:
            file: A binary I/O stream.
        Returns:
            A list of tuples of the form (byte, occurrences).
        """
        occurrences = {}
        while byte := file.read(1):
            occurrences[byte] = (occurrences[byte] + 1
                                 if byte in occurrences
                                 else 1)
        file.seek(0)
        return occurrences.items()

    @classmethod
    def from_input(cls, file: BinaryIO) -> Self:
        """Constructs a Huffman-tree from an input file.

        Positional arguments:
            file: A binary I/O stream.
        Returns:
            An instance of class HuffmanTree.
        """
        leaf_occurrences = cls.__count_occurrences(file)
        tree_builder = NodeQueue(leaf_occurrences, HuffmanNode)
        root = tree_builder.root
        leaves = tree_builder.leaves
        return cls(root, leaves)

    @classmethod
    def from_encoded(cls, file: BinaryIO) -> Self:
        """Recreates a Huffman-tree from an encoded representation
        in a file and does not move the cursor after.

        Positional arguments:
            file: A binary I/O stream.
        Returns:
            An instance of class HuffmanTree.
        """
        root = HuffmanNode()
        stack = deque([root])
        while stack and (node := stack.pop()):
            bit = file.read(1)
            if bit == b"1":
                node.value = file.read(1)
            else:
                node.reproduce()
                stack.extend([node.right_child, node.left_child])
        return cls(root)

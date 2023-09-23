from typing import Self
from functools import total_ordering
from fractions import Fraction
from queue import PriorityQueue


@total_ordering
class Node:
    """A class for holding the nodes of a Huffman-tree."""

    def __init__(self,
                 weight: Fraction,
                 left: Self = None,
                 right: Self = None,
                 parent: Self = None) -> None:
        self.weight = weight
        self.left_child = left
        self.right_child = right
        self.parent = parent

    def __eq__(self, other: Self) -> bool:
        return self.weight == other.weight

    def __lt__(self, other: Self) -> bool:
        return self.weight < other.weight


class Leaf(Node):
    """A leaf node subclass of Node for holding the actual data."""

    def __init__(self, byte: hex, weight: Fraction) -> None:
        super().__init__(weight)
        self.byte = byte


class HuffmanTree:
    """A class for constructing Huffman-tree."""

    def __init__(self) -> None:
        self.root = None
        self.queue = PriorityQueue()

    @classmethod
    def from_occurrences(cls, occurrences: dict, total: int) -> Self:
        """Constructs Huffman-tree using occurrences of bytes.

        Positional arguments:
            occurrences: A dict with hex bytes as keys for
                         int occurrences of the byte.
            total: The total number of occurrences, i.e.
                   sum(occurrences.values()).
        Returns:
            An instance of class HuffmanTree.
        """

        tree = cls()

        for key, value in occurrences.items():
            leaf = Leaf(key, Fraction(int(value), total))
            tree.queue.put(leaf)

        while tree.queue.qsize() > 1:
            left = tree.queue.get()
            right = tree.queue.get()
            weight = left.weight + right.weight

            node = Node(weight, left, right)
            left.parent = node
            right.parent = node

            tree.queue.put(node)

        tree.root = tree.queue.get()

        return tree

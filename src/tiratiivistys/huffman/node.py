from typing import Self

from tiratiivistys.classes import Node


class HuffmanNode(Node):
    """A class for holding a Huffman-tree node."""

    def __init__(self, value: bytes | None = None) -> None:
        self.value = value
        self.parent = None
        self.left_child = None
        self.right_child = None

    @property
    def edge(self) -> bool | None:
        if self.is_root:
            return None
        else:
            return self.parent.right_child is self

    @property
    def is_root(self) -> bool:
        return self.parent is None

    @property
    def is_leaf(self) -> bool:
        return self.value is not None

    def get_child(self, edge: bool | None) -> Self | None:
        if edge is not None:
            return self.right_child if edge else self.left_child
        else:
            return None

    def reproduce(self) -> None:
        self.left_child = HuffmanNode()
        self.right_child = HuffmanNode()
        self.left_child.parent = self.right_child.parent = self

    def adopt(self, left: Self, right: Self) -> None:
        left.parent = right.parent = self
        self.left_child = left
        self.right_child = right

from typing import Self
from tiratiivistys.classes import Node


class HuffmanNode(Node):
    """A class for holding a node of the Huffman-tree."""

    def __init__(self, value: bytes = None) -> None:
        self.value = value
        self.parent = None
        self.left_child = None
        self.right_child = None

    def __repr__(self):
        value = self.value if self.is_leaf else ''
        return f"{self.__class__.__name__}({value})"

    def __str__(self):
        return f"L: {self.value}" if self.is_leaf else "N"

    @property
    def edge(self) -> int | None:
        if self.is_root:
            return None
        else:
            return 0 if self.parent.left_child is self else 1

    @property
    def is_root(self) -> bool:
        return self.parent is None

    @property
    def is_leaf(self) -> bool:
        return self.value is not None

    def get_child(self, edge: bytes) -> Self:
        return self.left_child if edge == b"0" else self.right_child

    def reproduce(self) -> None:
        self.left_child = HuffmanNode()
        self.right_child = HuffmanNode()
        self.left_child.parent = self.right_child.parent = self

    def adopt(self, left: Self, right: Self) -> None:
        left.parent = right.parent = self
        self.left_child = left
        self.right_child = right

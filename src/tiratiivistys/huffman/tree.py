from functools import total_ordering
from fractions import Fraction
from queue import PriorityQueue


@total_ordering
class Node:
    def __init__(self, weight, left=None, right=None, parent=None):
        self.weight = weight
        self.left_child = left
        self.right_child = right
        self.parent = parent

    def __eq__(self, other):
        return self.weight == other.weight

    def __lt__(self, other):
        return self.weight < other.weight


class Leaf(Node):
    def __init__(self, byte, weight):
        Node.__init__(self, weight)
        self.byte = byte


class HuffmanTree:
    def __init__(self):
        self.root = None
        self.queue = PriorityQueue()

    @classmethod
    def from_occurrences(cls, occurrences, total):
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

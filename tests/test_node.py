import unittest
from random import randbytes

from tiratiivistys.huffman.node import HuffmanNode


class TestHuffmanNode(unittest.TestCase):
    def setUp(self):
        def value(): return randbytes(1)
        root = HuffmanNode()
        root.adopt(HuffmanNode(value), HuffmanNode(value))
        self.root = root

    def test_is_root(self):
        result = self.root.is_root
        self.assertTrue(result)
        result = self.root.left_child.is_root
        self.assertFalse(result)

    def test_edge(self):
        result = self.root.edge
        self.assertIsNone(result)
        left_result = self.root.left_child.edge
        right_result = self.root.right_child.edge
        self.assertFalse(left_result)
        self.assertTrue(right_result)

    def test_is_leaf(self):
        result = self.root.is_leaf
        self.assertFalse(result)
        result = self.root.left_child.is_leaf
        self.assertTrue(result)

    def test_get_child(self):
        left_bit = False
        right_bit = True
        no_bit = None
        result = self.root.get_child(left_bit)
        self.assertEqual(result, self.root.left_child)
        result = self.root.get_child(right_bit)
        self.assertEqual(result, self.root.right_child)
        result = self.root.get_child(no_bit)
        self.assertIsNone(result)

    def test_reproduce(self):
        node = HuffmanNode()
        node.reproduce()
        left_child = node.left_child
        right_child = node.right_child
        self.assertIsNotNone(left_child)
        self.assertIsNotNone(right_child)
        self.assertIs(node, left_child.parent)
        self.assertIs(node, right_child.parent)

    def test_adopt(self):
        node = HuffmanNode()
        left = HuffmanNode()
        right = HuffmanNode()
        node.adopt(left, right)
        self.assertIs(node.left_child, left)
        self.assertIs(node.right_child, right)
        self.assertIs(left.parent, node)
        self.assertIs(right.parent, node)

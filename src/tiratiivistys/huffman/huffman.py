from typing import BinaryIO, Generator
from tiratiivistys.classes import Compressor
from .tree import HuffmanTree
from .encoder import HuffmanEncoder as Encoder
from .decoder import HuffmanDecoder as Decoder


class Huffman(Compressor):
    """An interface to compress and restore files using Huffman Coding."""
    @staticmethod
    def compress(file: BinaryIO) -> Generator:
        tree = HuffmanTree.from_input(file)
        return Encoder(file, tree).encoder

    @staticmethod
    def restore(file: BinaryIO) -> Generator:
        tree = HuffmanTree.from_encoded(file)
        return Decoder(file, tree).decoder

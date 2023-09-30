from typing import BinaryIO, Tuple
from tiratiivistys.classes import Compressor
from .tree import HuffmanTree


class Huffman(Compressor):
    """An interface to compress and restore files using Huffman Coding."""

    @staticmethod
    def count_occurrences(file: BinaryIO) -> Tuple[dict, int]:
        """Counts the number of occurrences of bytes in a file.

        Positional arguments:
            file: A binary I/O stream.
        Returns:
            A tuple of
            - dict with bytes (hex) as keys for the number of occurrences of
              the byte found in file
            - the total number of bytes read from the file.
        """

        occurrences = {}
        total_bytes = 0
        while byte := file.read(1).hex():
            total_bytes += 1
            occurrences[byte] = (occurrences[byte] + 1
                                 if byte in occurrences
                                 else 1)

        return occurrences, total_bytes

    @classmethod
    def compress(cls, file: BinaryIO) -> None:
        occurrences, total_bytes = cls.count_occurrences(file)
        huffman_tree = HuffmanTree.from_occurrences(occurrences, total_bytes)

        compressed_file = None

    @classmethod
    def restore(cls, file: BinaryIO) -> None:
        pass

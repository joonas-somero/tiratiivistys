from .tree import HuffmanTree


class Huffman:
    """An interface to compress and restore files using Huffman Coding."""
    @staticmethod
    def __count_occurrences(file) -> dict:
        """Returns a tuple of (occurrences, total_bytes), where
           - occurrences is a dict with bytes (hex) as keys for the
             number of occurrences of the byte in question found in file
           - total_bytes is the number of bytes read from the file
        """
        occurrences = {}
        total_bytes = 0
        while byte := file.read(1).hex():
            total_bytes += 1
            occurrences[byte] = (occurrences[byte] + 1
                                 if byte in occurrences
                                 else 1)

        return occurrences, total_bytes

    @staticmethod
    def compress(file) -> None:
        occurrences, total_bytes = Huffman.__count_occurrences(file)
        huffman_tree = HuffmanTree.from_occurrences(occurrences, total_bytes)

        compressed_file = None

    @staticmethod
    def restore(file) -> None:
        pass

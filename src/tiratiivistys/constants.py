from typing import Final

# Number of loci addressable using a single byte
MAX_SIZE: Final[int] = 256

# One byte for each in ( offset, length, character )
CODEWORD_LENGTH: Final[int] = 3

# File extensions
EXTENSIONS: Final[dict] = {
    "huffman": ".huffman",
    "lempel-ziv": ".lempel-ziv"
}

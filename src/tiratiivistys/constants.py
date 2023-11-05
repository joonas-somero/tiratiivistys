from typing import Final


# Number of loci addressable using a single byte
MAX_SIZE: Final[int] = 256

# One byte for each in ( offset, length, character )
TOKEN_LENGTH: Final[int] = 3

# A single byte
LITERAL_LENGTH: Final[int] = 1

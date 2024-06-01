from typing import Final
from math import log2, floor


MAX_OFFSET: Final[int] = (2**9) - 1
MAX_HISTORY: Final[int] = MAX_OFFSET
MAX_BUFFER: Final[int] = MAX_HISTORY // 4

# Number of bits needed to encode the offset or length of a Lempel-Ziv token
N_BITS = floor(log2(MAX_OFFSET)) + 1

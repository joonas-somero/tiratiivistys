from typing import Self

from tiratiivistys.constants import N_BITS
from tiratiivistys.classes import Codeword, Token


class LempelZivToken(Token):
    """A class for encoding a string of bytes into an offset and a length."""

    def __init__(self, offset: int, length: int) -> None:
        self.offset = offset
        self.length = length

    @property
    def codeword(self) -> Codeword:
        return Codeword(self.offset, self.length)

    @classmethod
    def encode(cls,
               start: int,
               frame: bytes,
               history: bytearray,
               buffer: bytearray) -> Self | None:
        """A classmethod for matching a frame in window, i.e.
        history+buffer, and constructing a LempelZivToken
        if frame matches the corresponding frame in buffer.
        """
        frame_length = len(frame)
        offset = len(history) - start
        buffer_frame = buffer[:len(frame)]

        return (cls(offset, frame_length)
                if frame == buffer_frame and offset > 0
                else None)

    @classmethod
    def codeword_length(cls, token: bytes | Codeword) -> int:
        """Returns the encoded length of the token measured in bits."""
        if cls.is_token(token):
            # prefix + offset + length
            return 1 + N_BITS + N_BITS
        else:
            # prefix + value
            return 1 + 8

    @staticmethod
    def is_token(token: bytes | Codeword) -> bool:
        return not isinstance(token, bytes)

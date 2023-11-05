from typing import Self

from tiratiivistys.classes import Token
from tiratiivistys.constants import TOKEN_LENGTH, LITERAL_LENGTH


class LempelZivToken(Token):
    """A class for holding a range of matching strings of bytes and
    classmethods for encoding and decoding codewords.
    """

    def __init__(self,
                 offset: int = 0,
                 length: int = 0,
                 character: int = 0) -> None:
        self.offset = offset
        self.length = length
        self.character = character

    def __getitem__(self, key: int | slice) -> int | list[int]:
        return [self.offset, self.length, self.character][key]

    def __bytes__(self) -> bytes:
        return bytes([self.offset, self.length, self.character])

    @property
    def is_token(self) -> bool:
        return not self.offset == self.length == 0

    @classmethod
    def literal(cls, character: int) -> Self:
        """A classmethod for encoding a literal character."""
        return cls(character=character)

    @classmethod
    def decode(cls, codeword: bytes) -> Self | None:
        """A classmethod for decoding a codeword into
        an LempelZivToken object.
        """
        if len(codeword) == TOKEN_LENGTH:
            return cls(*codeword)
        elif len(codeword) == LITERAL_LENGTH:
            return cls.literal(int.from_bytes(codeword))
        else:
            return None

    @classmethod
    def encode(cls,
               start: int,
               frame: bytearray,
               history: bytearray,
               buffer: bytearray) -> Self | None:
        """A classmethod for matching a frame in window, i.e.
        history+buffer, and constructing a LempelZivToken
        if frame matches the corresponding frame in buffer.
        """
        frame_length = len(frame)
        history_length = len(history)
        offset = history_length - start
        character = buffer[frame_length]
        buffer_frame = buffer[:frame_length]

        return (cls(offset, frame_length, character)
                if frame == buffer_frame
                else None)

from typing import Self
from tiratiivistys.constants import CODEWORD_LENGTH


class EncodedRange:
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

    def __getitem__(self, key):
        return [self.offset, self.length, self.character][key]

    def __repr__(self):
        return ("EncodedRange(" +
                f"offset={self.offset}, "
                f"length={self.length}, "
                f"character={self.character})")

    def __bytes__(self):
        return bytes([self.offset, self.length, self.character])

    @classmethod
    def literal(cls, character) -> Self:
        """A classmethod for encoding a literal character."""
        return cls(character=character)

    @classmethod
    def decode(cls, codeword: bytes) -> Self | None:
        """A classmethod for decoding a codeword into
        an EncodedRange object.
        """
        return (cls(*codeword)
                if len(codeword) == CODEWORD_LENGTH
                else None)

    @classmethod
    def encode(cls,
               start: int,
               frame: bytearray,
               history: bytearray,
               buffer: bytearray) -> Self | None:
        """A classmethod for matching a frame in window, i.e.
        history+buffer, and constructing an EncodedRange object
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

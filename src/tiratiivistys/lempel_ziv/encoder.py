from typing import Self, Any, Generator, BinaryIO
from tiratiivistys.constants import CODEWORD_LENGTH
from tiratiivistys.classes import Encoder
from tiratiivistys.lempel_ziv.window import SlidingWindow


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
        if frame matches the corresponding frame in window.
        """
        frame_length = len(frame)
        history_length = len(history)
        offset = history_length - start
        character = buffer[frame_length]

        history_slice = slice(start,
                              start + frame_length)
        buffer_slice = slice(None,
                             max((start + frame_length) - history_length, 0))
        window_frame = history[history_slice] + buffer[buffer_slice]

        return (cls(offset, frame_length, character)
                if frame == window_frame
                else None)


class LempelZivEncoder(Encoder):
    def __init__(self, file: BinaryIO) -> None:
        self.__input = file
        self.__window = SlidingWindow(file, EncodedRange, 64, 32)

    @property
    def encoder(self) -> Generator:
        window = self.__window
        while window.has_input:
            match = window.match
            window.slide(match.length+1)
            yield bytes(match)

        while self.__window.has_input:
            pass

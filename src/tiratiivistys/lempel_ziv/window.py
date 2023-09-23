from typing import Final, Self, Tuple, Any, Callable, Generator, BinaryIO
from functools import total_ordering
from queue import PriorityQueue


# Number of loci addressable with a single byte
MAX_SIZE: Final = int.from_bytes(b"\xff")


@total_ordering
class EncodedRange:
    """A class for holding a range of matching strings of bytes."""

    def __init__(self, character: int) -> None:
        self.offset = 0
        self.length = 0
        self.character = character

    def __eq__(self, other: Self) -> bool:
        return (self.offset == other.offset and
                self.length == other.length and
                self.character == other.character)

    def __lt__(self, other: Self) -> bool:
        # Longer length signifies a lower priority
        return self.length > other.length

    def __repr__(self) -> str:
        return str(bytes(self))

    def __bytes__(self) -> bytes:
        return bytes([self.offset, self.length, self.character])

    @classmethod
    def encode(cls,
               start: int,
               frame: bytearray,
               history: bytearray,
               buffer: bytearray) -> Self:
        length = len(frame)
        offset = len(history) - start
        character = buffer[length]
        encoding = cls(character)
        encoding.offset = offset
        encoding.length = length

        return encoding


class SearchWindow:
    def __init__(self, file: BinaryIO, encoder: Any) -> None:
        self.__file = file
        self.__encoder = encoder
        self.__history = bytearray()
        self.__buffer = bytearray()
        self.__window = self.__new_window()

        self.__read_input()

    @property
    def has_input(self) -> bool:
        return len(self.__buffer) > 0

    @property
    def cursor(self) -> int:
        return self.__buffer[0]

    @property
    def match(self) -> Any:
        if self.cursor not in self.__history:
            return self.__encoder(self.cursor)

        matches = PriorityQueue()
        search_range = range(len(self.__history))
        frame = int.to_bytes(self.cursor)
        while (start := self.__window.find(frame)) in search_range:
            match = self.__encoder.encode(start,
                                          frame,
                                          self.__history,
                                          self.__buffer)
            matches.put(match)
            frame = self.__buffer[:len(frame)+1]

        return matches.get()

    def __new_window(self) -> bytearray:
        return self.__history + self.__buffer

    def __read_input(self) -> None:
        bytes_free = MAX_SIZE - len(self.__buffer)

        self.__buffer.extend(self.__file.read(bytes_free))
        self.__window = self.__new_window()

    def __popleft(self, length: int) -> bytearray:
        frame = self.__buffer[:length]
        del self.__buffer[:length]

        return frame

    def __discardleft(self, length: int) -> None:
        bytes_free = MAX_SIZE - len(self.__history)

        del self.__history[:length-bytes_free]

    def slide(self, length: int) -> None:
        if MAX_SIZE - len(self.__history) < length:
            self.__discardleft(length)
        self.__history.extend(self.__popleft(length))

        self.__read_input()


class SlidingWindow:
    def __init__(self, window: Any):
        self.__window = window

    @property
    def encoder(self) -> Generator:
        while self.__window.has_input:
            match = self.__window.match
            self.__window.slide(match.length+1)

            yield bytes(match)

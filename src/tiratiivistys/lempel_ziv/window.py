from typing import Self, Any, Callable, Generator
from click import File


MAX_SIZE = b'\xff'[0]  # Number of loci addressable with a single byte


class EncodedRange:
    def __init__(self, character: int):
        self.offset = 0
        self.length = 0
        self.character = character

    def __repr__(self) -> str:
        return str(bytes(self))

    def __bytes__(self) -> bytes:
        return bytes([self.offset, self.length, self.character])

    @classmethod
    def encode(cls, character: int, offset: int, length: int) -> Self:
        encoding = cls(character)
        encoding.offset = offset
        encoding.length = length

        return encoding


class SearchWindow:
    def __init__(self, file: File):
        self.__file = file
        self.__encoded = bytearray()
        self.__input = bytearray()
        self.__window = self.__new_window()

        self.__read_input()

    @property
    def has_input(self) -> bool:
        return len(self.__input) > 0

    @property
    def cursor(self) -> int:
        return self.__input[0]

    @property
    def match(self) -> tuple:
        offset = length = 0
        character = self.cursor
        window = self.__window
        buffer = self.__input
        search_frame = buffer[:length+1]
        search_range = range(len(self.__encoded))
        while (index := window.find(search_frame)) in search_range:
            character = buffer[len(search_frame)]
            offset = len(self.__encoded) - index
            length += 1

            search_frame = buffer[:length+1]

        return offset, length, character

    def __new_window(self) -> bytearray:
        return self.__encoded + self.__input

    def __read_input(self) -> None:
        bytes_free = MAX_SIZE - len(self.__input)

        self.__input.extend(self.__file.read(bytes_free))
        self.__window = self.__new_window()

    def __popleft(self, length: int) -> bytearray:
        frame = self.__input[:length]
        del self.__input[:length]

        return frame

    def __discardleft(self, length: int) -> None:
        del self.__encoded[:length-bytes_free]

    def slide(self, length: int) -> None:
        if MAX_SIZE - len(self.__encoded) < length:
            self.__discardleft(length)
        self.__encoded.extend(self.__popleft(length))

        self.__read_input()


class SlidingWindow:
    def __init__(self, window: Any, encoder: Callable):
        self.__window = window
        self.__encode = encoder

    def __encode_match(self) -> Any:
        offset, length, character = self.__window.match

        return self.__encode(character, offset, length)

    @property
    def encoder(self) -> Generator:
        while self.__window.has_input:
            match = self.__encode_match()
            self.__window.slide(match.length+1)

            yield bytes(match)

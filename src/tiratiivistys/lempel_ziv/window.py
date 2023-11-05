from typing import BinaryIO, Generator

from tiratiivistys.classes import Token, Window
from tiratiivistys.constants import MAX_SIZE, TOKEN_LENGTH, LITERAL_LENGTH


class SlidingWindow(Window):
    """Implements the sliding window technique used by
    the LZ77 algorithm.
    """

    def __init__(self,
                 input_file: BinaryIO,
                 encoder: Token,
                 history_size: int = MAX_SIZE-1,
                 buffer_size: int = MAX_SIZE) -> None:
        self.__input_file = input_file
        self.__encoder = encoder
        self.__history_size = history_size
        self.__buffer_size = buffer_size
        self.__history = bytearray()
        self.__buffer = bytearray()
        self.__window = self.__new_window()
        self.__read_input()

    def __new_window(self) -> bytearray:
        return self.__history + self.__buffer

    def __read_input(self) -> None:
        bytes_free = self.__buffer_size - len(self.__buffer)
        self.__buffer.extend(self.__input_file.read(bytes_free))
        self.__window = self.__new_window()

    def __popleft(self, count: int) -> bytearray:
        frame = self.__buffer[:count]
        del self.__buffer[:count]
        return frame

    def __discardleft(self, count: int) -> None:
        del self.__history[:count]

    def __slide(self, count: int) -> None:
        if self.__history_size - len(self.__history) < count:
            self.__discardleft(count)
        self.__history.extend(self.__popleft(count))
        self.__read_input()

    def __next_start(self, start: int, match: Token) -> int:
        buffer_slice = slice(start, start+match.length)
        frame = self.__buffer[buffer_slice]
        return self.__window.find(frame,
                                  start+1,
                                  len(self.__history)-1 + match.length)

    def __find_longer(self, start: int, current: Token) -> Token:
        match = current
        stop = start + match.length+1
        while stop < len(self.__buffer):
            next_match = self.__encoder.encode(start,
                                               self.__window[start:stop],
                                               self.__history,
                                               self.__buffer)
            if next_match is not None:
                match = next_match
                stop += 1
            else:
                break
        return match

    @property
    def __cursor(self):
        return self.__buffer[0]

    @property
    def __longest_match(self) -> Token:
        literal = self.__encoder.literal(self.__cursor)
        start = self.__history.find(self.__cursor)
        match = literal
        while -1 < start < len(self.__buffer)-2:
            match = self.__find_longer(start, match)
            start = self.__next_start(start, match)
        return (match
                if match.length >= TOKEN_LENGTH
                else literal)

    @property
    def output(self) -> Generator[Token, None, None]:
        while self.__buffer:
            match = self.__longest_match
            self.__slide(match.length+1)
            yield match


class TokenWindow(Window):
    def __init__(self,
                 compressed_data: Generator[bytes, None, None],
                 decoder: Token) -> None:
        self.__input_data = compressed_data
        self.__decoder = decoder
        self.__history = bytearray()

    def __decoded_range(self, codeword: bytes) -> Generator[int, None, None]:
        offset, length, character = self.__decoder.decode(codeword)
        start = len(self.__history)
        stop = start + length
        for cursor in range(start, stop):
            _character = self.__history[cursor - offset]
            self.__history.append(_character)
            yield _character
        self.__history.append(character)
        yield character

    @property
    def output(self) -> Generator[int, None, None]:
        for codeword in self.__input_data:
            for character in self.__decoded_range(codeword):
                yield character

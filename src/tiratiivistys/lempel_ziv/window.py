from typing import BinaryIO, Generator

from tiratiivistys.classes import Codeword, Window
from tiratiivistys.constants import MAX_HISTORY, MAX_BUFFER
from tiratiivistys.lempel_ziv.token import LempelZivToken as Token


class SlidingWindow(Window):
    """Implements the sliding window technique used in
    the LZ77 algorithm.
    """

    def __init__(self,
                 input_file: BinaryIO,
                 encoder: Token) -> None:
        self.__input_file = input_file
        self.__encoder = encoder
        self.__history = bytearray()
        self.__buffer = bytearray()
        self.__window = self.__new_window()
        self.__read_input()

    def __new_window(self) -> bytearray:
        return bytes(self.__history + self.__buffer)

    def __read_input(self) -> None:
        bytes_free = MAX_BUFFER - len(self.__buffer)
        self.__buffer.extend(self.__input_file.read(bytes_free))
        self.__window = self.__new_window()

    def __popleft(self, count: int) -> bytearray:
        frame = self.__buffer[:count]
        del self.__buffer[:count]
        return frame

    def __discardleft(self, count: int) -> None:
        del self.__history[:count]

    def __slide(self, count: int) -> None:
        if MAX_HISTORY - len(self.__history) < count:
            self.__discardleft(count)
        self.__history.extend(self.__popleft(count))
        self.__read_input()

    def __next_start(self, start: int, match: Token) -> int:
        buffer_slice = slice(start, start+match.length)
        frame = self.__buffer[buffer_slice]
        return self.__window.find(frame,
                                  start+1,
                                  len(self.__history) + match.length)

    def __find_longer(self, start: int, current: Token) -> Token:
        match = current
        stop = start + (match.length+1
                        if Token.is_token(match)
                        else 1)
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
        return bytes(self.__buffer[0:1])

    @property
    def __longest_match(self) -> Token:
        literal = self.__cursor
        match = literal
        start = self.__history.find(self.__cursor)
        while -1 < start < len(self.__buffer)-2:
            match = self.__find_longer(start, match)
            start = self.__next_start(start, match)
        if match is literal:
            return literal
        elif (Token.codeword_length(match)
              > Token.codeword_length(literal) * match.length):
            return literal
        else:
            return match

    @property
    def output(self) -> Generator[Token, None, None]:
        while self.__buffer:
            match = self.__longest_match
            self.__slide(match.length
                         if Token.is_token(match)
                         else 1)
            yield match


class TokenWindow(Window):
    """Class for decoding tokens in compressed data."""

    def __init__(self,
                 compressed_data: Generator[Codeword, None, None],
                 decoder: Token) -> None:
        self.__input_data = compressed_data
        self.__decoder = decoder
        self.__history = []

    def __decoded_token(self,
                        token: bytes | Codeword
                        ) -> Generator[bytes, None, None]:
        if Token.is_token(token):
            start = len(self.__history)
            stop = start + token.length
            for cursor in range(start, stop):
                index = cursor - token.offset
                character = self.__history[index]
                self.__history.append(character)
                yield character
        else:
            self.__history.append(token)
            yield token

    @property
    def output(self) -> Generator[bytes, None, None]:
        for codeword in self.__input_data:
            for character in self.__decoded_token(codeword):
                yield character

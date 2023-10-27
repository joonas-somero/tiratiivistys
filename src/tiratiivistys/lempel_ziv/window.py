from typing import BinaryIO, Generator
from tiratiivistys.classes import Matcher, Window
from tiratiivistys.constants import MAX_SIZE, CODEWORD_LENGTH


class SlidingWindow(Window):
    """Implements the sliding window technique used by
    the LZ77 algorithm.
    """
    def __init__(self,
                 file: BinaryIO,
                 encoder: Matcher,
                 history_size: int = MAX_SIZE-1,
                 buffer_size: int = MAX_SIZE) -> None:
        self.__file = file
        self.__encoder = encoder
        self.__history_size = history_size
        self.__buffer_size = buffer_size
        self.__history = bytearray()
        self.__buffer = bytearray()
        self.__window = self.__new_window()
        self.__read_input()

    @property
    def __match(self) -> Matcher:
        history, buffer, window, encoder = (self.__history,
                                            self.__buffer,
                                            self.__window,
                                            self.__encoder)
        b_length, h_length = len(buffer), len(history)
        cursor = buffer[0]
        match = encoder.literal(cursor)
        start = history.find(cursor)
        while -1 < start < b_length-2:
            stop = start + match.length+1
            while stop < b_length-1:
                if next_match := encoder.encode(start,
                                                window[start:stop],
                                                history,
                                                buffer):
                    match = next_match
                    stop += 1
                else:
                    break
            frame = buffer[start:start+match.length]
            f_start = start+1
            f_stop = h_length+match.length-1

            start = window.find(frame, f_start, f_stop)
        return match

    def __new_window(self) -> bytearray:
        return self.__history + self.__buffer

    def __read_input(self) -> None:
        bytes_free = self.__buffer_size - len(self.__buffer)
        self.__buffer.extend(self.__file.read(bytes_free))
        self.__window = self.__new_window()

    def __popleft(self, length: int) -> bytearray:
        frame = self.__buffer[:length]
        del self.__buffer[:length]
        return frame

    def __discardleft(self, length: int) -> None:
        del self.__history[:length]

    def __slide(self, length: int) -> None:
        if self.__history_size - len(self.__history) < length:
            self.__discardleft(length)
        self.__history.extend(self.__popleft(length))
        self.__read_input()

    @property
    def output(self) -> Generator:
        while self.__buffer:
            match = self.__match
            self.__slide(match.length+1)
            yield match


class CodeWordWindow(Window):
    def __init__(self,
                 file: BinaryIO,
                 decoder: Matcher):
        self.__file = file
        self.__decoder = decoder
        self.__history = bytearray()

    def __decoded_range(self, codeword: bytes) -> Generator:
        history = self.__history
        offset, length, character = self.__decoder.decode(codeword)
        start = len(history)
        stop = start + length
        for cursor in range(start, stop):
            _character = history[cursor - offset]
            history.append(_character)
            yield _character
        history.append(character)
        yield character

    @property
    def output(self) -> Generator:
        file = self.__file
        while codeword := file.read(CODEWORD_LENGTH):
            for character in self.__decoded_range(codeword):
                yield character

from typing import Any, BinaryIO
from tiratiivistys.constants import MAX_SIZE, CODEWORD_LENGTH


class SlidingWindow:
    def __init__(self,
                 file: BinaryIO,
                 encoder: Any,
                 history_size: int = MAX_SIZE,
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
    def has_input(self) -> bool:
        return len(self.__buffer) > 0

    @property
    def match(self) -> Any:
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

    def slide(self, length: int) -> None:
        if self.__history_size - len(self.__history) < length:
            self.__discardleft(length)
        self.__history.extend(self.__popleft(length))
        self.__read_input()


class CodeWordWindow:
    def __init__(self,
                 file: BinaryIO,
                 decoder: Any) -> None:
        self.__file = file
        self.__decoder = decoder

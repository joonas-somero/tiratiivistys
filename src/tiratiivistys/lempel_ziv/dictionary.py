from tiratiivistys.constants import BIT_WIDTH
from tiratiivistys.classes import Dictionary


class LZWDictionary(Dictionary):
    def __init__(self) -> None:
        self.__codes: [bytes] = [i.to_bytes() for i in range(2**8)]
        self.__max_length = (2**BIT_WIDTH) - 1

    def __contains__(self, item: bytes | None) -> bool:
        return item in self.__codes if item is not None else False

    def __getitem__(self, key: int | None) -> bytes | None:
        return self.__codes[key] if key is not None else None

    def index(self, value: bytes) -> int:
        return self.__codes.index(value)

    def add(self, item: bytes) -> None:
        if len(self.__codes) <= self.__max_length:
            self.__codes.append(item)

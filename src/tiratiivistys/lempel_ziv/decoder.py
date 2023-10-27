from typing import Self, Generator
from tiratiivistys.classes import Decoder, Window


class LempelZivDecoder(Decoder):
    def __init__(self, window: Window) -> None:
        self.__window = window

    @property
    def decoder(self) -> Generator:
        for character in self.__window.output:
            yield int.to_bytes(character)

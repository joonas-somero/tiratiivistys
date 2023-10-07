from typing import Self, Any, Generator
from tiratiivistys.classes import Decoder


class LempelZivDecoder(Decoder):
    def __init__(self, window: Any) -> None:
        self.__window = window

    @property
    def decoder(self) -> Generator:
        for character in self.__window.characters:
            yield int.to_bytes(character)

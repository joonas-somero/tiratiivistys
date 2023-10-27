from typing import Generator
from tiratiivistys.classes import Encoder, Window


class LempelZivEncoder(Encoder):
    def __init__(self, window: Window) -> None:
        self.__window = window

    @property
    def encoder(self) -> Generator:
        for match in self.__window.output:
            yield bytes(match)

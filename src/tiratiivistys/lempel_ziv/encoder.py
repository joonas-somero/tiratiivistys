from typing import Any, Generator
from tiratiivistys.classes import Encoder


class LempelZivEncoder(Encoder):
    def __init__(self, window: Any) -> None:
        self.__window = window

    @property
    def encoder(self) -> Generator:
        window = self.__window
        while window.has_input:
            match = window.match
            window.slide(match.length+1)
            yield bytes(match)

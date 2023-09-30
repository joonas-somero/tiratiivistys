from typing import Generator, BinaryIO
from abc import ABC, abstractproperty, abstractclassmethod


class Encoder(ABC):
    @abstractproperty
    def encoder() -> Generator:
        pass


class Decoder(ABC):
    @abstractproperty
    def decoder() -> Generator:
        pass


class Compressor(ABC):
    @abstractclassmethod
    def compress(file: BinaryIO) -> None:
        pass

    @abstractclassmethod
    def restore(file: BinaryIO) -> None:
        pass

from typing import Self, Generator, BinaryIO
from abc import ABC, abstractmethod


class Node(ABC):
    @property
    @abstractmethod
    def edge(self) -> int | None:
        pass

    @property
    @abstractmethod
    def is_root(self) -> bool:
        pass

    @property
    @abstractmethod
    def is_leaf(self) -> bool:
        pass

    @abstractmethod
    def get_child(self, edge: bytes) -> Self:
        pass

    @abstractmethod
    def reproduce(self) -> None:
        pass

    @abstractmethod
    def adopt(self, left: Self, right: Self) -> None:
        pass


class Tree(ABC):
    @property
    @abstractmethod
    def nodes() -> Generator:
        pass

    @abstractmethod
    def path_to(self, byte: bytes) -> list:
        pass

    @classmethod
    @abstractmethod
    def from_input(cls, file: BinaryIO) -> Self:
        pass

    @classmethod
    @abstractmethod
    def from_encoded(cls, file: BinaryIO) -> Self:
        pass


class Matcher(ABC):
    @classmethod
    @abstractmethod
    def literal(cls, character: int) -> Self:
        pass

    @classmethod
    @abstractmethod
    def decode(cls, codeword: bytes) -> Self:
        pass

    @classmethod
    @abstractmethod
    def encode(cls,
               start: int,
               frame: bytearray,
               history: bytearray,
               buffer: bytearray) -> Self | None:
        pass


class Window(ABC):
    @property
    @abstractmethod
    def output() -> Generator:
        pass


class Encoder(ABC):
    @property
    @abstractmethod
    def encoder() -> Generator:
        pass


class Decoder(ABC):
    @property
    @abstractmethod
    def decoder() -> Generator:
        pass


class Compressor(ABC):
    @staticmethod
    @abstractmethod
    def compress(file: BinaryIO) -> None:
        pass

    @staticmethod
    @abstractmethod
    def restore(file: BinaryIO) -> None:
        pass

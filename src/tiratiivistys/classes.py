from abc import ABC, abstractmethod
from typing import Self, Generator, BinaryIO, Callable, NamedTuple


class Weight(NamedTuple):
    value: bytes
    weight: int


class Codeword(NamedTuple):
    offset: int
    length: int


class Reader(ABC):
    @abstractmethod
    def __init__(self, input_file: BinaryIO) -> None:
        ...

    @abstractmethod
    def _read(self,
              method: Callable,
              fmt: str | list[str]) -> bool | bytes | Codeword | None:
        ...

    @property
    @abstractmethod
    def next_bit(self) -> bool | None:
        ...

    @property
    @abstractmethod
    def next_byte(self) -> bytes | None:
        ...


class Writer(ABC):
    @abstractmethod
    def write_to(self, output_file: BinaryIO) -> None:
        ...

    @abstractmethod
    def bit(self, bit: bool) -> None:
        ...

    @abstractmethod
    def byte(self, byte: bytes) -> None:
        ...


class Node(ABC):
    @abstractmethod
    def __init__(self, value: bytes | None) -> None:
        ...

    @property
    @abstractmethod
    def edge(self) -> bool | None:
        ...

    @property
    @abstractmethod
    def is_root(self) -> bool:
        ...

    @property
    @abstractmethod
    def is_leaf(self) -> bool:
        ...

    @abstractmethod
    def get_child(self, edge: bool | None) -> Self | None:
        ...

    @abstractmethod
    def reproduce(self) -> None:
        ...

    @abstractmethod
    def adopt(self, left: Self, right: Self) -> None:
        ...


class Tree(ABC):
    @abstractmethod
    def __init__(self, root: Node, leaves: dict | None) -> None:
        ...

    @property
    @abstractmethod
    def nodes(self) -> Generator[Node, None, None]:
        ...

    @abstractmethod
    def path_to(self, byte: bytes) -> tuple[bool] | None:
        ...

    @classmethod
    @abstractmethod
    def from_input_file(cls, input_file: BinaryIO) -> Self:
        ...

    @classmethod
    @abstractmethod
    def from_encoded_data(cls, encoded_data: Reader) -> Self:
        ...


class Token(ABC):
    @property
    @abstractmethod
    def codeword(self) -> Codeword:
        ...

    @classmethod
    @abstractmethod
    def encode(cls,
               start: int,
               frame: bytes,
               history: bytearray,
               buffer: bytearray) -> Self | None:
        ...

    @classmethod
    @abstractmethod
    def codeword_length(cls, token: bytes | Codeword) -> int:
        ...

    @staticmethod
    def is_token(token: bytes | Codeword) -> bool:
        ...


class Window(ABC):
    @property
    @abstractmethod
    def output(self) -> Generator[Token | bytes, None, None]:
        ...


class Model(ABC):
    @property
    def executor(self) -> Callable[[BinaryIO], None]:
        ...

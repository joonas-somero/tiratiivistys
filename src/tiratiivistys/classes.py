from abc import ABC, abstractmethod
from typing import Self, Generator, BinaryIO, Callable, NamedTuple


class Reader(ABC):
    """Reads files one bit at a time."""
    @abstractmethod
    def __init__(self,
                 input_file: BinaryIO,
                 padded: bool | None) -> None:
        ...

    @property
    @abstractmethod
    def bit(self) -> bool | None:
        ...

    @property
    @abstractmethod
    def literal(self) -> bytes | None:
        ...

    @property
    @abstractmethod
    def token(self) -> bytes | None:
        ...


class Writer(ABC):
    @abstractmethod
    def write_to(self, output_file: BinaryIO, padded: bool | None) -> None:
        ...

    @abstractmethod
    def bit(self, bit: bool) -> None:
        ...

    @abstractmethod
    def byte(self, byte: bytes) -> None:
        ...

    @abstractmethod
    def token(self, token: bytes) -> None:
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
    @abstractmethod
    def __getitem__(self, key: int | slice) -> int | list[int]:
        ...

    @abstractmethod
    def __bytes__(self) -> bytes:
        ...

    @property
    @abstractmethod
    def is_token(self) -> bool:
        ...

    @classmethod
    @abstractmethod
    def literal(cls, character: int) -> Self:
        ...

    @classmethod
    @abstractmethod
    def decode(cls, codeword: bytes) -> Self | None:
        ...

    @classmethod
    @abstractmethod
    def encode(cls,
               start: int,
               frame: bytearray,
               history: bytearray,
               buffer: bytearray) -> Self | None:
        ...


class Window(ABC):
    @property
    @abstractmethod
    def output(self) -> Generator[int, None, None]:
        ...


class Model(ABC):
    @property
    def executor(self) -> Callable[[BinaryIO], None]:
        ...


class Weight(NamedTuple):
    byte: bytes
    weight: int

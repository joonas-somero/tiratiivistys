from abc import ABC, abstractmethod
from typing import Self, Generator, BinaryIO, Callable, NamedTuple


class Weight(NamedTuple):
    value: bytes
    weight: int


class Reader(ABC):
    @abstractmethod
    def __init__(self, input_file: BinaryIO) -> None:
        ...

    @abstractmethod
    def _read(self, fmt: str) -> bool | bytes | int | None:
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


class Dictionary(ABC):
    @abstractmethod
    def __contains__(self, item: bytes | None) -> bool:
        ...

    def __getitem__(self, key: int | None) -> bytes | None:
        ...

    @abstractmethod
    def index(self, value: bytes) -> int:
        ...

    @abstractmethod
    def add(self, item: bytes) -> None:
        ...


class Model(ABC):
    @property
    def executor(self) -> Callable[[BinaryIO], None]:
        ...

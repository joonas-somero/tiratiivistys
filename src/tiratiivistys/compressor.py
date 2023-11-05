from typing import BinaryIO, Callable

from tiratiivistys.classes import Model


class Compressor:
    """Prepares a data compression model for deployment.

    Positional arguments:
        model: An interface to an implementation of a data compression model.
        input_file: A readable binary I/O stream.
        output_file: A writable binary I/O stream.
    """

    def __init__(self, model: Model,
                 input_file: BinaryIO,
                 output_file: BinaryIO) -> None:
        self.__Model = model
        self.__input_file = input_file
        self.__output_file = output_file

    def deploy(self) -> None:
        output_to: Callable[[BinaryIO], None] = self.__Model(
            self.__input_file).executor
        output_to(self.__output_file)

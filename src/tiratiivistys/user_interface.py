from typing import BinaryIO
import click
from tiratiivistys.constants import EXTENSIONS
from .huffman import Huffman
from .lempel_ziv import LempelZiv


def write_output(filename: str, content: bytes) -> None:
    with open(filename, "wb") as output_file:
        for byte in content:
            output_file.write(byte)


@click.command()
@click.option('--algorithm', '-a',
              required=True,
              type=click.Choice(choices=('Huffman', 'Lempel-Ziv'),
                                case_sensitive=False),
              help='compression algorithm to use')
@click.option('--compress', '-c',
              is_flag=True,
              help='compress FILE')
@click.argument('file', type=click.File('rb'))
def command_line_interface(compress: bool,
                           algorithm: str,
                           file: BinaryIO) -> None:
    """Restore previously compressed FILE to original, or compress FILE."""

    selected = algorithm.lower()
    operation = compress and "compress" or "restore"

    input_filename = file.name
    file_extension = (EXTENSIONS[selected]
                      if compress
                      else EXTENSIONS[operation])
    output_filename = input_filename + file_extension

    verb = compress and 'Compressing' or 'Restoring'
    click.echo(
        f"{verb} {input_filename} into {output_filename} using {algorithm}...")

    imports = {"huffman": Huffman, "lempel-ziv": LempelZiv}
    method = getattr(imports[selected], operation)
    content = method(file)

    write_output(output_filename, content)

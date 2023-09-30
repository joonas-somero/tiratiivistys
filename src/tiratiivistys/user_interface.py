from typing import BinaryIO
import click
from tiratiivistys.constants import EXTENSIONS
from .huffman import Huffman
from .lempel_ziv import LempelZiv


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
    input_filename = file.name
    output_filename = input_filename + EXTENSIONS[selected]

    verb = compress and 'Compressing' or 'Restoring'
    click.echo(
        f"{verb} {input_filename} into {output_filename} using {algorithm}...")

    operation = compress and "compress" or "restore"
    imports = {"huffman": Huffman, "lempel-ziv": LempelZiv}

    getattr(imports[selected], operation)(file)
